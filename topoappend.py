#!/usr/bin/env python

import meshio
import sys
from shutil import copyfile

topo_file = sys.argv[1]
vtk_file = sys.argv[2]
out_file = sys.argv[3]

print("Copying {} to {}".format(topo_file, out_file))
copyfile(topo_file, out_file)

print("Reading {}".format(vtk_file))
mesh = meshio.read(vtk_file)
data = mesh.point_data

with open(out_file, 'a') as file:

    for varname in data:
        print("Copying data field {} from {} to {}"
              .format(varname, vtk_file, out_file))
        file.write("$dependent variable: {}$\n".format(varname))
        for i, value in enumerate(data[varname], 1):
            file.write("{:8}  {:13E}\n".format(i, value))
        file.write("$fin\n")
