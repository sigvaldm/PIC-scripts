#!/usr/bin/env python
import numpy as np
import sys
import re
import os
import matplotlib.pyplot as plt

file = np.load(sys.argv[1])
ls = file['ls']
etas = file['etas']
ydata = file['popts']

comb = zip(ls, etas, ydata)
arr = map(lambda x: np.concatenate([[x[0]], [x[1]], x[2]]), comb)
arr = np.array(list(arr))

tol = 1e-6

for col in range(ydata.shape[1]):
    plt.figure()

    for eta in np.unique(etas):
        eta_inds = np.where(np.abs(etas-eta)<tol)[0]
        ls_at_eta = ls[eta_inds]
        ls_at_eta.sort()

        value = []
        for l in ls_at_eta:
            l_inds = np.where(np.abs(ls-l)<tol)[0]
            ind = [i for i in l_inds if i in eta_inds][0]
            value.append(ydata[ind,col])

        plt.plot(ls_at_eta, value, label=r'eta={:.0f}'.format(eta))

    plt.grid()
    plt.legend()

plt.show()
