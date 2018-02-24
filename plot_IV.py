#!/usr/bin/env python

"""
Plots IV (current-voltage) characteristics.

Example:

    ./plot_IV.py Run15_50mm_*   # Plot IV curve for 50 mm
    ./plot_IV.py Run15_*5*mm*   # Plot IV curve for 25 and 50 mm but not 100 mm
    ./plot_IV.py Run15_*        # Plot all IV curves for Run15
    ./plot_IV.py Run15_* -p 25  # Same as above but plot current per 25 mm
    ./plot_IV.py -p 25 Run15_*  # Same as above

This will plot IV-characteristics based on *.hst files in the selected folders.
The I and V datapoints is taken as the last timestep in the *.hst files after
exponential moving averaging. The units on the y-axis is [uA/mm] unless the 'p'
flag is used. Then it is uA per some integer number of mm. This is useful for
comparison with e.g. Huy who uses uA per 25 mm. The length of the probe is
deduced from the name of the folder, so the folders must contain the string
'<digits>mm'. E.g. 'Run15_50mm_2.5V' will be deduced to be a 50mm probe. All
folders specifying the same length will be taken as one datapoint on an IV curve
for that length. Comparison is made with OML theory.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import sys
import re
from funcs import *

def OML_func(V, c, beta):
    return c*V**beta

paths = sys.argv[1:]

perlength = 1
if '-p' in paths:
    ind = paths.index('-p')
    perlength = int(paths[ind+1])
    paths.pop(ind+1)
    paths.pop(ind)

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
