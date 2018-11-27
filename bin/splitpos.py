#!/usr/bin/env python

import sys
import os

path = sys.argv[1]

id = 0
fname = os.path.join(path, 'scanpositions.txt')
with open(fname) as file:
    for line in file:
        if '$begin$' in line: continue
        if '$end$' in line: continue
        if 'nvScan' in line: continue
