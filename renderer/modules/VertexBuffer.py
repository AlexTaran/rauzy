from OpenGL.GL import *
from OpenGL.GLU import *

from OpenGL.arrays import ArrayDatatype as ADT
from OpenGL.arrays import *
#from OpenGL_accelerate.arraydatatype import ArrayDatatype as AT
import numpy
#import Numeric
from ctypes import c_void_p

class VertexBuffer:
    __slots__ = ('_id','_target','_size' )

    def __init__(self):
        self._target = 0
        self._id = glGenBuffers(1)
        if self._id==0 :
            raise AssertionError('Failed to create VBO')
        self._size = 0
    def __del__(self):
        print "trying to delete VBO, id = "+str(self._id)+", but pyopengl sucks and hasn't function to do it"
        #glDeleteBuffers(1,[self._id])
    def bind(self,theTarget):
        self._target = theTarget
        glBindBuffer(self._target,self._id)
    def unBind(self):
        glBindBuffer(self._target,0)
        self._target = 0
    def setData(self,data, usage):
        arr = numpy.array(data, dtype='f')
        glBufferData(self._target, arr, usage)
    def setBinaryData(self,data, usage):
        glBufferData(self._target, data, usage)

    def setSubData(self,offs,data):
        if offs+ADT.arrayByteCount(data)>self._size:
            raise AssertionError('Tried to overflow VBO')
        raise Exception("Call of Unimplemented function: VertexBuffer.setSubData")
        #glBufferSubData(self._target, offs, ADT.arrayByteCount(data),ADT.voidDataPointer(data))

