#!/usr/bin/env python

"""
Plots the current to every segment of a single probe.

Example:

    ./plot_segment_currents.py Run15_25mm_2.5V/pictetra.hst
    ./plot_segment_currents.py Run15_25mm_2.5V

In the second case all files matching *.hst in Run15_25mm_2.5V will be merged
into one data array prior to plotting.
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
from funcs import *

data = readHst(sys.argv[1])

data[:,1] *= 1e6    # time in us
data[:,8::3] *= 1e6 # curents in uA
dt = data[1,1]-data[0,1]
xaxis = data[:,1]

current = data[:,26]+data[:,29]+data[:,32]+data[:,35]+data[:,38]+data[:,41]

V = expAvg(data[:,24],dt)[-1]
I = expAvg(current,dt)[-1]
Ioml = OML_cylinder(V)*1e6
print("Steady state voltage : ", V, "V")
print("Steady state current : ", I, "uA (",100*I/Ioml ,"% of OML)")
print("OML current          : ", Ioml, "uA")

plotAvg(xaxis, data[:,26], 'segment 1')
plotAvg(xaxis, data[:,29], 'segment 2')
plotAvg(xaxis, data[:,32], 'segment 3')
plotAvg(xaxis, data[:,35], 'segment 4')
plotAvg(xaxis, data[:,38], 'segment 5')
plotAvg(xaxis, data[:,20], 'insulator (cylindrical part)')
plotAvg(xaxis, data[:,23], 'insulator (annular part)')
plotAvg(xaxis, data[:,32], 'end cap')
plotAvg(xaxis, current   , 'total')
plt.plot(xaxis, Ioml*np.ones(xaxis.shape), label='OML', linewidth=1, linestyle='--')

plt.grid()

plt.legend(loc="lower right")
plt.xlabel("Time [$\mathrm{\mu s}$]")
plt.ylabel("Current [$\mathrm{\mu A}$]")
plt.title("Probe Section Current")

plt.show()
