#!/usr/bin/python

from modules.sequence_generator import SequenceGenerator

def gen_rauzy4_vbo(iters):
  gen = SequenceGenerator()
  gen.addIteration('12')
  gen.addIteration('13')
  gen.addIteration('14')
  gen.addIteration('1')
  gen.processIterations(iters, 4);
  seq = gen.lastIteration()
  deltas = {'1': [1, 0, 0, 0],
            '2': [0, 1, 0, 0],
            '3': [0, 0, 1, 0],
            '4': [0, 0, 0, 1]}
  colors = {'1': [1.0, 0.0, 0.0],
            '2': [0.0, 1.0, 0.0],
            '3': [0.0, 0.0, 1.0],
            '4': [1.0, 1.0, 0.0]}
  curr = [0, 0, 0, 0]
  v = []
  c = []
  for ch in seq:
    dlt = deltas[ch]
    curr = [curr[i]+dlt[i] for i in xrange(4)]
    v += curr
    c += colors[ch]
  return v, c

v, c = gen_rauzy4_vbo(10)

normal4 = [v4[-4], v4[-3], v4[-2], v4[-1]]
l4 = normal4[0] ** 2 + normal4[1] ** 2 + normal4[2] ** 2 + normal4[3] ** 2
normal4 = [coord/sqrt(l4) for coord in normal4]
rotation4 = complete_basis4(normal4)

