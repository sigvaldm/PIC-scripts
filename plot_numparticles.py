#!/usr/bin/env python

"""
Plots the number of particles in the domain for a simulation of a probe.

Example:

    ./plot_numparticles.py Run15_25mm_2.5V/pictetra.hst
    ./plot_numparticles.py Run15_25mm_2.5V

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
xaxis = data[:,1]

plt.plot(xaxis, data[:,2], linewidth=1, label='Electrons')
plt.plot(xaxis, data[:,3], linewidth=1, label='Ions')
plt.ylabel("Number of particles")
plt.title("Number of particles in simulation domain")
plt.grid()
plt.legend(loc="lower right")

plt.show()
