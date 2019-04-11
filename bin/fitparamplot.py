#!/usr/bin/env python
import numpy as np
import sys
import re
import os
from scipy.optimize import curve_fit, least_squares
import matplotlib.pyplot as plt
from fitfuncs import *
from mpl_toolkits.mplot3d import Axes3D # This import has side effects required for the kwarg projection='3d' in the call to fig.add_subplot

def func(z, a, b, c, d, e):
    return (a*np.exp(-b*z)+c*np.exp(-d*z))*(z**e)+1

def gunc(xdata, a, b, c, d, e, f):
# def gunc(xdata, a, b, e, f):
#     c, d = 0, 1
    z, l, eta = xdata
    res = f*func(z, a, b, c, d, e)*func(l-z, a, b, c, d, e)
    return res

gunc4 = lambda xdata, a, b, e, f: gunc(xdata, a, b, 0, 0, e, f)

def additive_func(z, a, b, c, d, e):
    return (a*np.exp(-b*z)+c*np.exp(-d*z))*z**e

def additive_gunc(xdata, a, b, c, d, e, f):
    z, l, eta = xdata
    return f + additive_func(z, a, b, c, d, e) + additive_func(l-z, a, b, c, d, e)

def additive_gunc_reduced(xdata, a, b, e, f):
    c, d = 0, 1
    return additive_gunc(xdata, a, b, c, d, e, f)

def residual(params, xdata, ydata):
    # a, b, c, d, e, f = params
    # res = gunc(xdata, *params)-ydata
    res = gunc4(xdata, *params)-ydata
    # print(res)
    return res

def loss(x):
    return x

def probelen(fname):
    l = float(re.findall('[\d\.]+(?=mm)', fname)[-1])*1e-3
    return l

ls = []
etas = []
popts = []

if '.npz' in sys.argv[1]:
    file = np.load(sys.argv[1])
    ls = file['ls']
    etas = file['etas']
    popts = file['popts']

