import math
from vector3 import *

EPSILON = 0.001

class Quaternion:
    __slots__ = ('_q')
    
    def __init__(self,*args):
        if not args:
            self._q = map(float,[0.0, 0.0, 0.0, 0.0])
            return
        if len(args)==4:
            self._q = map(float,args[:4])
        elif len(args)==2:
            sine = math.sin(float(args[1])*0.5)
            cosine = math.cos(float(args[1])*0.5)
            v = map(lambda x: float(x)*sine,args[0][:3])
            v.append(cosine)
            self._q = v;
        elif len(args)==1:
            self._q = map(float,args[0]._q[:4])
        else:
            raise ValueError("Quaternion constructor can only receive 0,1,2 or 4 args")
    def _get_x(self):
        return self._q[0]
    def _get_y(self):
        return self._q[1]
    def _get_z(self):
        return self._q[2]
    def _get_w(self):
        return self._q[3]
    
    def _set_x(self, x):
        assert isinstance(x, float), "Must be a float"
        self._q[0] = x
    def _set_y(self, y):
        assert isinstance(y, float), "Must be a float"
        self._q[1] = y
    def _set_z(self, z):
        assert isinstance(z, float), "Must be a float"
        self._q[2] = z
    def _set_w(self, w):
        assert isinstance(w, float), "Must be a float"
        self._q[3] = w
        
    x = property(_get_x,_set_x,None,"x component")
    y = property(_get_y,_set_y,None,"y component")
    z = property(_get_z,_set_z,None,"z component")
    w = property(_get_w,_set_w,None,"w component")
    
    def copy(self):
        return Quaternion(self)
    
    def length2(self):
        return reduce(lambda x,y: x+y , map(lambda x: x*x , self._q) )
    def length(self):
        return math.sqrt(self.length2())
    def normalize(self):
        l = self.length()
        try:
            self._q = map(lambda x: x/l , self._q)
        except ZeroDivisionError:
            self._q = [0.,0.,0.,0.]
    def normalized(self):
        q = Quaternion(self)
        q.normalize()
        return q
    def conjugate(self):
        self._q = [-self._q[0],-self._q[1],-self._q[2],self._q[3]]
    def inverse(self):
        self.conjugate()
        l2 = self.length2()
        try:
            self._q = map(lambda x: x/l2 , self._q)
        except ZeroDivisionError:
            self._q = [0.,0.,0.,0.]
    def __mul__(q1,q2):
        return Quaternion(q1.y * q2.z - q1.z * q2.y + q1.w * q2.x + q1.x * q2.w,
		               q1.z * q2.x - q1.x * q2.z + q1.w * q2.y + q1.y * q2.w,
					   q1.x * q2.y - q1.y * q2.x + q1.w * q2.z + q1.z * q2.w,
					   q1.w * q2.w - q1.x * q2.x - q1.y * q2.y - q1.z * q2.z)

if __name__=="__main__":
    print "Quaternion test"
    q = Quaternion(1,2,3,4)
    qq = Quaternion(q);
    qq._q[1]=0
    print qq._q
    v = Vector3(2.0,4.0,5.0)
    q2 = Quaternion(v,2.0)
    print q2._q , q2.length2()
    q3 = q2.copy();
    q2.inverse()
    print q2._q
    print q3._q
    
    print (q2*q3)._q
    
    raw_input()
