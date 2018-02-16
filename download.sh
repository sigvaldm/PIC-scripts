#!/bin/bash

# Download .hst files from Abel listed in the code:
# 
# 	./download.sh
# 
# Downlaod .hst, .topo and .vtk files from Abel:
# 
# 	./download.sh all
# 
# The folders on Abel downloaded from are listed below. So is the username.
# Modify as appropriate. In order not to be asked for password a key-pair must
# be put in ~/.ssh.

USER="sigvaldm"

for RUN in \
	Run15_25mm_2.5V \
	Run15_25mm_4.0V \
	Run15_25mm_5.5V \
	Run15_25mm_7.0V \
	Run15_50mm_2.5V \
	Run15_50mm_4.0V \
	Run15_50mm_5.5V \
	Run15_50mm_7.0V 
do

	HST="/usit/abel/u1/sigvaldm/PTetra/Projects/NeedleProbe/$RUN/pictetra.hst" 
	# HST="/usit/abel/u1/sigvaldm/PTetra/Projects/NeedleProbe/$RUN/pictetra*.hst" 
	TOP=`ssh $USER@abel.uio.no "ls -t /usit/abel/u1/sigvaldm/PTetra/Projects/NeedleProbe/$RUN/pictetra*.topo | head -n 1"`
	VTK=`ssh $USER@abel.uio.no "ls -t /usit/abel/u1/sigvaldm/PTetra/Projects/NeedleProbe/$RUN/pictetra*.vtk | head -n 1"`
	SCC=`ssh $USER@abel.uio.no "ls -t /usit/abel/u1/sigvaldm/PTetra/Projects/NeedleProbe/$RUN/scc*.vtk | head -n 1"`

	if [ "$1" = "all" ]; then
		echo "Downloading latest .hst, .vtk and .topo files for $RUN"
		rsync -P $USER@abel.uio.no:$HST $USER@abel.uio.no:$TOP $USER@abel.uio.no:$VTK $USER@abel.uio.no:$SCC $RUN/
	else
		echo "Downloading latest .hst files for $RUN"
		rsync -P $USER@abel.uio.no:$HST $RUN/
	fi
done
