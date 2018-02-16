#!/usr/bin/env python

"""
Plots the current to one or more probes.

Example:

    ./plot_currents.py Run15_25mm_2.5V/pictetra.hst
    ./plot_currents.py Run15_25mm_2.5V
    ./plot_currents.py Run15_*

In the second case all files matching *.hst in Run15_25mm_2.5V will be merged
into one data array prior to plotting. In the third case all folders matching
Run15_* will be plotted as a separate graph in the same plot.
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
import re
from funcs import *

plt.figure(1)
plt.grid()
plt.title('Comparison of simulation runs')
plt.xlabel('Time [$\mathrm{\mu s}$]')
plt.ylabel('Current [$\mathrm{\mu A}$]')

paths = sys.argv[1:]
paths.sort()
pattern = re.compile('([0-9]+)mm')

for path in paths:
    data = readHst(path)
    length = int(pattern.search(path).group(1))*1e-3
    data[:,1] *= 1e6    # time in us
    data[:,8::3] *= 1e6 # curents in uA
    xaxis = data[:,1]
    dx = xaxis[1]-xaxis[0]
    V = expAvg(data[:,24],dx)[-1]
    Ioml = OML_cylinder(V,l=length)*1e6
    current = data[:,26]+data[:,29]+data[:,32]+data[:,35]+data[:,38]+data[:,41]
    p = plotAvg(xaxis, current, path)
    color = p[-1].get_color()
    # plt.plot(xaxis, Ioml*np.ones(xaxis.shape), '--', color=color, linewidth=1)

plt.legend(loc='lower right')
plt.show()

