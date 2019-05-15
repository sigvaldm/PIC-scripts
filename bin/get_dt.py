#!/usr/bin/env python
import sys
import metaplot as mpl

for f in sys.argv[1:]:
    df = mpl.DataFrame(f)
    dt = df['t'][1].m*1e12
    print('{}: {} ps'.format(f, dt))
