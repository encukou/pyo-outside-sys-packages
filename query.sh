#! /bin/bash -ex

# Note: things get cached; `rm *.txt` to clean the cache entirely


# Get all pyo files in Rawhide
if [ '!' -e all-pyo-files.txt ]; then
    sudo dnf --disablerepo='*' --enablerepo='rawhide' repoquery -l '/**/*.pyo' | tee all-pyo-files.txt
fi

echo 'All .pyo:' $(cat all-pyo-files.txt | grep '\.pyo$' | wc -l)

# Filter out sitelib & pypy
if [ '!' -e non-site-pyo-files.txt ]; then
    cat all-pyo-files.txt | grep '\.pyo$' |
        grep -v --perl '/usr/lib(64)?/python[2-3]\.[0-9]/' |
        grep -v --perl '/usr/lib(64)?/pypy-[0-9.]+/lib' |
        sort | tee non-site-pyo-files.txt
fi

# Given a list of files, get the list of packages. (XXX slow!!)
if [ '!' -e affected-packages.txt ]; then
    cat non-site-pyo-files.txt | python3 get-affected-packages.py |
        sed -es'/-[0-9]*:.*$//' |
        sort | uniq | tee affected-packages.txt
fi

echo 'Affected packages:' $(cat affected-packages.txt | wc -l)
