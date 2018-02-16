#!/bin/bash

# Deletes all *.vtk, *.topo and *.rdm files in subfolders starting with Run* but
# the most recent timestep. E.g. if a folder Run15_25mm_2.5V contains one bunch
# of files called pictetrabin001000_*.rdm and another bunch of files called
# pictetrabin002000_*.rdm the latter bunch will not be deleted.
# 
# 	./clean.sh

for FOLDER in Run*
do
	VTK=`ls $FOLDER/pictetra*.vtk  -t 2> /dev/null | tail -n +2`
	TOP=`ls $FOLDER/pictetra*.topo -t 2> /dev/null | tail -n +2`
	SCC=`ls $FOLDER/scc*.vtk       -t 2> /dev/null | tail -n +2`
	RDM=`ls $FOLDER/*_000000.rdm   -t 2> /dev/null | tail -n +2 | sed 's/_000000/_*/'`
	rm -f $VTK $TOP $SCC $RDM 
done
