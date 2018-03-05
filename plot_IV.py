#!/usr/bin/env python

"""
Plots IV (current-voltage) charactersitics based on a set of simulations.

Example:

    ./plot_IV.py Run15_50mm_*   # Plot IV curve for 50 mm
    ./plot_IV.py Run15_*5*mm*   # Plot IV curve for 25 and 50 mm but not 100 mm
    ./plot_IV.py Run15_*        # Plot all IV curves for Run15

This will plot IV-characteristics based on *.hst files in the selected folders.
The I and V datapoints is taken as the last timestep in the *.hst files after
exponential moving averaging. The units on the y-axis is in current per length.
The length of the probe is deduced from the name of the folder, so the folders
must contain the string '<digits>mm'. E.g. 'Run15_50mm_2.5V' will be deduced to
be a 50mm probe. All folders specifying the same length will be taken as one
datapoint on an IV curve for that length. Comparison is made with OML theory.

In addition the following flags exist:

    -c  Include currents only from specified components (Default: All
        components). The components are numbered from 0 and in the same order as
        in the pictetra.hst file. Expects an expression that evaluates into a
        Python list.

        Example:
            -c "2,3,6,0"            # Components 2, 3, 6 and 0 in that order
            -c "range(6,12)"        # Components 6-11 in ascending order

    -r  Specify relaxation time in [us] for Exponential Moving Average (Default
        0.1 us). Expects an expression that evaluates into a floating point
        number. A value of zero turns off averaging.

        Example:
            -r 1e-2

    -p  Plot currents in uA per something mm. Useful for comparison with e.g.
        Huy which uses uA per 25 mm.

        Example:
            -p 25                   # Current is in [uA / 25 mm]
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import sys
import re
from funcs import *

def OML_func(V, c, beta):
    return c*V**beta

args = sys.argv[1:]

if '-c' in args:
    ind = args.index('-c')
    ids = np.array(eval(args[ind+1]))
    ids = ids.reshape((-1)) # Wraps it in a list if it's a pure number
    args.pop(ind+1)
    args.pop(ind)
else:
    ids = []

if '-r' in args:
    ind = args.index('-r')
    tau = float(eval(args[ind+1]))
    args.pop(ind+1)
    args.pop(ind)
else:
    tau = 0.1

if '-p' in args:
    ind = args.index('-p')
    perlength = int(args[ind+1])
    args.pop(ind+1)
    args.pop(ind)
else:
    perlength = 1

pattern = re.compile('([0-9]+)mm')
datasets = dict()

for path in args:
    data = readHst(path)
    length = pattern.search(path).group(1)
    data[:,1] *= 1e6    # time in us
    data[:,8::3] *= 1e6 # curents in uA
    xaxis = data[:,1]
    dx = xaxis[1]-xaxis[0]
    if ids == []:
        num_ids = int((data.shape[1]-6)/3)
        cids = np.array((range(num_ids)),dtype=int)
    else:
        cids = np.array(ids)
    cids = 8+3*cids # Get index of currents
    current = np.sum(data[:,cids],1)
    V = expAvg(data[:,cids[0]-2],dx)[-1]
    I = -expAvg(current,dx)[-1]*perlength/int(length)
    if not length in datasets:
        datasets[length] = ([],[]) # List of x-values vs y-values
    datasets[length][0].append(V)
    datasets[length][1].append(I)

Voml = np.linspace(0,8,100)
Ioml = -OML_cylinder(Voml, l=perlength*1e-3)*1e6
plt.plot(Voml, Ioml, label='OML theory')

for key in datasets:
    V = np.array(datasets[key][0])
    I = np.array(datasets[key][1])
    popt, pcov = curve_fit(OML_func, V, I)
    perr = np.sqrt(np.diag(pcov))
    beta = popt[1]
    betaerr = 3*perr[1] # 3 sigma error

    p = plt.plot(V,I,'o', label=key+'mm, $\\beta=%.2f\pm %.2f$'%(beta,betaerr))
    color = p[-1].get_color()

    plt.plot(Voml, OML_func(Voml,*popt), '--', color=color, linewidth=1)

plt.title('IV-characteristics')
plt.xlabel('Voltage [V]')
if perlength==1:
    plt.ylabel('Current [$\mathrm{\mu A/mm}$]')
else:
    plt.ylabel('Current [$\mathrm{\mu A/%d mm}$]'%perlength)
plt.legend(loc='upper left')
plt.grid()
plt.show()
