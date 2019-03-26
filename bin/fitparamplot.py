#!/usr/bin/env python
import numpy as np
import sys
import re
import os
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from fitfuncs import *
from mpl_toolkits.mplot3d import Axes3D # This import has side effects required for the kwarg projection='3d' in the call to fig.add_subplot

def func(z, a, b, c, d, e):
    return (a*np.exp(-b*z)+c*np.exp(-d*z))*(z**e)+1

def gunc(xdata, a, b, c, d, e, f):
# def gunc(xdata, a, b, e, f):
#     c, d = 0, 1
    z, l, eta = xdata
    res = f*func(z, a, b, c, d, e)*func(l-z, a, b, c, d, e)
    return res

ls = []
etas = []
popts = []

if '.npz' in sys.argv[1]:
    file = np.load(sys.argv[1])
    ls = file['ls']
    etas = file['etas']
    popts = file['popts']

else:
    for path in sys.argv[1:]:
        print(path)
        path = os.path.abspath(path)
        l    =  float(re.findall('[\d\.]+(?=mm)' , path)[-1])*1e-3
        n    =  float(re.findall('[\d\.]+(?=n)'  , path)[-1])*1e10
        eV   =  float(re.findall('[\d\.]+(?=eV)' , path)[-1])
        eta  = -float(re.findall('[\d\.]+(?=eta)', path)[-1])

        xdata, ydata = get_data(path)

        lower = ( 0     , 0     , 0     , 0     ,  0     , 0     )
        upper = ( 10    , 10    , 10    , 0.2   ,  10    , 10    )
        defpopt = [0,0,0,0,0,0]

        # lower = ( 0     , 0     ,  0     , 0     )
        # upper = ( 10    , 10    ,  10    , 10    )
        # defpopt = [0,0,0,0]

        try:
            popt, pcov = curve_fit(gunc, xdata, ydata, bounds=(lower, upper))
            perr = np.sqrt(np.diag(pcov))
            print("Popt", popt)
        except:
            popt = defpopt
            print("Popt not found")

        # ls.append(l)
        # etas.append(eta)
        # popts.append([0, 1, 2])

        ls.append(xdata[1,0])
        etas.append(xdata[2,0])
        popts.append(popt)

    ls = np.array(ls)
    etas = np.array(etas)
    popts = np.array(popts)

    np.savez_compressed('cache.npz', ls=ls, etas=etas, popts=popts)

fig = plt.figure()
for i in range(popts.shape[1]):
    ax = fig.add_subplot(231+i, projection='3d')
    ax.plot_trisurf(ls, etas, popts[:,i])
    plt.xlabel('l')
    plt.ylabel('eta')
    plt.title(list('abcdef')[i])
plt.show()
