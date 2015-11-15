#!/usr/bin/env python

import json
import sys
import os.path
import re
from collections import OrderedDict
from zipfile import ZipFile

archive_name = sys.argv[1]
sections = sys.argv[2:]

manifest = {
    'introduction': sections.pop(0),
    'conclusion': sections.pop(-1),
    'object': 'container',
    'slug': 'notions-de-python-avancees',
    'title': 'Notions de Python avancées',
    'version': 2,
    'description': 'Découvrez Python plus en profondeur',
    'type': 'TUTORIAL',
    'licence': 'CC BY-SA'
}

trans = str.maketrans('','','#*_`\n')

with ZipFile(archive_name, 'w') as archive:
    for section in (manifest['introduction'], manifest['conclusion']):
        with open(section, 'r') as f:
            next(f)
            archive.writestr(section, f.read())

    parts = OrderedDict()
    for section in sections:
        *_, part_name, sec_name = section.split('/')
        sec_name, _ = os.path.splitext(sec_name)
        part = parts.setdefault(part_name, {'object': 'container', 'slug': part_name, 'title': part_name, 'children': []})
        with open(section, 'r') as f:
            title = next(f).translate(trans).strip()
            archive.writestr(section, f.read())
        if sec_name.startswith('0'):
            part['introduction'] = section
            part['title'] = title
        else:
            part['children'].append({'object': 'extract', 'slug': sec_name, 'title': title, 'text': section})

    manifest['children'] = list(parts.values())
    archive.writestr('manifest.json', json.dumps(manifest, indent=4))
