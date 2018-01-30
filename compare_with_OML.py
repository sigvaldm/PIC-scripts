#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
from funcs import *

per_25mm = True

prefix = "Run13"
lengths = np.array([25, 50, 100])
voltages = np.array([2.5, 4.0, 5.5, 7.0])
variants = ['']

# Physical constants
kB = 1.38064852e-23 # J/K
me = 9.10938188e-31 # kg
e  = 1.60217733e-19 # C

# Parameters
n = 1.66e11  # m^(-3)
T = 750      # K
r = 0.255e-3 # m

V = np.linspace(0,8,100)
I = n*e*np.sqrt(kB*T/(2*np.pi*me))*2*np.pi*r*np.sqrt(1+e*V/(kB*T))*1e6
if per_25mm: I *= 25e-3

plt.plot(V, I, label='OML theory')
plt.grid()
plt.title('Comparison of simulations and OML theory')
plt.xlabel('Voltage [V]')
if per_25mm:
    plt.ylabel('Current [$\mathrm{\mu A/25 mm}$]')
else:
    plt.ylabel('Current [$\mathrm{\mu A/m}$]')

for length in lengths:

    if length==100:
        voltages = np.array([7.0])
        variants = ['Vbiased','Ibiased']

    currents = np.zeros(voltages.shape)

    for v in variants:
        if v != '': v='_'+v

        for i, voltage in enumerate(voltages):
            path = prefix+'_'+str(length)+'mm_'+str(voltage)+'V'+v+'/pictetra.hst'
            print(path)
            data = readHst(path)
            dt = data[1,1]-data[0,1]
            current_raw = data[:,26]+data[:,29]+data[:,32]+data[:,35]+data[:,38]+data[:,41]
            currents[i] = -expAvg(current_raw, dt)[-1]*1e6/(length*1e-3)

        if per_25mm: currents *= 25e-3

        label = str(length)+' mm '+v
        plt.plot(voltages, currents, 'o', label=label)

plt.legend(loc='upper left')
plt.show()

