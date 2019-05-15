#!/usr/bin/env python
import meshio
import numpy as np
import sys
import re
import os
from langmuir import *
from scipy.constants import value as constants
from fitfuncs import *

path = sys.argv[1]

r, l, n, eV, eta = get_probe_params(path)

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

if len(sys.argv)>3:
    dz = float(sys.argv[3])
else:
    dz = r

z_delimiters = np.arange(zmin, zmax + dz/2, dz)
z_midpoints = 0.5*(z_delimiters[:-1]+z_delimiters[1:])
Is = np.zeros_like(z_midpoints)

a = 0
for i, delim in enumerate(z_delimiters[1:]):
    where_smaller = np.where(z_centroids <= delim)[0]
    if len(where_smaller):
        b = np.where(z_centroids <= delim)[0][-1]
    else:
        b = a # No facets within this range, sum to zero.
    Is[i] = np.average(facet_currents[a:b])
    a = b

Is *= 2*np.pi*r

with open(sys.argv[2], 'w') as file:
    file.write("#:xaxis\tz\n")
    file.write("#:name\tz\tOML\tI\tg\n")
    file.write("#:units\tm\tA/m\tA/m\tdimensionless\n")

    for z, I in zip(z_midpoints, Is):
        file.write("{}\t{}\t{}\t{}\n"
                   .format(z, I_OML, I, I/I_OML))
