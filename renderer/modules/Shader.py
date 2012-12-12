from OpenGL.GL import *
from OpenGL.GLU import *
import numpy

class Shader:
    __slots__ = ("_vsh","_fsh","_gsh","_po","_uniforms","_attribs")
    def __init__(self):
        self._vsh = 0
        self._fsh = 0
        self._gsh = 0
        self._po = 0
        self._uniforms = {}
        self._attribs = {}
    def clear(self):
        _uniforms = {}
        _attribs = {}
        if glIsProgram(self._po) == GL_TRUE :
            glDeleteProgram(self._po)
        if glIsShader(self._vsh) == GL_TRUE :
            glDeleteShader(self._vsh)
        if glIsShader(self._fsh) == GL_TRUE:
            glDeleteShader(self._fsh)
        if glIsShader(self._gsh) == GL_TRUE:
            glDeleteShader(self._gsh)
        self._vsh = 0
        self._fsh = 0
        self._gsh = 0
        self._po = 0
    def bind(self):
        glUseProgram(self._po)
    def unBind(self):
        glUseProgram(0)
    def loadFromFile(self,filename):
        file = open(filename)
        mode = ''
        v = ''
        f = ''
        g = ''
        for line in file:
            if line.strip()=="###VERTEX":
                mode='V'
                continue
            if line.strip()=="###FRAGMENT":
                mode='F'
                continue
            if line.strip()=="###GEOMETRY":
                mode='G'
                continue
            if mode=='V':
                v+=line
            if mode=='F':
                f+=line
            if mode=='G':
                g+=line
        if v.strip() == '':
            v=None
        if f.strip() == '':
            f=None
        if g.strip() == '':
            g=None
        file.close()
        self.loadFromString(v,f,g)
    def loadFromString(self,vertex,fragment,geometry):
        #print vertex
        #print fragment
        #print geometry
        self.clear()
        self._po = glCreateProgram()
        if vertex!=None :
            self._vsh = glCreateShader(GL_VERTEX_SHADER)
            glShaderSource(self._vsh,vertex)
            glCompileShader(self._vsh);
            glAttachShader(self._po, self._vsh);
            self.shaderInfoLog(self._vsh)
        if fragment!=None :
            self._fsh = glCreateShader(GL_FRAGMENT_SHADER)
            glShaderSource(self._fsh,fragment)
            glCompileShader(self._fsh);
            glAttachShader(self._po, self._fsh);
            self.shaderInfoLog(self._fsh)
        if geometry!=None :
            self._gsh = glCreateShader(GL_GEOMETRY_SHADER)
            glShaderSource(self._gsh,geometry)
            glCompileShader(self._gsh);
            glAttachShader(self._po, self._gsh);
            self.shaderInfoLog(self._gsh)
        glLinkProgram(self._po)
        self.programInfoLog()
        glValidateProgram(self._po)
        self.programInfoLog()

    def programInfoLog(self):
        log = glGetProgramInfoLog(self._po)
        if len(log)!=0:
            print log

    def shaderInfoLog(self, shader_object):
        log = glGetShaderInfoLog(shader_object)
        if len(log)!=0:
            print log

    def getUniformLocation(self,name):
        if self._uniforms.has_key(name):
            return self._uniforms[name]
        else:
            loc = glGetUniformLocation(self._po , name)
            if loc<0:
                return -1
            else:
                self._uniforms[name] = loc
                return loc
    def getAttribLocation(self,name):
        if self._attribs.has_key(name):
            return self._attribs[name]
        else:
            loc = glGetAttribLocation(self._po , name)
            if loc<0:
                return -1
            else:
                self._attribs[name] = loc
                return loc
    def setUniformVec3(self,name,v):
        self.setUniform3f(name,v.x,v.y,v.z)
    def setUniform1f(self,name,f):
        loc = self.getUniformLocation(name)
        if loc<0:
            return
        glUniform1f(loc,f)
    def setUniform3f(self,name,x,y,z):
        loc = self.getUniformLocation(name)
        if loc<0:
            return
        glUniform3f(loc,x,y,z)
    def setUniform4f(self,name,x,y,z,w):
        loc = self.getUniformLocation(name)
        if loc<0:
            return
        glUniform4f(loc,x,y,z,w)
    def setUniform1i(self,name,i):
        loc = self.getUniformLocation(name)
        if loc<0:
            return
        glUniform1i(loc,i)
    def setUniformMat4(self,name,mat):
        loc = self.getUniformLocation(name)
        if loc<0:
            return
        arr = numpy.array(mat._m,dtype='f')
        #print arr
        glUniformMatrix4fv(loc,1,GL_FALSE,arr)
    def enableAttrArray(self,name,enable):
        loc = self.getAttribLocation(name)
        if loc<0:
            return
        if enable:
            glEnableVertexAttribArray(loc)
        else:
            glDisableVertexAttribArray(loc)
        
