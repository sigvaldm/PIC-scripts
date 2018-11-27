#!/usr/bin/env python
import meshio
import numpy as np
import matplotlib.pyplot as plt
from scipy.constants import value as constants
import sys
import os
import re
from langmuir import *

path = sys.argv[1]

l   = float(re.search('[\d\.]+(?=mm)', path).group())*1e-3
n   = float(re.search('[\d\.]+(?=n)', path).group())*1e10
eV  = float(re.search('[\d\.]+(?=eV)', path).group())
eta = -float(re.search('[\d\.]+(?=eta)', path).group())
print('l={}, n={}, eV={}, eta={}'.format(l, n, eV, eta))

r = 1e-3
elec = Species(n=n, eV=eV)
I_OML = OML_current(Cylinder(r, 1), elec, eta=eta)
print("I_OML={} A/m".format(I_OML))
vrms = elec.vth*np.sqrt(2)

zs = []
with open(os.path.join(path,'scanpositions.txt')) as file:
    for line in file:
        try:
            x,y,z,theta = line.split()
            zs.append(float(z))
        except:
            pass

zs = np.array(zs)
Is = np.zeros_like(zs)

for i in range(len(zs)):

    try:
        mesh = meshio.read(os.path.join(path,'distfunct{:06d}.vtk'.format(i+1)))

        cells  = mesh.cells['hexahedron']
        data   = mesh.point_data['scalars']
        points = mesh.points
        points *= vrms
        data   /= vrms**3

        data = np.array([-p[0]*d for p, d in zip(points,data)])

        cell_points = np.array([points[c] for c in cells])
        cell_volumes = np.prod(np.max(cell_points,1) - np.min(cell_points,1),1)
        cell_averages = np.array([np.average(data[c]) for c in cells])

        integral = np.sum(cell_volumes*cell_averages)
        current = 2*np.pi*r*elec.q*integral
        Is[i] = current
    except:
        pass

if len(zs)==1:
    print("Single current: {} A/m".format(Is[0]))

else:
    dz = zs[1]-zs[0]
    I_int = dz*sum(Is)
    print("OML      {} A".format(I_OML*l))
    print("Integral {} A".format(I_int))

    plt.plot(zs*1e3, Is*1e3)
    plt.plot(zs*1e3, I_OML*1e3*np.ones_like(zs))
    plt.grid()
    plt.show()