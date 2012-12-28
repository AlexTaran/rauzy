#!/usr/bin/python
from math import sqrt
from numpy import *
from vector3 import *

def project_point_on_plane(p, n, D):
  nl = sqrt(n[0] ** 2 + n[1] ** 2 + n[2] ** 2)
  dist = p[0] * n[0] + p[1] * n[1] + p[2] * n[2] + D
  dist /= nl
  x = p[0] - dist * n[0] / nl
  y = p[1] - dist * n[1] / nl
  z = p[2] - dist * n[2] / nl
  return [x, y, z]

def complete_basis(vec):
  vx, vy, vz = vec
  if abs(vx) < 1e-6 or abs(vy) < 1e-6 or abs(vz) < 1e-6:
    raise Exception("Bad Vector for fill basis")
  v1 = Vector3(0.0, vz, -vy).normalized()
  v0 = Vector3(vx , vy,  vz).normalized()
  v2 = v0.cross(v1);
  m = matrix([v0, v1, v2])
  #print m.T
  return m.T.I

if __name__ == "__main__":
  p = [16,76,80]
  n = [1,1,1]
  D = -1
  x, y, z = project_point_on_plane(p, n, D)
  print x*n[0] + y*n[1] + z*n[2] + D
  normal = [ 0.92209947,  0.21038206,  0.32476447]
  print complete_basis(normal)
  n4 = [0.49397243259417783, 0.76253943014453884, 0.31999472048553657, 0.26856699755036106]
