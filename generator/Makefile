all: genSeq genPoints projector grepMainDir genVerticesVbo genColorsVbo genNormals genNearestNeighbours

genSeq: genSeq.cpp
	g++ genSeq.cpp -o genSeq

genPoints: genPoints.cpp
	g++ genPoints.cpp -o genPoints

projector: projector.cpp
	g++ projector.cpp -o projector -lmpfr

grepMainDir: grepMainDir.cpp
	g++ grepMainDir.cpp -o grepMainDir

genVerticesVbo: genVerticesVbo.cpp
	g++ genVerticesVbo.cpp -o genVerticesVbo

genColorsVbo: genColorsVbo.cpp
	g++ genColorsVbo.cpp -o genColorsVbo

genNormals: genNormals.cpp
	g++ genNormals.cpp -o genNormals

genNearestNeighbours: genNearestNeighbours.cpp
	g++ genNearestNeighbours.cpp -o genNearestNeighbours

clean:
	rm -f genSeq genPoints projector grepMainDir genVerticesVbo genColorsVbo genNormals genNearestNeighbours
