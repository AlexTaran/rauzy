#!/usr/bin/python
from math import sqrt
from numpy import *
from vector3 import *
from bigfloat import *

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

def normalize_vec(vec):
  l = sqrt(vec[0] ** 2 + vec[1] ** 2 + vec[2] ** 2 + vec[3] ** 2, precision(200))
  with precision(200):
    n = [v / l for v in vec]
  return n

def complete_basis4(vec):
  vx, vy, vz, vw = [BigFloat(v, context = precision(200)) for v in vec]
  #print [vx,vy,vz,vw]
  if abs(vx) < 1e-6 or abs(vy) < 1e-6 or abs(vz) < 1e-6 or abs(vw) < 1e-6:
    raise Exception("Bad Vector for fill basis")
  dopvec = normalize_vec([1.0,1.0,1.0,1.0])
  b = array([0.0,0.0,0.0,1.0])
  v0 = normalize_vec([ vx, vy , vz ,  vw])
  v1 = normalize_vec([0.0, 0.0, vw , -vz])
  v2 = normalize_vec([-vy, vx , 0.0, 0.0])
  #print [v0,v1,v2,dopvec]
  mtx = matrix([v0,v1,v2,dopvec])
  #print mtx
  with precision(200):
    v3 = normalize_vec(array((b * mtx.I.T).tolist()[0]))
  m = matrix([v0,v1,v2,v3])
  print m
  return m

if __name__ == "__main__":
  p = [16,76,80]
  n = [1,1,1]
  D = -1
  x, y, z = project_point_on_plane(p, n, D)
  print x*n[0] + y*n[1] + z*n[2] + D
  normal = [ 0.92209947,  0.21038206,  0.32476447]
  print complete_basis(normal)
  n4 = [0.49397243259417783, 0.76253943014453884, 0.31999472048553657, 0.26856699755036106]
  print complete_basis4(n4)
