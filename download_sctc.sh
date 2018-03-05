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
	/usit/abel/u1/sigvaldm/PTetra/Projects/SCTC/Run1_50mm_1.0V \
	/usit/abel/u1/sigvaldm/PTetra/Projects/SCTC/Run1_50mm_2.0V \
	/usit/abel/u1/sigvaldm/PTetra/Projects/SCTC/Run1_50mm_3.0V \
	/usit/abel/u1/sigvaldm/PTetra/Projects/SCTC/Run1_50mm_4.0V \
	/usit/abel/u1/sigvaldm/PTetra/Projects/SCTC/Run1_50mm_5.0V \
	/usit/abel/u1/sigvaldm/PTetra/Projects/SCTC/Run1_50mm_6.0V \
	/usit/abel/u1/sigvaldm/PTetra/Projects/SCTC/Run1_50mm_7.0V \
	/usit/abel/u1/diakod/PicTetra/Projects/NeedleProbe/Run1_25mm_1V \
	/usit/abel/u1/diakod/PicTetra/Projects/NeedleProbe/Run1_25mm_2V \
	/usit/abel/u1/diakod/PicTetra/Projects/NeedleProbe/Run1_25mm_3V \
	/usit/abel/u1/diakod/PicTetra/Projects/NeedleProbe/Run1_25mm_4V \
	/usit/abel/u1/diakod/PicTetra/Projects/NeedleProbe/Run1_25mm_5V \
	/usit/abel/u1/diakod/PicTetra/Projects/NeedleProbe/Run1_25mm_6V \
	/usit/abel/u1/diakod/PicTetra/Projects/NeedleProbe/Run1_25mm_7V
do

	HST="$RUN/pictetra.hst" 
	TARGET=${RUN##*/}
	if [ "$1" = "all" ]; then

		echo "Downloading latest .hst, .vtk and .topo files for $TARGET"
		TOP=`ssh $USER@abel.uio.no "ls -t $RUN/pictetra*.topo | head -n 1"`
		VTK=`ssh $USER@abel.uio.no "ls -t $RUN/pictetra*.vtk | head -n 1"`
		SCC=`ssh $USER@abel.uio.no "ls -t $RUN/scc*.vtk | head -n 1"`
		rsync -P $USER@abel.uio.no:$HST $USER@abel.uio.no:$TOP $USER@abel.uio.no:$VTK $USER@abel.uio.no:$SCC $TARGET/

	else
		echo "Downloading latest .hst files for $TARGET"
		rsync -P $USER@abel.uio.no:$HST $TARGET/
	fi
done
