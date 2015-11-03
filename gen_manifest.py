#!/usr/bin/env python

import json
import sys
import os.path
import re
from collections import OrderedDict

sections = sys.argv[1:]

manifest = {
    'introduction': sections.pop(0),
    'conclusion': sections.pop(-1),
    'object': 'container',
    'slug': 'cours',
    'title': 'cours',
    'version': 2,
    'description': '',
    'type': 'TUTORIAL',
    'licence': ''
}


parts = OrderedDict()
for section in sections:
    *_, part_name, sec_name = section.split('/')
    sec_name, _ = os.path.splitext(sec_name)
    part = parts.setdefault(part_name, {'object': 'container', 'slug': part_name, 'title': part_name, 'children': []})
    with open(section, 'r') as f:
        title = re.sub(r'^#+\s+(.+)\s*$', r'\1', next(f))
    if sec_name.startswith('0'):
        part['introduction'] = section
        part['title'] = title
    else:
        part['children'].append({'object': 'extract', 'slug': sec_name, 'title': title, 'text': section})

manifest['children'] = list(parts.values())
print(json.dumps(manifest, indent=4))
