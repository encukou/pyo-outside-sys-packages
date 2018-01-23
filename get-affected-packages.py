#! /usr/bin/env python3

import sys
import subprocess

files = set(l.strip() for l in sys.stdin)

def pick_package(packages):
    packages = [p.strip() for p in packages if p]
    x86_64 = [p for p in packages if 'x86_64' in p]
    if x86_64:
        return x86_64[0]
    return packages[0]

while files:
    file = sorted(files)[0]
    files.remove(file)
    print('processing file', file, file=sys.stderr)

    result = subprocess.run(
        ["sudo", "dnf",
         "--disablerepo=*",
         "--enablerepo=rawhide",
         "repoquery", file],
        stdout=subprocess.PIPE, encoding='utf-8')
    packages = result.stdout.splitlines()
    print('got packages', packages, file=sys.stderr)
    package_name = pick_package(packages)
    print('got package', package_name, file=sys.stderr)
    print(package_name)

    result = subprocess.run(
        ["sudo", "dnf",
         "--disablerepo=*",
         "--enablerepo=rawhide",
         "repoquery", "-l", package_name],
        stdout=subprocess.PIPE, encoding='utf-8')
    for line in result.stdout.splitlines():
        line = line.strip()
        if line in files or line == file:
            print('xxxx', line.strip(), file=sys.stderr)
            files.discard(line.strip())
        else:
            print('----', line.strip(), file=sys.stderr)

    print(len(files), 'files remaining', file=sys.stderr)
