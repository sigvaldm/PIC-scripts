#!/usr/bin/env python

"""
Plots the total current to the spacecraft components for many simulations.

Example:

    ./plot_currents.py Run15_25mm_2.5V/pictetra.hst
    ./plot_currents.py Run15_25mm_2.5V
    ./plot_currents.py Run15_*

In the second case all files matching *.hst in Run15_25mm_2.5V will be merged
into one data array prior to plotting. In the third case all folders matching
Run15_* will be plotted as a separate graph in the same plot.

In addition the following flags exist:

    -c  Include currents only from specified components (Default: All
        components). The components are numbered from 0 and in the same order as
        in the pictetra.hst file. Expects an expression that evaluates into a
        Python list.

        Example:
            -c "2,3,6,0"            # Components 2, 3, 6 and 0 in that order
            -c "range(6,12)"        # Components 6-11 in ascending order

    -l  Specify legends for the plots. (Default: "Component <x>"). Expects
        an expression that evaluates into a Python list. Supports
        LaTeX-expressions.

        Example:
            -l "'25mm','50mm','100mm'"
            -l "r'$\\alpha$',r'$\\beta$'"

    -r  Specify relaxation time in [us] for Exponential Moving Average (Default
        0.1 us). Expects an expression that evaluates into a floating point
        number. A value of zero turns off averaging.

        Example:
            -r 1e-2
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

args = sys.argv[1:]
pattern = re.compile('([0-9]+)mm')

if '-c' in args:
    ind = args.index('-c')
    ids = np.array(eval(args[ind+1]))
    ids = ids.reshape((-1)) # Wraps it in a list if it's a pure number
    args.pop(ind+1)
    args.pop(ind)
else:
    ids = []

if '-l' in args:
    ind = args.index('-l')
    legends = list(eval(args[ind+1]))
    args.pop(ind+1)
    args.pop(ind)
else:
    legends = []

if '-r' in args:
    ind = args.index('-r')
    tau = float(eval(args[ind+1]))
    args.pop(ind+1)
    args.pop(ind)
else:
    tau = 0.1

for i in range(len(legends), len(args)):
    legends.append(args[i])

print("Last datapoint in averaged current:")

for path, legend in zip(args, legends):
    data = readHst(path)
    data[:,1] *= 1e6    # time in us
    data[:,8::3] *= 1e6 # curents in uA
    xaxis = data[:,1]
    dx = xaxis[1]-xaxis[0]
    # dx_last = xaxis[-1]-xaxis[-2]
    # print("  {}: {} s == {} s ?".format(legend, dx*1e-6, dx_last*1e-6))
    if ids == []:
        num_ids = int((data.shape[1]-6)/3)
        cids = np.array((range(num_ids)),dtype=int)
    else:
        cids = np.array(ids)
    cids = 8+3*cids # Get index of currents
    current = np.sum(data[:,cids],1)
    plotAvg(xaxis, current, legend, tau)

    dx = xaxis[1]-xaxis[0]
    last_avg_point = expAvg(current, dx, tau)[-1]
    print("  {}: {} uA".format(legend, last_avg_point))

if len(args)>1:
    plt.legend(loc='lower right')
plt.show()

