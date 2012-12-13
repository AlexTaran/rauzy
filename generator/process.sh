#!/bin/sh

numberOfNeighbours="50"

sequenceFile="sequence$1.gen"
pointsFile="points$1.gen"
projectedFile="projected$1.gen"
normalsFile="normals$1.gen"
neighboursFile="neighbours$1.gen"
filterMaskFile="filterMask$1.gen"
filteredPointsFile="filteredPoints$1"
filteredColorsFile="filteredColors$1"
filteredNormalsFile="filteredNormals$1"
neighboursAfterFilteringFile="neighboursAfterFiltering$1"
facesFile="faces$1"

VBO="v$1.gen"
CBO="c$1.gen"
NBO="n$1.gen"
FBO="f$1.gen"

./genSeq $1 > $sequenceFile
cat $sequenceFile | ./genPoints > $pointsFile
maindir=$(cat $pointsFile | ./grepMainDir)
cat $pointsFile | ./projector $maindir > $projectedFile
cat $projectedFile | ./genNearestNeighbours $numberOfNeighbours > $neighboursFile
cat $neighboursFile | ./genNormals > $normalsFile
cat $normalsFile | ./filterNormals.py 0.0001 > $filterMaskFile

cat $projectedFile | ./applyFilterMask.py $filterMaskFile > $filteredPointsFile
cat $sequenceFile  | ./genColors | ./applyFilterMask.py $filterMaskFile > $filteredColorsFile
cat $normalsFile   | ./applyFilterMask.py $filterMaskFile > $filteredNormalsFile

cat $filteredPointsFile | ./genNearestNeighbours 6 > $neighboursAfterFilteringFile

./genFaces.py $neighboursAfterFilteringFile $filteredColorsFile $filteredNormalsFile > $facesFile

cat $projectedFile | ./applyFilterMask.py $filterMaskFile | ./gen > $FBO

cat $filteredPointsFile  | ./genVbo > $VBO
cat $filteredColorsFile  | ./genVbo > $CBO
cat $filteredNormalsFile | ./genVbo > $NBO
cat $facesFile           | ./genVbo > $FBO

#rm -f $sequenceFile
#rm -f $pointsFile
#rm -f $projectedFile

#maindir=$(cat $1 |./grepmaindir)
#echo $maindir
#cat $1 | ./projector $maindir
