from lowess import lowess
from loess.loess_1d import loess_1d
from statsmodels.nonparametric.smoothers_lowess import lowess as statslowess
import numpy as np
import matplotlib.pyplot as plt
from sklearn.kernel_ridge import KernelRidge
from time import time

def f(x):
    return np.cos(x) + np.log(x)

x = 4*np.pi*np.random.rand(2000)
x = np.sort(x)
y = f(x) + 1.0 * np.random.randn(x.shape[0])
x0 = np.linspace(0,4*np.pi,100)

# Scikit-Learn
t0 = time()
clf = KernelRidge(kernel='rbf', gamma=0.1, degree=5)
clf.fit(x[:,None], y)
f_kernelridge = clf.predict(x0[:,None])
print("Scikit-Learn: ", time()-t0)

# Lowess GitHub library
t0 = time()
f_lowess = lowess(x, y, x0, deg=2, l=0.5)
print("Lowess GitHub library: ", time()-t0)

# Statsmodels
t0 = time()
res = statslowess(y, x, return_sorted=True, frac=0.1, it=0)
x_stats = res[:,0]
f_stats = res[:,1]
print("Statsmodels: ", time()-t0)

# Loess from PyPI
t0 = time()
x_loess, f_loess, w_loess = loess_1d(x, y, degree=2, frac=0.1, x0=x0)
print("Loess for PyPI: ", time()-t0)

plt.plot(x, y, '.', markersize=1)
plt.plot(x0, f(x0), '--', label='Ground truth')
plt.plot(x_stats, f_stats, label='Statsmodels')
plt.plot(x0, f_lowess, label='LOWESS')
plt.plot(x0, f_loess, label='LOESS')
plt.plot(x0, f_kernelridge, label='Kernel Ridge')
plt.legend()
plt.show()
