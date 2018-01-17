import math
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
        sum=0
        for x in self.coordinates:
            sum += x*x
        return math.sqrt(sum)

    def normalize(self):
        mag = self.magnitude()
        return [v / mag for v in self.coordinates]

vector1 = Vector([-0.221,7.437])
print vector1.magnitude()

vector2 = Vector([8.813,-1.331,-6.247])
print vector2.magnitude()

vector3 = Vector([5.581,-2.136])
print vector3.normalize()

vector4 = Vector([1.996,3.108,-4.554])
print vector4.normalize()
