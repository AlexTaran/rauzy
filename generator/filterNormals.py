#!/usr/bin/python

import sys
from math import *

def veclen2(v):
  return v[0] ** 2 + v[1] ** 2 + v[2] ** 2

def main():
  if len(sys.argv) != 2:
    print '''Wrong number of arguments. Should be
      <min_length_of_normal>
    '''
    return
  min_len2 = float(sys.argv[1]) ** 2
  first_line = True
  for line in sys.stdin:
    normal = [float(x) for x in line.strip().split()]
    if first_line:
      first_line = False
    else:
      sys.stdout.write('\n')
    if veclen2(normal) >= min_len2:
      sys.stdout.write('1')
    else:
      sys.stdout.write('0')

if __name__ == "__main__":
  main()
