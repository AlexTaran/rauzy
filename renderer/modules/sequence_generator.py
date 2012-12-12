
from bigfloat import *

class SequenceGenerator:
  def __init__(self, ):
    self.iterations = []

  def addIteration(self, value):
    self.iterations.append(value)

  def processIterations(self, num, prevs):
    for i in xrange(num):
      s = self.iterations[-prevs]
      for j in xrange(1, prevs):
        s += self.iterations[-(prevs-j)]
      self.iterations.append(s)

  def lastIteration(self):
    return self.iterations[-1];


def gen_precise_vbo4(seq):
  main_direction = [len([c for c in seq if c==ch]) for ch in '1234']
