import meshio
import numpy as np
import re
import os
import scipy.special as special
from langmuir import *

def get_data(path):

    path = os.path.abspath(path)
    l    =  float(re.findall('[\d\.]+(?=mm)' , path)[-1])*1e-3
    n    =  float(re.findall('[\d\.]+(?=n)'  , path)[-1])*1e10
    eV   =  float(re.findall('[\d\.]+(?=eV)' , path)[-1])
    eta  = -float(re.findall('[\d\.]+(?=eta)', path)[-1])
    print('l={}, n={}, eV={}, eta={}'.format(l, n, eV, eta))

    r = 1e-3
    elec = Species(n=n, eV=eV)
    geo = Cylinder(r, 1)
    I_OML = OML_current(geo, elec, eta=eta)

    mesh = meshio.read(path)

    z_vertices = mesh.points[:,2]
    cells = mesh.cells['triangle']
    z_centroids = np.average(z_vertices[cells], axis=1)
    facet_currents = mesh.cell_data['triangle']['J']

    # Sort along probe (not sure if this is necessary)
    ind = np.argsort(z_centroids)
    z_centroids = z_centroids[ind]
    facet_currents = facet_currents[ind]

    zmin = z_centroids[0]
    zmax = z_centroids[-1]

    # Filter end caps
    tol = 1e-10
    ind = np.logical_and(np.abs(z_centroids-zmin)>tol,
                         np.abs(z_centroids-zmax)>tol)
    z_centroids = z_centroids[ind]
    facet_currents = facet_currents[ind]

    # Shift and scale z-axis
    z_centroids -= zmin
    z_centroids /= elec.debye
    l /= elec.debye

    # Scale to A/m and then w.r.t. I_OML
    facet_currents *= 2*np.pi*r
    facet_currents /= I_OML

    L = l*np.ones_like(z_centroids)
    ETA = eta*np.ones_like(z_centroids)
    indeps = np.array([z_centroids, L, ETA], dtype=float)

    return indeps, facet_currents

def Gamma(a, x):
    return special.gammaincc(a, x)*special.gamma(a)

def h(zeta, alpha, gamma):
    return np.exp(-alpha*zeta)*(zeta**gamma)

# Indefinite integral of h
def H(zeta, alpha, gamma):
    if zeta==0: zeta=np.finfo(float).eps
    return -(zeta**gamma)*((alpha*zeta)**(-gamma))*Gamma(1+gamma,alpha*zeta)/alpha

def additive_model(zeta, lambd, A, alpha, B, beta, gamma, C):
    return C + A*h(zeta, alpha, gamma) + B*h(zeta, beta, gamma) \
             + A*h(lambd-zeta, alpha, gamma) + B*h(lambd-zeta, beta, gamma)

def int_additive_model(zeta, lambd, A, alpha, B, beta, gamma, C):
    return C*zeta + A*H(zeta, alpha, gamma) + B*H(zeta, beta, gamma) \
                  - A*H(lambd-zeta, alpha, gamma) - B*H(lambd-zeta, beta, gamma)
