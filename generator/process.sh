#!/bin/sh

numberOfNeighbours="50"

sequenceFile="sequence$1"
pointsFile="points$1"
projectedFile="projected$1"
normalsFile="normals$1"
neighboursFile="neighbours$1"


VBO="v$1"
CBO="c$1"
NBO="n$1"

./genSeq $1 > $sequenceFile
cat $sequenceFile | ./genPoints > $pointsFile
maindir=$(cat $pointsFile | ./grepMainDir)
cat $pointsFile | ./projector $maindir > $projectedFile
cat $projectedFile | ./genNearestNeighbours $numberOfNeighbours > $neighboursFile
cat $neighboursFile | ./genNormals > $normalsFile

cat $projectedFile | ./genVerticesVbo > $VBO
cat $sequenceFile | ./genColorsVbo > $CBO
cat $normalsFile | ./genVerticesVbo > $NBO

#rm -f $sequenceFile
#rm -f $pointsFile
#rm -f $projectedFile

#maindir=$(cat $1 |./grepmaindir)
#echo $maindir
#cat $1 | ./projector $maindir
