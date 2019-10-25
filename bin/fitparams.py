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
from subprocess import call

def h(zeta, alpha, gamma=1, delta=0):
    # return (zeta+delta)*np.exp(-alpha*zeta)
    return ((zeta+delta)**gamma)*np.exp(-alpha*zeta)
    # return ((zeta+delta)**gamma)*np.exp(-alpha*(zeta+delta))

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

fit_of_fit = False
inspect = len(files)==1
use_longer = False
use_slope = True
use_delta = True
add_eta_zero = True

print((6*"{:>5s}  ").format("l", "eta", "C", "A", "alpha", "delta"))
for path in files:
    r, l, n, eV, eta, lambd, debye = get_probe_params(path)
    zeta, g = get_facet_currents(path)

            #               C     A alpha     B  beta gamma delta
    p_lower = np.array([    0,    0,  0.1,    0,    1,    1,    0 ])
    p_upper = np.array([   10,   10,    2,    0,    1,    1, 10.0 ])
    p_lower = np.array([    0,0.001, 0.01,                    0.0 ])
    p_upper = np.array([   10,   10,    3,                    2.0 ])

    if l<19e-3: p_upper[2]=30

    for i in range(len(p_lower)):
        if p_lower[i]==p_upper[i]:
            p_upper[i] += 1e-6

    p_init = None
    p_init = (p_lower+p_upper)/3
    # p_init = (4*p_lower+1*p_upper)/5

    where_eta = np.where(np.abs(np.array(etas)-eta)<1e-6)[0]
    lambds_at_eta  = np.array(lambds)[where_eta]

    # Get initial guess from one step longer probe
    if use_longer:
        if len(lambds_at_eta):
            ind = np.argmin(lambds_at_eta)
            ind = where_eta[ind]
            p_init = deepcopy(p_opts[ind])

    # SLOPE ON ALPHA FOR LOW L
    # If l <= 10 mm, use slope to infer alpha
    if use_slope:
        if l<11e-3:
            ind_20mm = np.where(np.abs(lambds_at_eta-20e-3/debye)<1e-6)[0][0]
            ind_30mm = np.where(np.abs(lambds_at_eta-30e-3/debye)<1e-6)[0][0]

            # p_upper[2] = 50

            # C_20mm = p_opts[where_eta[ind_20mm]][0]
            # C_30mm = p_opts[where_eta[ind_30mm]][0]
            # C_slope = (C_30mm-C_20mm)/(30e-3-20e-3)
            # C_off = C_30mm-30e-3*C_slope
            # C = C_slope*l+C_off
            # p_lower[0] = C
            # p_upper[0] = C+1e-6
            # p_init[0]  = C

            # p_lower[3] = -10
            # p_upper[3] = 2.5

            # A_20mm = p_opts[where_eta[ind_20mm]][1]
            # A_30mm = p_opts[where_eta[ind_30mm]][1]
            # A_slope = (A_30mm-A_20mm)/(30e-3-20e-3)
            # A_off = A_30mm-30e-3*A_slope
            # A = A_slope*l+A_off
            # p_lower[1] = A
            # p_upper[1] = A+1e-6
            # p_init[1]  = A

            alpha_20mm = p_opts[where_eta[ind_20mm]][2]
            alpha_30mm = p_opts[where_eta[ind_30mm]][2]
            alpha_slope = (alpha_30mm-alpha_20mm)/(30e-3-20e-3)
            alpha_off = alpha_30mm-30e-3*alpha_slope
            alpha = alpha_slope*l+alpha_off
            p_lower[2] = alpha
            p_upper[2] = alpha+1e-6
            p_init[2]  = alpha

            # delta_20mm = p_opts[where_eta[ind_20mm]][3]
            # delta_30mm = p_opts[where_eta[ind_30mm]][3]
            # delta_slope = (delta_30mm-delta_20mm)/(30e-3-20e-3)
            # delta_off = delta_30mm-30e-3*delta_slope
            # delta = delta_slope*l+delta_off
            # p_lower[3] = delta
            # p_upper[3] = delta+1e-6
            # p_init[3]  = delta

            # inspect=True

    if use_delta:
        if l<6e-3:
            ind = np.argmin(lambds_at_eta)
            ind = where_eta[ind]

            p_lower[2] = p_opts[ind][2]*0.8
            p_upper[2] = p_opts[ind][2]*1.2
            p_init[2]  = p_opts[ind][2]

            # inspect=True

    if np.abs(l-5e-3)<1e-4:
        p_upper[1] = 0.5
        p_init[1] = 0.1

    # if np.abs(l-5e-3)<1e-4 and np.abs(eta+100)<1e-4:
    #     p_lower[0] = 8
    #     p_upper[0] = 12
    #     p_init[0]  = 9.11
    #     # p_lower[2] = 1
    #     # p_upper[2] = 2
    #     # p_init[2] = 1.5
    #     p_upper[3] = 3

    # if np.abs(l-2e-3)<1e-4:
    #     p_lower[1] = 0
    #     p_upper[1] = 1e-6
    #     p_init[1] = 0
    #     p_lower[3] = -1

    if inspect or fit_of_fit:
        zeta_ = np.linspace(0, lambd, 5000)
        g_ = localreg(zeta, g, zeta_, kernel=gaussian, width=0.1, degree=2)

    bounded = ""
    model = partial(additive_model, lambd)
    model = lambda zeta, C, A, alpha, delta: additive_model(lambd, zeta, C, A, alpha, 0, 1, 1, delta)
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
    sigma = 1/np.sqrt(weights)

    p_opt, p_cov = curve_fit(model, zeta_fit, g_fit, p0=p_init,
                             bounds=(p_lower, p_upper), sigma=sigma, maxfev=5000)

    p_err = np.sqrt(np.diag(p_cov))
    for po, pl, pu in zip(p_opt, p_lower, p_upper):
        if np.abs(pl-pu)>1e-5 and (np.abs(po-pu)<1e-2 or np.abs(po-pl)<1e-2):
            bounded = "<--- BOUNDED"
    print(("{:5.0f}  {:5.0f}"+len(p_opt)*"  {:5.2f}"+" {}").format(l*1e3, -eta, *p_opt, bounded))

    if inspect:
        plt.plot(zeta, g, '+', markersize=0.1, color='gray')
        plt.plot(zeta_, g_)
        plt.plot(zeta, model(zeta, *p_opt))
        plt.show()

    lambds.append(lambd)
    etas.append(eta)
    p_opts.append(p_opt)

