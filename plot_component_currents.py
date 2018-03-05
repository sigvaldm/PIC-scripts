#!/usr/bin/env python

"""
Plots the current to the components of a single simulation.

Example:

    ./plot_component_currents.py Run15_25mm_2.5V/pictetra.hst
    ./plot_component_currents.py Run15_25mm_2.5V

In the second case all files matching *.hst in Run15_25mm_2.5V will be merged
into one data array prior to plotting.

In addition the following flags exist:

    -c  Plot only specified components and in the specified order (Default: All
        components in ascending order). The components are numbered from 0 and
        in the same order as in the pictetra.hst file. Expects an expression
        that evaluates into a Python list.

        Example:
            -c "2,3,6,0"            # Components 2, 3, 6 and 0 in that order
            -c "range(6,12)"        # Components 6-11 in ascending order

    -l  Specify legends for the plots. (Default: "Component <x>"). Expects
        an expression that evaluates into a Python list. Supports
        LaTeX-expressions.

        Example:
            -l "'Probe','Bootstrap','End caps'"
            -l "r'$\\alpha$',r'$\\beta$'"

    -r  Specify relaxation time in [us] for Exponential Moving Average (Default
        0.1 us). Expects an expression that evaluates into a floating point
        number. A value of zero turns off averaging.

        Example:
            -r 1e-2

    -t  Turn off "total" plot.

"""

import numpy as np
import matplotlib.pyplot as plt
import sys
from funcs import *

args = sys.argv[1:]

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

if '-t' in args:
    ind = args.index('-t')
    plot_total = False
    args.pop(ind)
else:
    plot_total = True

data = readHst(args[0])

if ids == []:
    num_ids = int((data.shape[1]-6)/3)
    ids = list(range(num_ids))

for i in range(len(legends),len(ids)):
    legends.append("Component %d"%ids[i])

print("Plotting components: ", ids)

ids = np.array(ids)
cids = 8+3*ids # Get index of currents

data[:,1] *= 1e6    # time in us
data[:,8::3] *= 1e6 # curents in uA
dt = data[1,1]-data[0,1]
xaxis = data[:,1]

current = np.sum(data[:,cids],1)

# V = expAvg(data[:,24],dt)[-1]
# I = expAvg(current,dt)[-1]
# Ioml = OML_cylinder(V)*1e6
# print("Steady state voltage : ", V, "V")
# print("Steady state current : ", I, "uA (",100*I/Ioml ,"% of OML)")
# print("OML current          : ", Ioml, "uA")

for cid, legend in zip(cids, legends):
    # plotAvg(xaxis, data[:,cid], 'component %d'%id)
    plotAvg(xaxis, data[:,cid], legend, tau)

if len(ids)>1 and plot_total:
    plotAvg(xaxis, current, 'Total', tau)

# plt.plot(xaxis, Ioml*np.ones(xaxis.shape), label='OML', linewidth=1, linestyle='--')

plt.grid()

if len(ids)>1:
    plt.legend(loc="lower right")

plt.xlabel("Time [$\mathrm{\mu s}$]")
plt.ylabel("Current [$\mathrm{\mu A}$]")
plt.title("Component Current")

plt.show()
