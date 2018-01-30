import numpy as np
import os
import glob

def readHst(fname):

    # Make fnames a list of filenames of the form pictetra*.hst
    if os.path.isdir(fname):
        pattern = os.path.join(fname,'pictetra??.hst')
        fnames = glob.glob(pattern)
        fnames.sort()
        pattern = os.path.join(fname,'pictetra.hst')
        if os.path.isfile(pattern):
            fnames.append(pattern)
    else:
        fnames = [fname]
    print(fnames)

    data = []
    for fname in fnames:
        f = open(fname)
        for l in f:
            l.strip() 
            if len(l)>0 and l[0] != '#':
                data.append(l.split())
        f.close()
    return np.array(data, dtype=float)

def expAvg(data, dt, tau=0.05e-6):
    weight = 1-np.exp(-dt/tau)
    result = np.zeros(data.shape)
    result[0] = data[0]
    for i in range(1,len(data)):
        result[i] = weight*data[i] + (1-weight)*result[i-1]
    return result
