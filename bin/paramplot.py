#!/usr/bin/env python
import numpy as np
import sys
import re
import os
import matplotlib.pyplot as plt

file = np.load(sys.argv[1])
coeffs = dict()

lambds = file['lambds'] if 'lambds' in file else file['ls']
etas = file['etas']

if 'popts' in file:
    coeffs['As'] = file['popts'][:,0]
    coeffs['alphas'] = file['popts'][:,1]
    coeffs['Bs'] = file['popts'][:,2]
    coeffs['betas'] = file['popts'][:,3]
    coeffs['gammas'] = file['popts'][:,4]
    coeffs['C'] = file['popts'][:,5]
else:
    for coeff_name in file:
        if not coeff_name in ('etas', 'ls', 'lambds'):
            coeffs[coeff_name] = file[coeff_name]

tol = 1e-6

for coeff_name in coeffs:
    coeff = coeffs[coeff_name]
    plt.figure()

    for num, eta in enumerate(np.unique(etas)):
        eta_inds = np.where(np.abs(etas-eta)<tol)[0]
        lambds_at_eta = lambds[eta_inds]
        lambds_at_eta.sort()

        value = []
        for lambd in lambds_at_eta:
            l_inds = np.where(np.abs(lambds-lambd)<tol)[0]
            ind = [i for i in l_inds if i in eta_inds][0]
            value.append(coeff[ind])

        color = 0.7*(1-num/len(np.unique(etas)))
        color *= np.array([1., 1., 1.])

        plt.plot(lambds_at_eta, value, color=color,
                 label='$\eta={:.0f}$'.format(-eta))

    plt.grid()
    plt.legend()
    plt.title('{}'.format(coeff_name))
    plt.xlabel('Length [$\lambda$]')
    plt.ylabel('Value')

plt.show()
