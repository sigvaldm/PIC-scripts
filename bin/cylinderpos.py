#!/usr/bin/env python

"""
Computes points on the surface of a cylinder (the probe). Under development.
"""

import numpy as np
import sys

l    = sys.argv[2] #200e-3
r    = 1.0e-3
zmin = -l/2
dz   = sys.argv[3] #2.5e-3
offset = 1
Nz   = int(np.ceil(l/dz))+(1-offset)
Nth  = 1

zs     = np.linspace(zmin+offset*dz/2 , zmin+l-offset*dz/2, Nz)
thetas = np.linspace(0,          2*np.pi,     Nth, endpoint=False)

f = open(sys.argv[1],'w')
f.write('$begin$\n')
f.write('  nvScan=%d\n'%(len(thetas)*len(zs)))

for z in zs:
    for theta in thetas:
        x = r*np.cos(theta)
        y = r*np.sin(theta)
        f.write(" %f %f %f %f\n"%(x,y,z,theta))

f.write('$end\n')
