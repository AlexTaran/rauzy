#!/usr/bin/python

import sys
from vector3 import Vector3

def extract_floats(s):
  return [float(x) for x in s.strip().split()]

def check_consistency(neibs, color, normal):
  ln = len(neibs)
  lc = len(color)
  lr = len(normal)
  if ln == 0 and lc == 0 and lr == 0:
    return True
  if ln % 3 != 0 or ln == 0 or lc !=3 or lr !=3:
    return False
  return True

# return list of floats
# result is sequence of faces (len(neighbors)==len(result-faces))
# face is 3 points
# each point is: posx, posy, posz, colr, colg, colb, nrmx, nrmy, nrmz

def vects(l):
  for i in xrange(0, len(l), 3):
    yield l[i:i+3]

class NeighboursComparator:
  def __init__(self, p, n):
    self.p = Vector3(p).normalize()
    self.n = Vector3(n).normalize()
  def __call__(self, p1, p2):
    v1 = p1 - self.p
    v2 = p2 - self.p
    n1 = v1.cross(self.n).normalize()
    n2 = v2.cross(self.n).normalize()
    value = n1.cross(n2).dot(self.n)
    if value > 0.0:
      return 1
    if value < 0.0:
      return -1
    return 0

def gen_faces(neibs, color, normal):
  point = Vector3(neibs[0:3])
  nrm = Vector3(normal)
  vects = []
  #sys.stderr.write(str(len(neibs))+"\n")
  for i in xrange(3, len(neibs), 3):
    vects.append(Vector3(neibs[i:i+3]))
  srt = vects.sort(cmp=NeighboursComparator(point, nrm))
  vects.append(vects[0])
  outbuf = []
  for i in xrange(1, len(vects)):
    v1 = vects[i-1]
    v2 = vects[i]
    n = list(v1.cross(v2).normalize())
    #sys.stderr.write(str(len(list(point) + color + n))+"\n")
    outbuf += list(point) + color + normal
    outbuf += list(v1) + color + normal
    outbuf += list(v2) + color + normal
    #sys.stderr.write(str(list(point) + color + n)+"\n")
  return outbuf

def main():
  if len(sys.argv) != 4:
    sys.stderr.write("Wrong number of arguments")
  with open(sys.argv[1]) as neighbours_file, open(sys.argv[2]) as colors_file, open(sys.argv[3]) as normals_file:
    while True:
      neighbours = extract_floats(neighbours_file.readline())
      color = extract_floats(colors_file.readline())
      normal = extract_floats(normals_file.readline())
      if not check_consistency(neighbours, color, normal):
        sys.stderr.write("Inconsistent triplet found!\n")
        break
      if len(neighbours) == 0:
        break
      face = gen_faces(neighbours, color, normal)
      print " ".join([str(f) for f in face])

if __name__ == "__main__":
  main()
