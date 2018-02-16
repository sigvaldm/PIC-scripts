# PTetra scripts
Scripts for use with PTetra. Brief explanation follows below. More explanation is provided in each individual file.

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

I always put the files directly in a folder where the simulation results are stored
in subfolders prefixed with `Run`. The `.sh`-files would require modification to work
with other folder structures. The `.py`-files should work regardless, but several
files rely on `funcs.py` being in the same folder.
