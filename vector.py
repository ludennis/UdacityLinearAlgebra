from math import sqrt,acos,pi

class Vector(object):
    def __init__(self, coordinates):
        try:
            if not coordinates:
                raise ValueError
            self.coordinates = tuple(coordinates)
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
        return [other * v for v in self.coordinates]

    def magnitude(self):
        return sqrt(sum([x**2 for x in self.coordinates]))

    def normalize(self):
        try:
            mag = self.magnitude()
            return Vector(self * (1 / mag))
        except ZeroDivisionError:
            raise Exception('Cannot normalize the zero vector')

    def inner(self,other):
        return sum([v1*v2 for v1,v2 in zip(self.coordinates,other.coordinates)])

    def angle(self,other,degree=False):
        try:
            angle_in_rad = acos((self.normalize()).inner(other.normalize()))
            if degree:
                return angle_in_rad*180/pi
            else:
                return angle_in_rad
        except ZeroDivisionError:
            raise Exception('Cannot find angle of zero vector')

vector1 = Vector([7.887,4.138])
vector2 = Vector([-8.802,6.776])

print (vector1.inner(vector2))

vector1 = Vector([-5.955,-4.904,-1.874])
vector2 = Vector([-4.496,-8.755,7.103])

print (vector1.inner(vector2))

vector1 = Vector([3.183,-7.627])
vector2 = Vector([-2.668,5.319])

print (vector1.angle(vector2))

vector1 = Vector([7.35,0.221,5.188])
vector2 = Vector([2.751,8.259,3.985])

print (vector1.angle(vector2,True))