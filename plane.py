from decimal import Decimal, getcontext

from vector import Vector

getcontext().prec = 30


class Plane(object):

    NO_NONZERO_ELTS_FOUND_MSG = 'No nonzero elements found'

    def __init__(self, normal_vector=None, constant_term=None):
        self.dimension = 3

        if not normal_vector:
            all_zeros = ['0']*self.dimension
            normal_vector = Vector(all_zeros)
        self.normal_vector = normal_vector

        if not constant_term:
            constant_term = Decimal('0')
        self.constant_term = Decimal(constant_term)

        self.set_basepoint()


    def set_basepoint(self):
        try:
            n = self.normal_vector
            c = self.constant_term
            basepoint_coords = ['0']*self.dimension

            initial_index = Plane.first_nonzero_index(n)
            initial_coefficient = n[initial_index]

            basepoint_coords[initial_index] = c/initial_coefficient
            self.basepoint = Vector(basepoint_coords)

        except Exception as e:
            if str(e) == Plane.NO_NONZERO_ELTS_FOUND_MSG:
                self.basepoint = Vector(['0']*self.dimension)
            else:
                raise e


    def is_parallel(self,other):
        return self.normal_vector.is_parallel(other.normal_vector)

    def __eq__(self,other):
        vector_in_between = self.basepoint - other.basepoint
        return True if vector_in_between.is_zero_vector() \
            else self.is_parallel(other) and vector_in_between.is_orthogonal(self.normal_vector) \
                                         and vector_in_between.is_orthogonal(other.normal_vector)

    def __str__(self):

        num_decimal_places = 3

        def write_coefficient(coefficient, is_initial_term=False):
            coefficient = round(coefficient, num_decimal_places)
            if coefficient % 1 == 0:
                coefficient = int(coefficient)

            output = ''

            if coefficient < 0:
                output += '-'
            if coefficient > 0 and not is_initial_term:
                output += '+'

            if not is_initial_term:
                output += ' '

            if abs(coefficient) != 1:
                output += '{}'.format(abs(coefficient))

            return output

        n = self.normal_vector

        try:
            initial_index = Plane.first_nonzero_index(n)
            terms = [write_coefficient(n[i], is_initial_term=(i==initial_index)) + 'x_{}'.format(i+1)
                     for i in range(self.dimension) if round(n[i], num_decimal_places) != 0]
            output = ' '.join(terms)

        except Exception as e:
            if str(e) == self.NO_NONZERO_ELTS_FOUND_MSG:
                output = '0'
            else:
                raise e
        
        if MyDecimal(self.constant_term).is_near_zero():
            constant = 0
        else: constant = round(self.constant_term, num_decimal_places)
        if constant % 1 == 0:
            constant = int(constant)
        output += ' = {}'.format(constant)

        return output


    @staticmethod
    def first_nonzero_index(iterable):
        for k, item in enumerate(iterable):
            if not MyDecimal(item).is_near_zero():
                return k
        raise Exception(Plane.NO_NONZERO_ELTS_FOUND_MSG)


class MyDecimal(Decimal):
    def is_near_zero(self, eps=1e-10):
        return abs(self) < eps

# plane1 = Plane(Vector([-0.412,3.806,0.728]),-3.46)
# plane2 = Plane(Vector([1.03,-9.515,-1.82]),8.65)

# print(plane1==plane2)
# print(plane1.is_parallel(plane2))


# plane3 = Plane(Vector([2.611,5.528,0.283]),4.6)
# plane4 = Plane(Vector([7.715,8.306,5.342]),3.76)

# print(plane3==plane4)
# print(plane3.is_parallel(plane4))


# plane5 = Plane(Vector([-7.926,8.625,-7.217]),-7.952)
# plane6 = Plane(Vector([-2.642,2.875,-2.404]),-2.443)

# print(plane5==plane6)
# print(plane5.is_parallel(plane6))
