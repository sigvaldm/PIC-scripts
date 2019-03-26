#!/usr/bin/env python
import meshio
import numpy as np
from scipy.constants import value as constants
import sys
import os
import re
from langmuir import *
# from statsmodels.nonparametric.smoothers_lowess import lowess
from loess.loess_1d import loess_1d

# Read file and path-encoded info
path = os.path.abspath(sys.argv[1])
l    =  float(re.findall('[\d\.]+(?=mm)' , path)[-1])*1e-3
n    =  float(re.findall('[\d\.]+(?=n)'  , path)[-1])*1e10
eV   =  float(re.findall('[\d\.]+(?=eV)' , path)[-1])
eta  = -float(re.findall('[\d\.]+(?=eta)', path)[-1])
print('l={}, n={}, eV={}, eta={}'.format(l, n, eV, eta))

# path = sys.argv[1]
# l   = float(re.search('[\d\.]+(?=mm)', path).group())*1e-3
# n   = float(re.search('[\d\.]+(?=n)', path).group())*1e10
# eV  = float(re.search('[\d\.]+(?=eV)', path).group())
# eta = -float(re.search('[\d\.]+(?=eta)', path).group())
# print('l={}, n={}, eV={}, eta={}'.format(l, n, eV, eta))

r = 1e-3
elec = Species(n=n, eV=eV)
I_OML = OML_current(Cylinder(r, 1), elec, eta=eta)
print("I_OML={} A/m".format(I_OML))

mesh = meshio.read(path)

z_vertices = mesh.points[:,2]
cells = mesh.cells['triangle']
z_centroids = np.average(z_vertices[cells], axis=1)
facet_currents = mesh.cell_data['triangle']['J']

# Sort along probe
ind = np.argsort(z_centroids)
z_centroids = z_centroids[ind]
facet_currents = facet_currents[ind]

zmin = z_centroids[0]
zmax = z_centroids[-1]

# Filter end caps
tol = 1e-10
ind = np.logical_and(np.abs(z_centroids-zmin)>tol,
                     np.abs(z_centroids-zmax)>tol)
z_centroids = z_centroids[ind]
facet_currents = facet_currents[ind]

print("Number of points: {}".format(len(facet_currents)))

if len(sys.argv)>3:
    dz = float(sys.argv[3])
else:
    dz = 0.0001

window = 7.5e-3
frac = window/l
# z0 = np.arange(zmin, zmax + dz/2, dz)
z0 = np.linspace(zmin, zmax, int(l/dz)+1, endpoint=True)
# res = lowess(facet_currents, z_centroids, it=0, return_sorted=True, frac=frac)
# Is = res[:,1]
z_loess, Is, w_loess = loess_1d(z_centroids, facet_currents, degree=2, frac=frac, x0=z0)

Is *= 2*np.pi*r
facet_currents *= 2*np.pi*r

with open(sys.argv[2], 'w') as file:
    file.write("#:xaxis\tz\n")
    file.write("#:name\tz\tOML\tI\tg\ti\n")
    file.write("#:units\tm\tA/m\tA/m\tdimensionless\tA/m\n")

    for z, facet_current, I in zip(z0, facet_currents, Is):
        file.write("{}\t{}\t{}\t{}\t{}\n"
                   .format(z, I_OML, I, I/I_OML, facet_current))
