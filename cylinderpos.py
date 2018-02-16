#!/usr/bin/env python

"""
Computes points on the surface of a cylinder (the probe). Under development.
"""

import numpy as np
import sys

l    = 25e-3
r    = 0.255e-3
zmin = 0.046 
dz   = 1e-3
Nz   = int(np.ceil(l/dz))
Nth  = 8

zs     = np.linspace(zmin+dz/2 , zmin+l-dz/2, Nz)
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
