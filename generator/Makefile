all: genSeq genPoints projector grepMainDir genVbo genColors genNormals genNearestNeighbours genFastNearestNeighbours

genSeq: genSeq.cpp
	g++ genSeq.cpp -o genSeq

genPoints: genPoints.cpp
	g++ genPoints.cpp -o genPoints

projector: projector.cpp
	g++ projector.cpp -o projector -lmpfr

grepMainDir: grepMainDir.cpp
	g++ grepMainDir.cpp -o grepMainDir

genVbo: genVbo.cpp
	g++ genVbo.cpp -o genVbo

genColors: genColors.cpp
	g++ genColors.cpp -o genColors

genNormals: genNormals.cpp
	g++ genNormals.cpp -o genNormals

genNearestNeighbours: genNearestNeighbours.cpp
	g++ genNearestNeighbours.cpp -o genNearestNeighbours

genFastNearestNeighbours: genFastNearestNeighbours.cpp
	g++ genFastNearestNeighbours.cpp -o genFastNearestNeighbours

clean:
	rm -f genSeq genPoints projector grepMainDir genVbo genColors genNormals genNearestNeighbours genFastNearestNeighbours
