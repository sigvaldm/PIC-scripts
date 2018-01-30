#!/bin/bash

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
		echo "Downloading latest files for $RUN"

		HST="/usit/abel/u1/sigvaldm/PTetra/Projects/NeedleProbe/$RUN/pictetra*.hst" 
		VTK=`ssh $USER@abel.uio.no "ls -t  /usit/abel/u1/sigvaldm/PTetra/Projects/NeedleProbe/$RUN/pictetra*.vtk | head -n 1"`
		SCC=`ssh $USER@abel.uio.no "ls -t  /usit/abel/u1/sigvaldm/PTetra/Projects/NeedleProbe/$RUN/scc*.vtk | head -n 1"`

		rsync -P $USER@abel.uio.no:$HST $USER@abel.uio.no:$VTK $USER@abel.uio.no:$SCC $RUN/
done
