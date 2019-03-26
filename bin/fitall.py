#!/usr/bin/env python
import numpy as np
import sys
import re
import os
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from fitfuncs import *

def func(z, a, b, c, d, e):
    return (a*np.exp(-b*z)+c*np.exp(-d*z))*(z**e)+1

def gunc(xdata, a, b, c, d, e, f):
    z, l, eta = xdata
    res = f*func(z, a, b, c, d, e)*func(l-z, a, b, c, d, e)
    return res

xdata = np.array([]).reshape(3,-1)
ydata = np.array([])

for path in sys.argv[1:]:
    print(path)

    indeps, facet_currents = get_data(path)

    xdata = np.append(xdata, indeps, axis=1)
    ydata = np.append(ydata, facet_currents)

lower = ( 0     , 0     , 0     , 0     ,  0     , 0     )
upper = ( 10    , 10    , 10    , 0.2   ,  10    , 10    )

popt, pcov = curve_fit(gunc, xdata, ydata, bounds=(lower, upper))
perr = np.sqrt(np.diag(pcov))

print("Popt", popt)
print("Perr", perr)

for path_ in sys.argv[1:]:
    print(path_)
    path = os.path.abspath(path_)
    l    =  float(re.findall('[\d\.]+(?=mm)' , path)[-1])*1e-3
    n    =  float(re.findall('[\d\.]+(?=n)'  , path)[-1])*1e10
    eV   =  float(re.findall('[\d\.]+(?=eV)' , path)[-1])
    eta  = -float(re.findall('[\d\.]+(?=eta)', path)[-1])
    print('l={}, n={}, eV={}, eta={}'.format(l, n, eV, eta))

    zint = np.linspace(0, l, int(1e4))
    lint = l*np.ones_like(zint)
    plt.plot(xdata[0], ydata, label='Simulated current')
    plt.plot(zint, gunc([zint,lint,zint], *popt), label='Curve fit')
    plt.legend()
    plt.show()
