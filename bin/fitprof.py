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
# l = max(Zn)

# m = int(len(Zn)/2)
# Zn = Zn[:m]
# f = f[:m]

def func(z, a, b, c, d, e):
    # return a*(z**b)*(np.exp(-c*z)+d*np.exp(-e*z))+f
    # return a*(z**b)*(c**-z)+d
    # return (a*np.exp(-b*z)+c*np.exp(-d*z))*(z**e)+f # Great success!
    # return (a*b**z+c*d**z)*(z**e)+f
    return (a*np.exp(-b*z)+c*np.exp(-d*z))*(z**e)+1 # Great success!
    # return (a*np.exp(-b*z)+c*np.exp(-d*np.sqrt(z)))*(z**e)+1 # Great success!
    # return (a*np.exp(-b*z)+c*np.exp(-d*z**e))*z+1

def gunc(z, a, b, c, d, e, f):
    # return func(z, a, b, c, d, e, f)*func(l-z, a, b, c, d, e, f)
    return f*func(z, a, b, c, d, e)*func(l-z, a, b, c, d, e)

def gunc_reduced(z, a, b, e, f):
    c, d = 0, 1
    c, d = 0.02859, 0.06836
    return f*func(z, a, b, c, d, e)*func(l-z, a, b, c, d, e)

def additive_func(z, a, b, c, d, e):
    return (a*np.exp(-b*z)+c*np.exp(-d*z))*z**e

def additive_gunc(z, a, b, c, d, e, f):
    return f + additive_func(z, a, b, c, d, e) + additive_func(l-z, a, b, c, d, e)

def additive_gunc_reduced(z, a, b, e, f):
    c, d = 0, 1
    return additive_gunc(z, a, b, c, d, e, f)

def additive_gunc_reduced2(z, a, e, f):
    b = 2.105
    return additive_gunc_reduced(z, a, b, e, f)

def lfunc(z):
    # c = [0.31954035, 0.37300383, 0.01781202, 0.03428675, 0.19866518, 1.01889591] # 2
    # c = [0.25984115, 0.27587257, 0.02103033, 0.05847973, 0.20860986, 1.47716334] # 6
    # c = [1.40390027, 0.57300261, 0.02762015, 0.0437869 , 0.3582573 , 1.02575968] # 10
    # c = [2.78543138, 0.67890957, 0.03090874, 0.05976335, 0.49747247, 1.02552137] # 25
    # c = [3.10750752, 0.65961924, 0.02553392, 0.05421702, 0.51825116, 1.03097488] # 32
    # c = [4.97752097, 0.69210761, 0.0216956 , 0.07139628, 0.65178986, 1.02271311] # 75
    # c = [5.14755149, 0.63980931, 0.01076595, 0.07144683, 0.68706727, 1.02748378] # 100
    return (c[0]*np.exp(-c[1]*z)+c[2]*np.exp(-c[3]*z))*(z**c[4])+1

def lgunc(z, f):
    return f*lfunc(z)*lfunc(l-z)

# my_func = additive_gunc_reduced2
# lower = ( 0     ,  0     , 1     )
# upper = (100    , 10     ,10     )

# my_func = additive_gunc_reduced
# lower = ( 0     , 0.2   ,  0     , 1     )
# upper = (100    , 10    , 10     ,10     )

my_func = additive_gunc
lower = ( 0     , 0.2   , 0     , 0     ,  0     , 0     )
upper = ( 10    , 10    , 10    , 0.2   ,  10    , 10    )

# my_func = gunc
# lower = ( 0     , 0     , 0     , 0     ,  0     , 0     )
# upper = ( 10    , 10    , 10    , 0.2   ,  10    , 10    )

# my_func = gunc_reduced
# lower = ( 0     , 0     , 0     , 0     )
# upper = ( 10    , 10    , 10    , 10    )

# my_func = lgunc
# lower = ( 0)
# upper = ( 10)

popt, pcov = curve_fit(my_func, Zn, g, bounds=(lower, upper))
perr = np.sqrt(np.diag(pcov))

# if any(perr>1):
#     my_func = gunc_reduced
#     popt, pcov = curve_fit(my_func, Zn, g)
#     perr = np.sqrt(np.diag(pcov))

print("Popt", popt)
# print("Pcov", pcov)
print("Perr", perr)

# popt[0] = 1.019
# popt[0] = 1.027 # 100

Zinterp = np.linspace(0, l, int(1e4))
rc('text', usetex=True)
plt.plot(Zn, g, label='Simulated current')
plt.plot(Zinterp, my_func(Zinterp, *popt), label='Curve fit')
plt.xlabel('$z/\lambda_D$')
plt.ylabel('$I/I_{OML}$')
plt.legend()
plt.title('Current for $l/\lambda_D={:.1f}$ and $qV/kT={:.0f}$'.format(l,eta))
plt.show()
