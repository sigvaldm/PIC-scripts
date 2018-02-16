# PTetra scripts
Scripts for use with PTetra.

The following scripts are assumed to lie in a folder with subfolders prefixed
`Run` containing data. E.g. `Run15_25mm_2.5V`. `download.sh` will create such
folders when downloading the latest files from Abel, matching the folder
structure on Abel.  More detailed description follows inside the individual scripts.

| Filename                 | Brief description                                                 |
|--------------------------|-------------------------------------------------------------------|
| clean.sh                 | Deletes old data and restart files but leaves the latest timestep |
| cylinderpos.py           | Creates coordinates on a cylinder                                 |
| download.sh              | Downloads latest data from Abel                                   |
| funcs.py                 | Plotting functions used by other script                           |
| plot_currents.py         | Plots current of one or several probes                            |
| plot_IV.py               | Plots IV-characteristics                                          |
| plot_numparticles.py     | Plots the number of particle in a simulation domain               |
| plot_segment_currents.py | Plots the current of the segments of a probe                      |
