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

    def parallel(self,other):
        return self.normalize() == other.normalize()


vector1 = Vector([3,3])
vector2 = Vector([6,6])

print (vector1.parallel(vector2))