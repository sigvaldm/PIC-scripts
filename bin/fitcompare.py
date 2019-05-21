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
from localreg import *
import glob

file = sys.argv[1]

r, l, n, eV, eta, lambd, debye = get_probe_params(file)

elec = Species(n=n, eV=eV)
geo = Cylinder(r, l)
I_OML = OML_current(Cylinder(r, 1), elec, eta=eta)

sccfiles = glob.glob(os.path.join(file, 'scc*.vtk'))
sccfiles.sort()
zeta_centroids, facet_currents = get_facet_currents(sccfiles[-1])
zeta = np.arange(0, lambd+0.01, 0.1)
I = localreg(zeta_centroids, facet_currents, zeta, degree=2, kernel=gaussian, width=0.1)
plt.plot(zeta, I, label='localreg')

I_fit = finite_length_current(geo, elec, eta=eta)
I_sim = np.average(facet_currents)*l*I_OML

print("OML        {:.4e} A".format(I_OML*l))
print("Simulated  {:.4e} A".format(I_sim))
print("Curve fit  {:.4e} A".format(I_fit))
print("Error (simulated vs curve fit) {:.2f}%".format(100*(I_sim-I_fit)/I_sim))

zeta = np.linspace(0, lambd, int(1e4))

if len(sys.argv)>2:
    params = np.load(sys.argv[2])

    lambds = params['lambds']
    etas = params['etas']

    # Index of this probe length and voltage
    where_lambd = np.where(np.abs(np.array(lambds)-lambd)<1e-3)[0]
    where_eta = np.where(np.abs(np.array(etas)-eta)<1e-3)[0]
    ind = [a for a in where_lambd if a in where_eta][0]

    A = params['As'][ind]
    B = params['Bs'][ind]
    C = params['Cs'][ind]
    alpha = params['alphas'][ind]
    beta = params['betas'][ind]
    gamma = params['gammas'][ind]
    delta = params['deltas'][ind]
    print(delta)

    i = additive_model(lambd, zeta, C, A, alpha, B, beta, gamma, delta)
    plt.plot(zeta, i, label=sys.argv[2])

i = finite_length_current_density(geo, elec, eta=eta, zeta=zeta, normalize='OML')
plt.plot(zeta, i, label='Langmuir')
plt.xlabel('$z/\lambda_D$')
plt.ylabel('$I/I_{OML}$')
plt.legend()
plt.title('Current for $l/\lambda_D={:.1f}$ and $qV/kT={:.0f}$'.format(lambd,eta))
plt.show()
