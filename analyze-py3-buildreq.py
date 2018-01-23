#! /usr/bin/env python3

import sys

pkgs = {}

for line in sys.stdin:
    line = line.rstrip()
    if not line.startswith(' '):
        pkgs[line] = False
        current_package = line
    else:
        if 'python3' in line:
            pkgs[current_package] = True

py3_count = len([v for v in pkgs.values() if v])
total_count = len(pkgs)

print('Python3 BRs: {}/{} -- {}%'.format(py3_count, total_count, 100 * py3_count / total_count))
