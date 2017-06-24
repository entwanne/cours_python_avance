#!/usr/bin/env python3

import json
import sys
import os.path
import re
from collections import OrderedDict
from zipfile import ZipFile

archive_name = sys.argv[1]
sections = sys.argv[2:]

manifest = {
    'slug': 'notions-de-python-avancees',
    'title': 'Notions de Python avancées',
    'version': 2,
    'description': 'Découvrez Python plus en profondeur',
    'type': 'TUTORIAL',
    'licence': 'CC BY-SA'
}

from collections import OrderedDict
container = OrderedDict()
# Number of nested levels
document_depth = 0
trans = str.maketrans('','','#*_`\n')

# Split filenames into a dict that represent file hierarchy
for section in sections:
    *path, filename = section.split('/')
    document_depth = max(document_depth, len(path))
    parent = container
    for p in path:
        parent = parent.setdefault(p, OrderedDict())
    parent[filename] = section

# Prefix for 1st-level titles
title_prefix = '#' * (document_depth + 1)

# Rewrite titles of files
def rewrite_titles(f):
    code = False
    for i, line in enumerate(f):
        if line.startswith('```'):
            code = not code
        elif not code and line.startswith('#'):
            if line.startswith(title_prefix):
                line = line[document_depth:]
            else:
                print('Warning with title {!r} in file {}:{}'.format(line, f.name, i))
        yield line

# Write a file in the archive
def write_file(archive, filename):
    with open(filename, 'r') as f:
        title = next(f).translate(trans).strip()
        content = ''.join(rewrite_titles(f))
    archive.writestr(filename, content)
    return title

# Recursively construct a document
def make_document(archive, obj, name=None):
    if isinstance(obj, str):
        extract = {'object': 'extract', 'text': obj}
        extract['slug'], _ = os.path.splitext(name)
        extract['title'] = write_file(archive, obj)
        return extract
    container = {'object': 'container'}
    if name:
        container['slug'] = name
    keys = list(obj.keys())
    if keys[0].startswith('0-'):
        container['introduction'] = obj.pop(keys[0])
        container['title'] = write_file(archive, container['introduction'])
    if keys[-1].startswith('x-'):
        container['conclusion'] = obj.pop(keys[-1])
        write_file(archive, container['conclusion'])
    if obj:
        container['children'] = [make_document(archive, child, name) for name, child in obj.items()]
    return container

with ZipFile(archive_name, 'w') as archive:
    document = make_document(archive, container['src'])
    document.update(manifest)
    archive.writestr('manifest.json', json.dumps(document, indent=4))