else:

    files = sys.argv[1:]
    files.sort(key=probelen, reverse=True)

    for path in files:
        print(path)
        path = os.path.abspath(path)
        l    =  float(re.findall('[\d\.]+(?=mm)' , path)[-1])*1e-3
        n    =  float(re.findall('[\d\.]+(?=n)'  , path)[-1])*1e10
        eV   =  float(re.findall('[\d\.]+(?=eV)' , path)[-1])
        eta  = -float(re.findall('[\d\.]+(?=eta)', path)[-1])

        if True: #l>3e-3 and l<300e-3:

            xdata, ydata = get_data(path)

            debye = l/xdata[1,0]

            # ORIGINAL METHOD, SKIP THE FEW THAT DOESN'T WORK
            # """
            myfunc = additive_gunc
            lower = [ 0     , 0     , 0     , 0     ,  0     , 1     ]
            upper = [ 10    , 10    , 10    , 0.2   ,  10    , 10    ]
            defpopt = [0,0,0,0,0,0]

            # myfunc = additive_gunc_reduced
            # lower = [ 0     , 0     ,  0     , 0     ]
            # upper = [ 10    , 10    ,  10    , 10    ]
            # defpopt = [0,0,0,0]

            p0 = None

            # Get initial guess from one step longer probe
            where_etas = np.where(np.abs(np.array(etas)-eta)<1e-6)[0]
            ls_at_eta  = np.array(ls)[where_etas]
            if len(ls_at_eta):
                ind = np.argmin(ls_at_eta)
                ind = where_etas[ind]
                p0 = deepcopy(popts[ind])

            # SLOPE ON ALPHA FOR LOW L
            # If l <= 10 mm, use slope to infer b coefficient (alpha)
            if l<11e-3:
                ind_20mm = np.where(np.abs(ls_at_eta-20e-3/debye)<1e-6)[0][0]
                ind_30mm = np.where(np.abs(ls_at_eta-30e-3/debye)<1e-6)[0][0]
                alpha_20mm = popts[where_etas[ind_20mm]][1]
                alpha_30mm = popts[where_etas[ind_30mm]][1]
                alpha_slope = (alpha_30mm-alpha_20mm)/(30e-3-20e-3)
                alpha_off = alpha_30mm-30e-3*alpha_slope
                alpha = alpha_slope*l+alpha_off
                print(alpha_20mm, alpha_30mm, alpha_slope, alpha_off, alpha)
                lower[1] = alpha
                upper[1] = alpha+1e-6
                p0[1] = alpha

            # SLOPE ON BETA FOR LOW L
            # if l<11e-3:
            #     ind_20mm = np.where(np.abs(ls_at_eta-20e-3/debye)<1e-6)[0][0]
            #     ind_30mm = np.where(np.abs(ls_at_eta-30e-3/debye)<1e-6)[0][0]
            #     beta_20mm = popts[where_etas[ind_20mm]][3]
            #     beta_30mm = popts[where_etas[ind_30mm]][3]
            #     beta_slope = (beta_30mm-beta_20mm)/(30e-3-20e-3)
            #     beta_off = beta_30mm-30e-3*beta_slope
            #     beta = beta_slope*l+beta_off
            #     print(beta_20mm, beta_30mm, beta_slope, beta_off, beta)
            #     lower[3] = beta
            #     upper[3] = beta+1e-6
            #     p0[3] = beta

            # BETA AND B INDEPENDENT OF L
            # if l<1999e-3:
            #     ind_2000mm = np.where(np.abs(ls_at_eta-2000e-3/debye)<1e-4)[0][0]
            #     B = popts[where_etas[ind_2000mm]][2]
            #     beta = popts[where_etas[ind_2000mm]][3]
            #     lower[2] = B-1e-6
            #     upper[2] = B+1e-6
            #     p0[2] = B
            #     lower[3] = beta-1e-6
            #     upper[3] = beta+1e-6
            #     p0[3] = beta

            # NO BETA-TERM
            lower[2] = -1e-6
            upper[2] = 1e-6
            lower[3] = 1-1e-6
            upper[3] = 1+1e-6
            # p0[2] = 0
            # p0[3] = 1

            # try:
            popt, pcov = curve_fit(myfunc,
                                   xdata, ydata, p0=p0, bounds=(lower, upper))
            perr = np.sqrt(np.diag(pcov))
            print("Popt", popt)
            # print("Pcov", pcov)
            # except:
            #     popt = defpopt
            #     print("Popt not found")
            # """

            # UNSUCCESSFUL ATTEMPT OF USING MIXED 4 OR 6 PARAMETERS
            """
            lower = ( 0     , 0     , 0     , 0     ,  0     , 0     )
            upper = ( 10    , 10    , 10    , 0.2   ,  10    , 10    )
            popt, pcov = curve_fit(gunc, xdata, ydata, bounds=(lower, upper))
            # perr = np.sqrt(np.diag(pcov))

            usefour = np.max(pcov)>1
            if usefour:
                lower = ( 0     , 0     ,  0     , 0     )
                upper = ( 10    , 10    ,  10    , 10    )
                popt, pcov = curve_fit(gunc4, xdata, ydata, bounds=(lower, upper))
                perr = np.sqrt(np.diag(pcov))
                popt = [popt[0], popt[1], 0, 0, popt[2], popt[3]]

            print("Popt", popt, usefour)
            """

            # REGULARIZATION
            # params0 = [1.732,1,0,0,1,1]
            # params0 = [1.732,1,1,1]
            # res = least_squares(residual, params0, loss=loss, args=(xdata, ydata))
            # popt = res.x
            # print("Popt", popt)

            # ls.append(l)
            # etas.append(eta)
            # popts.append([0, 1, 2])

            ls.append(xdata[1,0])
            etas.append(xdata[2,0])
            popts.append(popt)

    ls = np.array(ls)
    etas = np.array(etas)
    popts = np.array(popts)

    np.savez_compressed('cache.npz', ls=ls, etas=etas, popts=popts)

fig = plt.figure()
for i in range(popts.shape[1]):
    ax = fig.add_subplot(231+i, projection='3d')
    ax.plot_trisurf(ls, etas, popts[:,i])
    plt.xlabel('l')
    plt.ylabel('eta')
    plt.title(list('abcdef')[i])
plt.show()
