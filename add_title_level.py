#!/usr/bin/env python3

import re
import os

files = []

for directory, _, filenames in os.walk('src'):
    for filename in filenames:
        files.append(os.path.join(directory, filename))

code = False
def handle_line(line):
    global code
    if re.match(r'```', line):
        code = not code
        return line
    if code:
        return line

    m = re.match(r'#+ .+$', line)
    if m:
        line = '#' + line
    return line

for filename in files:
    with open(filename, 'r') as f:
        lines = f.readlines()
    lines = [handle_line(l) for l in lines]
    with open(filename, 'w') as f:
        f.write(''.join(lines))
