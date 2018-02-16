#!/usr/bin/env python

"""
Plots IV (current-voltage) characteristics.

Example:

    ./plot_IV.py Run15_*

This will plot IV-characteristics based on *.hst files in all folders starting
with "Run15_". The I and V datapoints is taken as the last timestep in the *.hst
files after exponential moving averaging. The units on the y-axis is [uA/mm].
The length of the probe is deduced from the name of the folder, so the folders
must contain the string '<digits>mm'. E.g. 'Run15_50mm_2.5V' will be deduced to
be a 50mm probe. All IV datapoints having the same probe length is treated as
probe, having one legend. Comparison is made with OML theory.
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
import re
from funcs import *

plt.figure(1)
plt.grid()
plt.title('IV-characteristics')
plt.xlabel('Voltage [V]')
plt.ylabel('Current [$\mathrm{\mu A/mm}$]')

paths = sys.argv[1:]
paths.sort()
pattern = re.compile('([0-9]+)mm')

datasets = dict()
for path in paths:
    data = readHst(path)
    length = pattern.search(path).group(1)
    data[:,1] *= 1e6    # time in us
    data[:,8::3] *= 1e6 # curents in uA
    xaxis = data[:,1]
    dx = xaxis[1]-xaxis[0]
    current = data[:,26]+data[:,29]+data[:,32]+data[:,35]+data[:,38]+data[:,41]
    V = expAvg(data[:,24],dx)[-1]
    I = -expAvg(current,dx)[-1]/int(length)
    if not length in datasets:
        datasets[length] = ([],[]) # List of x-values vs y-values
    datasets[length][0].append(V)
    datasets[length][1].append(I)

for key in datasets:
    V = datasets[key][0]
    I = datasets[key][1]
    plt.plot(V,I,'o',label=key+'mm')

V = np.linspace(0,8,100)
I = -OML_cylinder(V, l=1e-3)*1e6
plt.plot(V, I, label='OML theory')

plt.legend(loc='upper left')
plt.show()
