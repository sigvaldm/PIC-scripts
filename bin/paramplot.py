#!/usr/bin/env python

import matplotlib as mp

mp.rc('text', usetex=True)
mp.rc('font', family='serif', size=8)
mp.rc('axes', titlesize=8)
mp.rc('axes', labelsize=8)
mp.rc('xtick', labelsize=8)
mp.rc('ytick', labelsize=8)
mp.rc('legend', fontsize=8)
mp.rc('figure', titlesize=8)

from mpl_toolkits.axes_grid1.inset_locator import inset_axes

import numpy as np
import sys
import re
import os
import matplotlib.pyplot as plt

pretty = False
if '-p' in sys.argv:
    sys.argv.remove('-p')
    pretty = True

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

symbols = {'As': 'A',
           'Cs': 'C',
           'alphas': '$\\alpha$',
           'deltas': '$\\delta$'}

lw = 0.8

if pretty:

    figwidth = 85*2
    figheight = 85*2/1.618
    dpi = 300

    # fig = plt.figure(constrained_layout = True)
    fig = plt.figure(figsize=(figwidth/25.4, figheight/25.4), constrained_layout=True, dpi=dpi)
    gs = mp.gridspec.GridSpec(2, 2, figure=fig)
    axs = []
    axinss = []

for i, coeff_name in enumerate(coeffs):
    coeff = coeffs[coeff_name]

    if pretty:
        axs.append(fig.add_subplot(gs[i//2, i%2]))
        ax = axs[-1]
        if coeff_name in ('Cs', 'alphas'):
            axins = inset_axes(ax, width="100%", height="100%",
                               bbox_to_anchor=(0.5, 0.4, 0.48, 0.55),
                               bbox_transform=ax.transAxes)
    else:
        fig = plt.figure()
        ax = fig.gca()

    for num, eta in enumerate(np.unique(etas)):
        eta_inds = np.where(np.abs(etas-eta)<tol)[0]
        lambds_at_eta = lambds[eta_inds]
        lambds_at_eta.sort()

        value = []
        for lambd in lambds_at_eta:
            l_inds = np.where(np.abs(lambds-lambd)<tol)[0]
            ind = [i for i in l_inds if i in eta_inds][0]
            value.append(coeff[ind])

        color = 0.7*(num/len(np.unique(etas)))
        color *= np.array([1., 1., 1.])

        ax.semilogx(lambds_at_eta, value, color=color,
                 label='$\eta={:.0f}$'.format(-eta), linewidth=lw)

        if pretty and coeff_name in ('Cs', 'alphas'):
            axins.semilogx(lambds_at_eta, value, color=color, linewidth=lw)
            if coeff_name=='Cs':
                axins.set_xlim([50, 600])
                axins.set_ylim([1, 1.10])
            if coeff_name=='alphas':
                axins.set_xlim([5, 600])
                axins.set_ylim([0.5, 1.5])

    # ax.grid()
    ax.set_ylabel('{}'.format(symbols.get(coeff_name, coeff_name)))
    ax.set_xlabel('$\lambda$')

    if pretty:
        if i==0:
            ax.legend(bbox_to_anchor=(0., 1.05, 2.210, .102), loc=3,
                      ncol=9, mode="expand", borderaxespad=0.)
    else:
        ax.legend()


# plt.show()
fig.savefig('coeff.png')
plt.show()
