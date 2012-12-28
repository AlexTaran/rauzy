#!/bin/sh

numberOfNeighbours="50"
genFolder="gen"

sequenceFile="$genFolder/sequence$1.gen"
pointsFile="$genFolder/points$1.gen"
projectedFile="$genFolder/projected$1.gen"
normalsFile="$genFolder/normals$1.gen"
neighboursFile="$genFolder/neighbours$1.gen"
filterMaskFile="$genFolder/filterMask$1.gen"
filteredPointsFile="$genFolder/filteredPoints$1.gen"
filteredColorsFile="$genFolder/filteredColors$1.gen"
filteredNormalsFile="$genFolder/filteredNormals$1.gen"
neighboursAfterFilteringFile="$genFolder/neighboursAfterFiltering$1.gen"
facesFile="$genFolder/faces$1.gen"

VBO="$genFolder/v$1.gen"
CBO="$genFolder/c$1.gen"
NBO="$genFolder/n$1.gen"
FBO="$genFolder/f$1.gen"

./genSeq $1 > $sequenceFile
cat $sequenceFile | ./genPoints > $pointsFile
maindir=$(cat $pointsFile | ./grepMainDir)
cat $pointsFile | ./projector $maindir > $projectedFile
cat $projectedFile | ./genFastNearestNeighbours $numberOfNeighbours > $neighboursFile
cat $neighboursFile | ./genNormals > $normalsFile
cat $normalsFile | ./filterNormals.py 0.00001 > $filterMaskFile

cat $projectedFile | ./applyFilterMask.py $filterMaskFile > $filteredPointsFile
cat $sequenceFile  | ./genColors | ./applyFilterMask.py $filterMaskFile > $filteredColorsFile
cat $normalsFile   | ./applyFilterMask.py $filterMaskFile > $filteredNormalsFile

cat $filteredPointsFile | ./genFastNearestNeighbours 6 > $neighboursAfterFilteringFile

./genFaces.py $neighboursAfterFilteringFile $filteredColorsFile $filteredNormalsFile > $facesFile

cat $projectedFile | ./applyFilterMask.py $filterMaskFile | ./genVbo > $FBO

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
