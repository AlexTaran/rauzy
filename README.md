All this repository code is copyright of Alexander Taran

rauzy
=====

Rauzy fractal generation and renderer

Usage
=====

in folder 'generator' run:

make
./process.sh 15

where 15 is number of iterations for sequence. You can use any number. There are nearly 60000 points
for 15 iterations, you can use more or less to generate another number of points.

The result is 3 files: v15, c15 and n15 - vertexbuffer, colorbuffer and normalsbuffer

NB: normals are in experimental mode now and may be wrong
