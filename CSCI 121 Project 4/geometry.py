import random
import math

#
# geometry.py
#
# This defines three classes that we use to track bodies that
# occupy the world of a simulation. Bodies inhabit a 2-D
# world at a position, have a velocity (a heading and a speed),
# and they are compelled (by their behavior) to change their
# heading. They also live within the bounds of the world.
#
# We define the classes
#
#   Point2D: for tracking a location of a body
#   Vector2D: for tracking the velocity and acceleration of a body; 
#     also used to talk about positions of bodies relative to others
#   bounds: used to track a rectangular region in the world
#
# These are described more carefully in the project description.
# The key methods are the "arithmetic" operations we define for
# working with Point2D and Vector2D. They are the following:
#
#   p + v : a point that is at vector offset v from a point p
#   v + w : a vector that is a combination of vectors v and w
#   p - q : the vector offset that thakes you from point q to point p
#   -v : a vector in the opposite heading of vector v
#   v * s : a vector whose length is scaled up by the float factor s
#   v / s : a vector whose length is scaled down by the float factor s
#   v - w : vector difference (same as v + (-w))
#
# We also support:
#
#   v.magnitude() : the length of vector v
#   v.direction() : a unit-length vector in the direction of v
#   v.dot(w) : the dot product of v with w (see the description, a float)
#   v.cross(w) : the cross product (or turn) of v with w (a float)
#
# Finally, we have a 'bounds' class for operating on points within a 2-D
# rectangular region.
#

class Point2D:

    @classmethod
    def random(cls, bounds):
        return bounds.point_at(random.random(),random.random())

    def __init__(self, xCoord=0.0, yCoord=0.0):
        self.x = xCoord
        self.y = yCoord

    def copy(self):
        return Point2D(self.x, self.y)

    def plus(self, offset):
        assert(type(offset) == Vector2D)
        return Point2D(self.x+offset.dx, self.y+offset.dy)

    def minus(self, arg):
        if type(arg) == Vector2D:
            offset = arg
            return Point2D(self.x-offset.dx, self.y-offset.dy)
        elif type(arg) == Point2D:
            other = arg
            return Vector2D(self.x-other.x, self.y-other.y)
        else:
            assert(type(arg) == Vector2D or type(arg) == Point2D)

    def get(self,coord):
        assert(coord == 0 or coord == 1 or coord == 'x' or coord == 'y')
        if coord == 0 or coord == 'x':
            return self.x
        else:
            return self.y

    def to_string(self):
        return "<P X="+str(self.x)+", Y="+str(self.y)+">"

    __add__  = plus
    __sub__  = minus
    __str__  = to_string
    __repr__ = to_string
    __getitem__ = get


class Vector2D:

    EPSILON = 0.000001

    @classmethod
    def random(cls,length = 1.0):
        angle = random.random() * 2 * math.pi
        return Vector2D(math.cos(angle), math.sin(angle)) * length

    def __init__(self, xOffset=0.0, yOffset=0.0):
        self.dx = xOffset
        self.dy = yOffset

    def perp(self):
        return Vector2D(-self.dy, self.dx)

    def cross(self, vec):
        assert(type(vec) == Vector2D)
        return self.dx*vec.dy - self.dy*vec.dx

    def dot(self, vec):
        assert(type(vec) == Vector2D)
        return self.dx*vec.dx + self.dy*vec.dy

    def plus(self, vec):
        assert(type(vec) == Vector2D)
        return Vector2D(self.dx+vec.dx, self.dy+vec.dy)

    def minus(self, vec):
        assert(type(vec) == Vector2D)
        return Vector2D(self.dx-vec.dx, self.dy-vec.dy)

    def negated(self):
        return Vector2D(0.0-self.dx, 0.0-self.dy)

    def times(self, amount):
        assert(type(amount) == float)
        return Vector2D(amount*self.dx, amount*self.dy)

    def over(self, amount):
        assert(type(amount) == float)
        return Vector2D(self.dx/amount, self.dy/amount)

    def magnitude(self):
        return math.sqrt(self.dot(self))

    def direction(self):
        mag = self.magnitude()
        if mag > Vector2D.EPSILON:
            return self.over(mag)
        else:
            # return 0 vector if we are dividing by 0
            return Vector2D()

    def to_string(self):
        return "<V DX="+str(self.dx)+", DY="+str(self.dy)+">"
    
    __add__ = plus
    __sub__ = minus
    __neg__ = negated
    __mul__ = times
    __rmul__ = times
    __div__ = over
    x = cross
    __str__ = to_string
    __repr__ = to_string


class Bounds:

    def __init__(self,x0,y0,x1,y1):
        self.xmin = min(x0,x1)        
        self.xmax = max(x0,x1)
        self.ymin = min(y0,y1)        
        self.ymax = max(y0,y1)

    def width(self):
        return self.xmax - self.xmin

    def height(self):
        return self.ymax - self.ymin

    def point_at(self,fractionx,fractiony):
        x = self.xmin + fractionx * self.width()
        y = self.ymin + fractiony * self.height()
        return Point2D(x,y)

    def wrap(self,position):
        p = position.copy()
        while p.x >= self.xmax:
            p.x -= self.width()
        while p.x < self.xmin:
            p.x += self.width()
        while p.y >= self.ymax:
            p.y -= self.height()
        while p.y < self.ymin:
            p.y += self.height()
        return p

    def clip(self,position):
        p = position.copy()
        if p.x >= self.xmax:
            p.x = self.xmax
        if p.x < self.xmin:
            p.x = self.xmin
        while p.y >= self.ymax:
            p.y = self.ymax
        while p.y < self.ymin:
            p.y = self.ymin
        return p
        
