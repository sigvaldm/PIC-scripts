"""
Various functions used by plotting scripts.
"""
import numpy as np
import matplotlib.pyplot as plt
import scipy.constants as constants
import os
import glob

def readHst(fname):
    """
    Reads an .hst-file given by the absolute or relative path in fname into a
    numpy array. If fname is a directory, all files matching *.hst in that
    directory is concatenated into the array in correct order. Lines starting
    with # is ignored.
    """

    if os.path.isdir(fname):
        pattern = os.path.join(fname,'*.hst')
        fnames = glob.glob(pattern)
    else:
        fnames = [fname]

    data = []
    for fname in fnames:
        f = open(fname)
        for l in f:
            l.strip()
            if len(l)>0 and l[0] != '#':
                data.append(l.split())
        f.close()
    data = np.array(data, dtype=float)
    data = data[data[:,0].argsort()]
    return data

def expAvg(data, dt, tau=0.1):
    """
    Makes an exponential moving average of "data". dt is the timestep between
    each sample in some unit and tau is the relaxation time in the same unit.
    """
    weight = 1-np.exp(-dt/tau)
    result = np.zeros(data.shape)
    result[0] = data[0]
    for i in range(1,len(data)):
        result[i] = weight*data[i] + (1-weight)*result[i-1]
    return result

def expAvg2(data, xaxis, tau=0.1):
    """
    Makes an exponential moving average of "data". dt is the timestep between
    each sample in some unit and tau is the relaxation time in the same unit.
    """
    result = np.zeros(data.shape)
    result[0] = data[0]
    for i in range(1,len(data)):
        weight = np.exp(-(xaxis[i]-xaxis[i-1])/tau)
        result[i] = weight*result[i-1] + (1-weight)*data[i]
    return result

def plotAvg(x, y, label=None, tau=0.1, linewidth=1):
    """
    Plots a moving exponential average of "y" versus "x" in a matplotlib plot
    while showing the raw values of "y" in the background. tau is the relaxation
    time in the same unit as the value on the x-axis.
    """
    dx = x[1]-x[0]

    if tau != 0.0:
        plt.plot(x, y, '#CCCCCC', linewidth=1, zorder=0)

    p = plt.plot(x, expAvg(y, dx, tau), linewidth=linewidth, label=label)

    # returning this allows color to be extracted
    return p

def plotAvg2(x, y, label=None, tau=0.1, linewidth=1):
    """
    Plots a moving exponential average of "y" versus "x" in a matplotlib plot
    while showing the raw values of "y" in the background. tau is the relaxation
    time in the same unit as the value on the x-axis.
    """
    if tau != 0.0:
        plt.plot(x, y, '#CCCCCC', linewidth=1, zorder=0)

    p = plt.plot(x, expAvg2(y, x, tau), linewidth=linewidth, label=label)

    # returning this allows color to be extracted
    return p

def OML_cylinder(V=2.2, l=25e-3, r=0.255e-3, n=1.66e11, T=750):
    """
    Returns the collected current [A] according to OML theory of a cylinder
    with:
        V - Probe bias voltage [V]
        l - Probe length [m]
        r - Probe radius [m]
        n - Plasma density [m^(-3)]
        T - Plasma temperature [K]
    """
    e  = constants.value('elementary charge')
    me = constants.value('electron mass')
    k  = constants.value('Boltzmann constant')
    current = -n*e*np.sqrt(k*T/(2*np.pi*me))*2*np.pi*r*np.sqrt(1+e*V/(k*T))*l
    return current
