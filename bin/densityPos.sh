#!/bin/bash

# Script used to run separate instances of densityNew for each point in
# scanpositions.txt-file

NUM=$1

DIR="POS$NUM"
FILE="$DIR/scanpositions.txt"
mkdir -p "$DIR"

LINE=$(head -n $(($NUM+2)) scanpositions.txt | tail -1)

echo "\$begin$"   >  $FILE
echo "  nvScan=1" >> $FILE
echo $LINE        >> $FILE
echo "\$end$"     >> $FILE

cp density.dat $DIR
cp octree.dat $DIR
cp densityNew $DIR
ln -sf ../meshAndField.dat $DIR

cd $DIR
./densityNew
NEWNAME=$(printf "distfunct%06d.vtk" $NUM)
mv distfunct000001.vtk ../$NEWNAME
cd ..
rm -rf $DIR
