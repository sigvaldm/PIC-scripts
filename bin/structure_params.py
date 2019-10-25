#!/usr/bin/env python

import numpy as np
import sys

file = np.load(sys.argv[1])
lambds = file['lambds']
etas = -file['etas']
As = file['As']
Cs = file['Cs']
alphas = file['alphas']
deltas = file['deltas']

def unique(array, tol=1e-6):
    tmp = array.copy()
    tmp.sort()
    diff = np.append(10*tol, np.diff(tmp))
    res = tmp[diff>tol]
    return res

lambds_lin = unique(lambds)
etas_lin = unique(etas)

I, J = len(lambds_lin), len(etas_lin)
As_lin = np.zeros((I, J))
Cs_lin = np.zeros((I, J))
alphas_lin = np.zeros((I, J))
deltas_lin = np.zeros((I, J))

tol = 1e-6
for i, lambd in enumerate(lambds_lin):
    for j, eta in enumerate(etas_lin):
        ind_lambds = np.where(np.abs(lambds-lambd)<tol)[0]
        ind_etas   = np.where(np.abs(etas-eta)<tol)[0]
        ind = list(set(ind_lambds) & set(ind_etas))[0]

        As_lin[i, j] = As[ind]
        Cs_lin[i, j] = Cs[ind]
        alphas_lin[i, j] = alphas[ind]
        deltas_lin[i, j] = deltas[ind]

print(As_lin)
print(As_lin.shape)
print(etas_lin)

np.savez_compressed(sys.argv[2],
                    lambds=lambds_lin,
                    etas=etas_lin,
                    Cs=Cs_lin,
                    As=As_lin,
                    alphas=alphas_lin,
                    deltas=deltas_lin
                   )