if add_eta_zero:
    all_lambds = np.array(lambds)
    all_lambds.sort()
    diffs = deepcopy(all_lambds)
    diffs[1:] -= diffs[:-1]
    diffs[0] = 1
    unique_lambd_inds = np.where(np.abs(diffs)>1e-3)[0]
    unique_lambds = all_lambds[unique_lambd_inds]

    for lambd in unique_lambds:
        where_lambd = np.where(np.abs(np.array(lambds)-lambd)<1e-6)[0]
        etas_at_lambd = np.array(etas)[where_lambd]
        ind = np.argmin(np.abs(etas_at_lambd))
        ind = where_lambd[ind]

        lambds.append(lambd)
        etas.append(0)
        alpha = p_opts[ind][2]
        delta = p_opts[ind][3]
        p_opts.append([1, 0, alpha, delta])

# Cs, As, alphas, Bs, betas, gammas, deltas = zip(*p_opts)
Cs, As, alphas, deltas = zip(*p_opts)

np.savez_compressed('params.npz',
                    lambds=lambds,
                    etas=etas,
                    Cs=Cs,
                    As=As,
                    alphas=alphas,
                    # Bs=Bs,
                    # betas=betas,
                    # gammas=gammas,
                    deltas=deltas
                   )

if not inspect:
    call(["espeak", "curve fits complete"])
