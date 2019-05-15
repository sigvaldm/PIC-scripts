#!/usr/bin/env python

# DEPRECATED
# use normprof.py and constrprof.py instead

import sys
import metaplot as mpl
import numpy as np

# Read data
df = mpl.DataFrame(sys.argv[1])
z = df['z'].to('m').m
OML = df['OML'].to('A/m').m[0]
g = df['g'].m

# Shift z-axis to origin
dz = z[1]-z[0]
z -= z[0]-dz/2

half = int(len(z)/2)
f = 0.5*(g[:half] + g[:half-1:-1])
z = z[:half]

num = int(sys.argv[3])
z_new = z[:num] - num*1e-3/2
g_new = f[:num] * f[num-1::-1]

with open(sys.argv[2], 'w') as file:
    file.write("#:xaxis\tz\n")
    file.write("#:name\tz\tOML\tI\tg\n")
    file.write("#:units\tm\tA/m\tA/m\tdimensionless\n")

    for z, g in zip(z_new, g_new):
        file.write("{}\t{}\t{}\t{}\n"
                   .format(z, OML, g*OML, g))
