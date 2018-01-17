from math import sqrt,acos,pi
from decimal import Decimal,getcontext

getcontext().prec=30

class Vector(object):
    def __init__(self, coordinates):
        try:
            if not coordinates:
                raise ValueError
            self.coordinates = tuple([Decimal(x) for x in coordinates])
            self.dimension = len(coordinates)

        except ValueError:
            raise ValueError('The coordinates must be nonempty')

        except TypeError:
            raise TypeError('The coordinates must be an iterable')

    def __str__(self):
        return 'Vector: {}'.format(self.coordinates)

    def __eq__(self, v):
        return self.coordinates == v.coordinates

    def __add__(self, other):
        return [v1+v2 for v1,v2 in zip(self.coordinates,other.coordinates)]

    def __sub__(self, other):
        return [v1-v2 for v1,v2 in zip(self.coordinates,other.coordinates)]

    def __mul__(self, other):
        return [Decimal(other) * v for v in self.coordinates]

    def magnitude(self):
        return sqrt(sum([x**2 for x in self.coordinates]))

    def normalize(self):
        try:
            mag = self.magnitude()
            return Vector(self * (Decimal(1.0) / Decimal(mag)))
        except ZeroDivisionError:
            raise Exception('Cannot normalize the zero vector')

    def inner(self,other):
        return sum([v1*v2 for v1,v2 in zip(self.coordinates,other.coordinates)])

    def angle(self,other,degree=False):
        try:
            v1 = self.normalize()
            v2 = other.normalize()
            angle_in_rad = acos(round(v1.inner(v2),3))
            if degree:
                return angle_in_rad*180/pi
            else:
                return angle_in_rad
        except ZeroDivisionError:
            raise Exception('Cannot find angle of zero vector')

    def is_parallel(self,other):
        coordinates_divided = [round(v1/v2,3) for v1,v2 in zip(self.coordinates,other.coordinates)]
        return len(set(coordinates_divided)) <= 1

    def is_orthogonal(self,other):
        return round(self.inner(other),3) == 0

    def proj_onto(self,basis):
        return Vector(basis.normalize() * self.inner(basis.normalize())) 

    def find_perp(self,basis):
        return Vector(self - self.proj_onto(basis))


v = Vector([3.039,1.879])
b = Vector([0.825,2.036])

print ('v parallel: \n{}'.format(v.proj_onto(b)))

v = Vector([-9.88,-3.264,-8.159])
b = Vector([-2.155,-9.353,-9.473])

print ('v orthogonal: \n{}'.format(v.find_perp(b)))

v = Vector([3.009,-6.172,3.692,-2.51])
b = Vector([6.404,-9.144,2.759,8.718])

print ('v = \n{} + \n{}'.format(v.proj_onto(b),v.find_perp(b)))