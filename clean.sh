#!/bin/bash

for FOLDER in Run*
do
	VTK=`ls $FOLDER/pictetra*.vtk -t 2> /dev/null | tail -n +2`
	TOP=`ls $FOLDER/pictetra*.topo -t 2> /dev/null | tail -n +2`
	SCC=`ls $FOLDER/scc*.vtk      -t 2> /dev/null | tail -n +2`
	RDM=`ls $FOLDER/*_000000.rdm  -t 2> /dev/null | tail -n +2 | sed 's/_000000/_*/'`
	rm -f $VTK $TOP $SCC $RDM 
done
