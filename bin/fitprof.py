#!/usr/bin/env python

import sys
import metaplot as mpl
import numpy as np
import os
import re
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from matplotlib import rc
import langmuir

fnin  = os.path.abspath(sys.argv[1])

# Read file and path-encoded info
l    =  float(re.findall('[\d\.]+(?=mm)' , fnin)[-1])*1e-3
n    =  float(re.findall('[\d\.]+(?=n)'  , fnin)[-1])*1e10
eV   =  float(re.findall('[\d\.]+(?=eV)' , fnin)[-1])
eta  = -float(re.findall('[\d\.]+(?=eta)', fnin)[-1])
print('l={}, n={}, eV={}, eta={}'.format(l, n, eV, eta))

debye = langmuir.Species(n=n, eV=eV).debye
l /= debye

df = mpl.DataFrame(fnin)
Zn = df['Zn'].m
f = df['f'].m
g = df['g'].m

def func(z, a, b, c, d, e):
    return (a*np.exp(-b*z)+c*np.exp(-d*z))*(z**e)+1 # Great success!

def gunc(z, a, b, c, d, e, f):
    return f*func(z, a, b, c, d, e)*func(l-z, a, b, c, d, e)

def gunc_reduced(z, a, b, e, f):
    c, d = 0, 1
    return f*func(z, a, b, c, d, e)*func(l-z, a, b, c, d, e)

def additive_func(z, a, b, c, d, e):
    return (a*np.exp(-b*z)+c*np.exp(-d*z))*z**e

def additive_gunc(z, a, b, c, d, e, f):
    return f + additive_func(z, a, b, c, d, e) + additive_func(l-z, a, b, c, d, e)

def additive_gunc_reduced(z, a, b, e, f):
    c, d = 0, 1
    return additive_gunc(z, a, b, c, d, e, f)

def func_rm(z, A, alpha, delta):
    return A*(z+delta)*np.exp(-alpha*z)

def gunc_rm(z, A, alpha, delta, C):
    return C*(1+func_rm(z, A, alpha, delta)+func_rm(l-z, A, alpha, delta))

def func_rm2(z, A, alpha, B, beta, delta):
    return (z+delta)*(A*np.exp(-alpha*z)+B*np.exp(-beta*z))

def gunc_rm2(z, A, alpha, B, beta, delta, C):
    return C*(1+func_rm2(z  , A, alpha, B, beta, delta)
               +func_rm2(l-z, A, alpha, B, beta, delta))

# my_func = additive_gunc_reduced
# lower = ( 0     , 0.2   ,  0     , 1     )
# upper = (100    , 10    , 10     ,10     )

# my_func = additive_gunc
# lower = ( 0     , 0.2   , 0     , 0     ,  0     , 0     )
# upper = ( 10    , 10    , 10    , 0.2   ,  10    , 10    )

# my_func = gunc
# lower = ( 0     , 0     , 0     , 0     ,  0     , 0     )
# upper = ( 10    , 10    , 10    , 0.2   ,  10    , 10    )

my_func = gunc_reduced
lower = ( 0     , 0     , 0     , 0     )
upper = ( 10    , 10    , 10    , 10    )

my_func = gunc_rm
lower = ( 0     , 0     , -10   , 0     )
upper = ( 10    , 10    , 10    , 10    )
# lower=None
# upper=None

my_func = gunc_rm2
lower = ( 0     , 0     , 0     , 0     , -10   , 0     )
upper = ( 10    , 10    , 0.1   , 0.2   , 10    , 10    )


popt, pcov = curve_fit(my_func, Zn, g, bounds=(lower, upper))
perr = np.sqrt(np.diag(pcov))

# if any(perr>1):
#     my_func = gunc_reduced
#     popt, pcov = curve_fit(my_func, Zn, g)
#     perr = np.sqrt(np.diag(pcov))

print("Popt", popt)
print("Perr", perr)

Zinterp = np.linspace(0, l, int(1e4))
rc('text', usetex=True)
plt.plot(Zn, g, label='Simulated current')
plt.plot(Zinterp, my_func(Zinterp, *popt), label='Curve fit')
plt.xlabel('$z/\lambda_D$')
plt.ylabel('$I/I_{OML}$')
plt.legend()
plt.title('Current for $l/\lambda_D={:.1f}$ and $qV/kT={:.0f}$'.format(l,eta))
plt.show()
