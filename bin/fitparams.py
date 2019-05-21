#!/usr/bin/env python
import numpy as np
import sys
import re
import os
from scipy.optimize import curve_fit, least_squares
from fitfuncs import *
from functools import partial
import matplotlib.pyplot as plt
from localreg import *

def h(zeta, alpha, gamma=1, delta=0):
    # return (zeta+delta)*np.exp(-alpha*zeta)
    # return ((zeta+delta)**gamma)*np.exp(-alpha*zeta)
    return ((zeta+delta)**gamma)*np.exp(-alpha*(zeta+delta))

def additive_model(lambd, zeta, C, A, alpha, B, beta, gamma, delta):
    delta = (1/alpha)-delta
    assert np.all(zeta>=0)
    assert np.all(lambd-zeta>=0)
    return C * (1 + A*h(zeta,       alpha, gamma, delta) \
                  + A*h(lambd-zeta, alpha, gamma, delta) \
                  + B*h(zeta,       beta,  gamma, delta) \
                  + B*h(lambd-zeta, beta,  gamma, delta) )

def sortkey(fname):
    l =   float(re.findall('[\d\.]+(?=mm)', fname)[-1])
    eta = float(re.findall('[\d\.]+(?=eta)', fname)[-1])
    return l*1000+eta

lambds = []
etas = []
p_opts = []


files = sys.argv[1:]
files.sort(key=sortkey, reverse=True)

print((9*"{:>5s}  ").format("l", "eta", "C", "A", "alpha", "B", "beta", "gamma", "delta"))
for path in files:
    r, l, n, eV, eta, lambd, debye = get_probe_params(path)
    zeta, g = get_facet_currents(path)

            #               C     A alpha     B  beta gamma delta
    p_lower = np.array([    0,    0,  0.1,    0,    1,    1,    0 ])
    p_upper = np.array([   10,   10,    2,    0,    1,    1, 10.0 ])

    for i in range(len(p_lower)):
        if p_lower[i]==p_upper[i]:
            p_upper[i] += 1e-6

    # Get initial guess from one step longer probe
    p_init = None
    p_init = p_lower
    where_eta = np.where(np.abs(np.array(etas)-eta)<1e-6)[0]
    lambds_at_eta  = np.array(lambds)[where_eta]
    if len(lambds_at_eta):
        ind = np.argmin(lambds_at_eta)
        ind = where_eta[ind]
        p_init = deepcopy(p_opts[ind])

    # SLOPE ON ALPHA FOR LOW L
    # If l <= 10 mm, use slope to infer b coefficient (alpha)
    # if l<11e-3:
    #     ind_20mm = np.where(np.abs(lambds_at_eta-20e-3/debye)<1e-6)[0][0]
    #     ind_30mm = np.where(np.abs(lambds_at_eta-30e-3/debye)<1e-6)[0][0]
    #     alpha_20mm = popts[where_eta[ind_20mm]][1]
    #     alpha_30mm = popts[where_eta[ind_30mm]][1]
    #     alpha_slope = (alpha_30mm-alpha_20mm)/(30e-3-20e-3)
    #     alpha_off = alpha_30mm-30e-3*alpha_slope
    #     alpha = alpha_slope*l+alpha_off
    #     print(alpha_20mm, alpha_30mm, alpha_slope, alpha_off, alpha)
    #     lower[1] = alpha
    #     upper[1] = alpha+1e-6
    #     p0[1] = alpha

    zeta_ = np.linspace(0, lambd, 5000)
    g_ = localreg(zeta, g, zeta_, kernel=gaussian, width=0.1, degree=2)

    bounded = ""
    model = partial(additive_model, lambd)
    fit_of_fit = False
    if fit_of_fit:
        zeta_fit = zeta_
        g_fit = g_
    else:
        zeta_fit = zeta
        g_fit = g

    zeta_bnd = 5
    frac_bnd = 0.5
    inds = np.where(np.logical_or(zeta_fit<zeta_bnd, zeta_fit>lambd-zeta_bnd))[0]
    n_bnd = len(inds)
    n_tot = len(zeta_fit)
    n_mid = n_tot-n_bnd
    w_bnd = max(frac_bnd/n_bnd, 1/n_tot)
    w_mid = (1-n_bnd*w_bnd)/n_mid if n_mid != 0 else w_bnd
    weights = w_mid*np.ones_like(zeta_fit)
    weights[inds] = w_bnd
    print(w_bnd, w_mid)
    sigma = 1/np.sqrt(weights)

    p_opt, p_cov = curve_fit(model, zeta_fit, g_fit, p0=p_init,
                             bounds=(p_lower, p_upper), sigma=sigma)

    p_err = np.sqrt(np.diag(p_cov))
    for po, pl, pu in zip(p_opt, p_lower, p_upper):
        if np.abs(pl-pu)>1e-5 and (np.abs(po-pu)<1e-6 or np.abs(po-pl)<1e-6):
            bounded = "<--- BOUNDED"
    print(("{:5.0f}  {:5.0f}"+7*"  {:5.2f}"+" {}").format(l*1e3, -eta, *p_opt, bounded))

    plt.plot(zeta, g, '+', markersize=0.1, color='gray')
    plt.plot(zeta_, g_)
    plt.plot(zeta, model(zeta, *p_opt))
    plt.show()

    lambds.append(lambd)
    etas.append(eta)
    p_opts.append(p_opt)

Cs, As, alphas, Bs, betas, gammas, deltas = zip(*p_opts)

np.savez_compressed('params.npz',
                    lambds=lambds,
                    etas=etas,
                    Cs=Cs,
                    As=As,
                    alphas=alphas,
                    Bs=Bs,
                    betas=betas,
                    gammas=gammas,
                    deltas=deltas
                   )
