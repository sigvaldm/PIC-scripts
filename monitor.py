#!/usr/bin/env python

# Live monitoring of simulation results. Run simulations, and run
# ./monitor.py
#

from __future__ import print_function, division
import sys
if sys.version_info.major == 2:
    from itertools import izip as zip
    range = xrange

import numpy as np
import matplotlib.pyplot as plt
import time
import sys
from funcs import *

# Physical constants
kB = 1.38064852e-23 # J/K
me = 9.10938188e-31 # kg
e  = 1.60217733e-19 # C

# Parameters
n = 1.66e11  # m^(-3)
T = 750      # K
r = 0.255e-3 # m
l = 25e-3    # m

data = readHst(sys.argv[1])

dt = data[1,1]-data[0,1]
data[:,1] *= 1e6 # time in us
data[:,8::3] *= 1e6 # curents in uA
xaxis = data[:,1]

tau = 0.1e-6

def plotAvg(x, y, label=None):
    plt.plot(x, y, '#CCCCCC', linewidth=1, zorder=0)
    plt.plot(x, expAvg(y, dt, tau), linewidth=1, label=label) 

current = data[:,26]+data[:,29]+data[:,32]+data[:,35]+data[:,38]+data[:,41]

V = expAvg(data[:,24],dt,tau)[-1]
Ioml = -n*e*np.sqrt(kB*T/(2*np.pi*me))*2*np.pi*r*np.sqrt(1+e*V/(kB*T))*1e6*l
I = expAvg(current,dt,tau)[-1]
print("Steady state voltage:", V, "V")
print("OML current:", Ioml, "uA")
print("Steady state current:", I, "uA (",100*I/Ioml ,"%)")


fig = plt.figure(1)
ax1 = fig.add_subplot(111)

plotAvg(xaxis, data[:,26], 'segment 1')
plotAvg(xaxis, data[:,29], 'segment 2')
plotAvg(xaxis, data[:,32], 'segment 3')
plotAvg(xaxis, data[:,35], 'segment 4')
plotAvg(xaxis, data[:,38], 'segment 5')
plotAvg(xaxis, data[:,20], 'insulator (cylindrical part)')
plotAvg(xaxis, data[:,23], 'insulator (annular part)')
plotAvg(xaxis, data[:,32], 'end cap')
plotAvg(xaxis, current   , 'total')

plt.grid()
# ax2 = ax1.twiny()
# ax1.set_xlabel('Time [us]')
# ax2.set_xlabel('Timestep')


plt.legend(loc="lower right")
plt.xlabel("Time [us]")
plt.ylabel("Current [$\mathrm{\mu A}$]")
plt.title("Probe Section Current")

fig = plt.figure(2)
ax1 = fig.add_subplot(111)
plt.plot(xaxis, data[:,2], linewidth=1, label='Electrons')
plt.plot(xaxis, data[:,3], linewidth=1, label='Ions')
plt.ylabel("Number of particles")
plt.title("Number of particles in simulation domain")
plt.legend(loc="lower right")

fig = plt.figure(3)
ax1 = fig.add_subplot(111)
plotAvg(xaxis, data[:,24])
plt.ylabel("Potential [V]")
plt.title("Probe Potential")

plt.show()
