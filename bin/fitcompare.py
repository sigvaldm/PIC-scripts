#!/usr/bin/env python
import numpy as np
import meshio
import sys
import os
import re
import langmuir
import metaplot as mpl
import matplotlib.pyplot as plt
from fitfuncs import *
import scipy.integrate as integrate

paramfile = np.load(sys.argv[1])
file = sys.argv[2]

r, l, n, eV, eta = get_probe_params(file)

elec = Species(n=n, eV=eV)
I_OML = OML_current(Cylinder(r, 1), elec, eta=eta)
debye = elec.debye
l /= debye

df = mpl.DataFrame(file)
Zn = df['Zn'].m
f = df['f'].m
g = df['g'].m
i = df['I'].m
z = df['z'].m

ls = paramfile['ls']
etas = paramfile['etas']
popts = paramfile['popts']
where_l = np.where(np.abs(np.array(ls)-l)<1e-3)[0]
where_eta = np.where(np.abs(np.array(etas)-eta)<1e-3)[0]
ind = [a for a in where_l if a in where_eta][0]
popt = popts[ind]

I_fit = I_OML * debye * (int_additive_model(l, l, *popt)
                        -int_additive_model(0, l, *popt))

dz = z[1]-z[0]
I_sim = np.sum(i)*dz

I_quad = integrate.quad(lambda z: additive_model(z, l, *popt), 0, l)[0]
I_quad *= I_OML * debye

print("dz         {:.2e} m".format(dz))
print("l          {:.2e} m".format(l))
print("")
print("OML        {:.2e} A/m".format(I_OML))
print("Simulated  {:.2e} A/m".format(i[int(len(i)/2)]))
print("")
print("OML        {:.4e} A".format(I_OML*l*debye))
print("Simulated  {:.4e} A".format(I_sim))
print("Quadrature {:.4e} A".format(I_quad))
print("Curve fit  {:.4e} A".format(I_fit))
print("Error (simulated vs curve fit) {:.2f}%".format(100*(I_sim-I_fit)/I_sim))

Zinterp = np.linspace(0, l, int(1e4))
plt.plot(Zn, g, label='Simulated current')
plt.plot(Zinterp, additive_model(Zinterp, l, *popt), label='Curve fit')
plt.xlabel('$z/\lambda_D$')
plt.ylabel('$I/I_{OML}$')
plt.legend()
plt.title('Current for $l/\lambda_D={:.1f}$ and $qV/kT={:.0f}$'.format(l,eta))
plt.show()
