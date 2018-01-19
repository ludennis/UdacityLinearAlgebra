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
    def __repr__(self):
        return 'Vector: {}'.format(self.coordinates)

    def __eq__(self, v):
        return self.coordinates == v.coordinates

    def __add__(self, other):
        return Vector([v1+v2 for v1,v2 in zip(self.coordinates,other.coordinates)])

    def __sub__(self, other):
        return Vector([v1-v2 for v1,v2 in zip(self.coordinates,other.coordinates)])

    def __mul__(self, other):
        return Vector([Decimal(other) * v for v in self.coordinates])

    def __getitem__(self,i):
        return self.coordinates[i]

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
        if self.is_zero_vector() or other.is_zero_vector(): 
            return True
        else:
            coordinates_divided = [round(v1/v2,2) if v2!=0 else 0 for v1,v2 in zip(self.coordinates,other.coordinates)]
            return len(set(coordinates_divided)) <= 1

    def is_orthogonal(self,other):
        if self.is_zero_vector() or other.is_zero_vector():
            return True
        else:
            return round(self.inner(other),2) == 0

    def proj_onto(self,basis):
        return Vector(basis.normalize() * self.inner(basis.normalize())) 

    def find_perp(self,basis):
        return Vector(self - self.proj_onto(basis))

    def cross_product(self,other):
        a_x,a_y,a_z = self.coordinates
        b_x,b_y,b_z = other.coordinates
        return Vector([a_y*b_z - a_z*b_y,
                       a_z*b_x - a_x*b_z,
                       a_x*b_y - a_y*b_x])

    def is_zero_vector(self):
        for v in self.coordinates:
            if v != 0: return False
        return True