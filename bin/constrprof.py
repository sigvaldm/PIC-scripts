#!/usr/bin/env python

import sys
import metaplot as mpl
import numpy as np
import os
import re
from langmuir import *

fnin  = os.path.abspath(sys.argv[1])
fnout = os.path.abspath(sys.argv[2])

# Determine parameters on new file based on path name
l    =  float(re.findall('[\d\.]+(?=mm)' , fnout)[-1])*1e-3
n    =  float(re.findall('[\d\.]+(?=n)'  , fnout)[-1])*1e10
eV   =  float(re.findall('[\d\.]+(?=eV)' , fnout)[-1])
eta  = -float(re.findall('[\d\.]+(?=eta)', fnout)[-1])
print('l={}, n={}, eV={}, eta={}'.format(l, n, eV, eta))

electron = Species(n=n, eV=eV)
debye = electron.debye
OML = OML_current(Cylinder(r=1e-3, l=1), electron, eta=eta)

df = mpl.DataFrame(fnin)
Zn = df['Zn'].m
f = df['f'].m

Z = Zn*debye

res = 0.1*debye
Z_interp = np.linspace(0, l, int(np.ceil(l/res)+1))
Z_interp = np.array([a for a in Z_interp if a>min(Z) and a<l-min(Z)])

f_interp = np.interp(Z_interp, Z, f)
g_interp = f_interp * f_interp[::-1]

with open(fnout, 'w') as fout:
    fout.write("#:xaxis\tz\n")
    fout.write("#:name\tz\tzn\tZ\tZn\tOML\tI\tg\tf\n")
    fout.write("#:units\tm\tdimensionless\tm\tdimensionless\tA/m\tA/m\tdimensionless\tdimensionless\n")

    for Z, g, f in zip(Z_interp, g_interp, f_interp):
        z = Z-l/2
        zn = z/debye
        Zn = Z/debye
        I = OML*g
        fout.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n"
                   .format(z, zn, Z, Zn, OML, I, g, f))
