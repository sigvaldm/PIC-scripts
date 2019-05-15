#!/usr/bin/env python

import sys
import metaplot as mpl
import numpy as np
import os
import re
import langmuir
from fitfuncs import *

fnin = os.path.abspath(sys.argv[1])

if len(sys.argv)>2:
    fnout = sys.argv[2]
else:
    fnout = fnin

r, l, n, eV, eta = get_probe_params(fnin)

debye = langmuir.Species(n=n, eV=eV).debye

df = mpl.DataFrame(fnin)
z = df['z'].to('m').m
g = df['g'].m

Z  = z+l/2
zn = z/debye
Zn = Z/debye

f = np.ones_like(g)
for i in range(int(np.ceil(len(f)/2))):
    ind = np.where(np.abs(np.abs(z)-np.abs(z[i]))<1e-5)
    f[i] = np.average(g[ind])

i = 0
with open(fnout, 'w') as fout:
    with open(fnin) as fin:
        for line in fin:
            fout.write(line.rstrip('\n'))

            if '#:xaxis' in line:
                fout.write('')
            elif '#:name' in line:
                fout.write('\tZ\tzn\tZn\tf')
            elif '#:units' in line:
                fout.write('\tm\tdimensionless\tdimensionless\tdimensionless')
            else:
                fout.write('\t{}\t{}\t{}\t{}'.format(Z[i], zn[i], Zn[i], f[i]))
                i += 1

            fout.write('\n')
