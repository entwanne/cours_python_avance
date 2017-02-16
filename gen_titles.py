#!/usr/bin/env python3

import re
import os

files = []

for directory, _, filenames in os.walk('src'):
    for filename in filenames:
        files.append(os.path.join(directory, filename))

def sort_key(path):
    return tuple(int(re.sub(r'[^0-9]', '', x) or 0) for x in path.split('/'))

files.sort(key=sort_key)


print('% Notions de Python avancées')

for filename in files:
    with open(filename, 'r') as f:
        code = False
        for line in f:
            if re.match(r'```', line):
                code = not code
                continue
            if code:
                continue

            m = re.match(r'(#+) (.+)$', line)
            if m:
                tabs = len(m.group(1)) - 1
                if not tabs:
                    print()
                print('{}- {}'.format('    ' * tabs, m.group(2)))
