import numpy
from vector3 import *
from quaternion import *
from matrix44 import *

class Camera:
    __slots__ = ("_pos","_dir","_up")
    def __init__(self,*args):
        if len(args)==3:
            self._pos = map(float,args[0][:3])
            self._dir = map(float,args[1][:3])
            self._up  = map(float,args[2][:3])
            self.reNormalize()
        elif len(args)==1:
            if not isinstance(args[0],Camera):
                raise TypeError("Copy constructor of camera must receive a camera")
            self._pos = map(float,args[0]._pos[:3])
            self._dir = map(float,args[0]._dir[:3])
            self._up  = map(float,args[0]._up [:3])
        elif len(args)==0:
            self._pos = Vector3(0.0,0.0,0.0)
            self._dir = Vector3(1.0,0.0,0.0)
            self._up  = Vector3(0.0,1.0,0.0)
        else:
            raise ValueError("Camera constructor can receive only 0,1 or 3 arguments")
        self.reNormalize()

    def reNormalize(self):
        self._dir.normalize()
        side = (self._dir.cross(self._up)).normalized()
        side.y = 0.0 # snap to vertical
        self._up = (side.cross(self._dir)).normalized()
    def move(self,dist):
        if isinstance(dist,float):
            self._pos = self._pos + self._dir*dist
        elif isinstance(dist,Vector3):
            self._pos = self._pos + dist
        else:
            raise ValueError("Camera move method can only receive float or vector3")
    def getRight(self):
        return (self._dir.cross(self._up)).normalized()
    def getForwardXZ(self):
        v = [self._dir.copy(),self._up.copy()]
        v[0].y = 0.0
        v[1].y = 0.0
        l =  [v[0].get_length(),v[1].get_length()]
        if l[0]>l[1]:
            return v[0].normalized()
        else:
            return v[1].normalized()
    def strafeRight(self,dist): #dist is only float
        self._pos = self._pos + self.getRight() * dist
    def rotateHoriz(self,radians):
        qn = Quaternion(Vector3(0.0,1.0,0.0),radians)
        qn.normalize()
        qc=qn.copy()
        qc.inverse()
        pd = Quaternion(self._dir.x, self._dir.y, self._dir.z, 0)
        pd.normalize()
        pu = Quaternion(self._up.x, self._up.y, self._up.z, 0)
        pu.normalize()
        rd = qn * pd * qc
        ru = qn * pu * qc
        self._dir = Vector3(rd.x, rd.y, rd.z)
        self._up = Vector3(ru.x, ru.y, ru.z)
        self.reNormalize()
    def rotateVert(self,radians):
        side = self.getRight()
        #assert(side.y < EPSILON)
        side.y = 0.0;
        qn = Quaternion(side, radians)
        qn.normalize()
        qc = qn.copy()
        qc.inverse()
        pd=Quaternion(self._dir.x, self._dir.y, self._dir.z, 0)
        pd.normalize()
        pu=Quaternion(self._up.x, self._up.y, self._up.z, 0)
        pu.normalize()
        pd = qn * pd * qc
        pu = qn * pu * qc
        self._dir = Vector3(pd.x, pd.y, pd.z)
        self._up = Vector3(pu.x, pu.y, pu.z)
        self.reNormalize()
    def getLookAtMatrix(self):
        #Matrix4 matrix2, resultMatrix;
        fwd = self._dir.copy()
        side =(self._dir.cross(self._up)).normalized()
        up = self._up.copy()
        matrix2 = Matrix44((side.x , -up.x , -fwd.x , 0.0) ,
                           (side.y , -up.y , -fwd.y , 0.0) ,
                           (side.z , -up.z , -fwd.z , 0.0) ,
                           (0.0    , 0.0   , 0.0    , 1.0))
        trans = Matrix44.translation (-self._pos.x,-self._pos.y,-self._pos.z);
        return  matrix2*trans ;
    def getRotationMatrix(self):
        fwd = self._dir.copy()
        side =(self._dir.cross(self._up)).normalized()
        up = self._up.copy()
        matrix2 = Matrix44((side.x , -up.x , -fwd.x , 0.0) ,
                           (side.y , -up.y , -fwd.y , 0.0) ,
                           (side.z , -up.z , -fwd.z , 0.0) ,
                           (0.0    , 0.0  , 0.0    , 1.0))
        return matrix2

