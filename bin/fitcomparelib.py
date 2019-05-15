#!/usr/bin/env python
import numpy as np
import meshio
import sys
import os
import re
import metaplot as mpl
import matplotlib.pyplot as plt
from fitfuncs import *
import scipy.integrate as integrate

file = sys.argv[1]

r, l, n, eV, eta = get_probe_params(file)

elec = Species(n=n, eV=eV)
geo = Cylinder(r, l)
I_OML = OML_current(Cylinder(r, 1), elec, eta=eta)
debye = elec.debye
lambd = l / debye

df = mpl.DataFrame(file)
zeta = df['Zn'].m
g = df['g'].m
i = df['I'].m
z = df['z'].m

I_fit = finite_length_current(geo, elec, eta=eta)

dz = z[1]-z[0]
I_sim = np.sum(i)*dz

print("dz         {:.2e} m".format(dz))
print("")
print("OML        {:.2e} A/m".format(I_OML))
print("Simulated  {:.2e} A/m".format(i[int(len(i)/2)]))
print("")
print("OML        {:.4e} A".format(I_OML*l))
print("Simulated  {:.4e} A".format(I_sim))
print("Curve fit  {:.4e} A".format(I_fit))
print("Error (simulated vs curve fit) {:.2f}%".format(100*(I_sim-I_fit)/I_sim))

Zinterp = np.linspace(0, lambd, int(1e4))
i = finite_length_current_density(geo, elec, eta=eta, zeta=Zinterp, normalize='OML')
plt.plot(zeta, g, label='Simulated current')
plt.plot(Zinterp, i, label='Curve fit')
plt.xlabel('$z/\lambda_D$')
plt.ylabel('$I/I_{OML}$')
plt.legend()
plt.title('Current for $l/\lambda_D={:.1f}$ and $qV/kT={:.0f}$'.format(lambd,eta))
plt.show()
