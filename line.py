from decimal import Decimal, getcontext

from vector import Vector

getcontext().prec = 30


class Line(object):

    NO_NONZERO_ELTS_FOUND_MSG = 'No nonzero elements found'

    def __init__(self, normal_vector=None, constant_term=None):
        self.dimension = 2

        if not normal_vector:
            all_zeros = ['0']*self.dimension
            normal_vector = Vector(all_zeros)
        self.normal_vector = normal_vector

        if not constant_term:
            constant_term = Decimal('0.000')
        self.constant_term = Decimal(constant_term)

        self.set_basepoint()


    def set_basepoint(self):
        try:
            n = self.normal_vector
            c = self.constant_term
            basepoint_coords = ['0']*self.dimension

            initial_index = Line.first_nonzero_index(n)
            initial_coefficient = n[initial_index]

            basepoint_coords[initial_index] = c/Decimal(initial_coefficient)
            self.basepoint = Vector(basepoint_coords)

        except Exception as e:
            if str(e) == Line.NO_NONZERO_ELTS_FOUND_MSG:
                self.basepoint = None
            else:
                raise e


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
            initial_index = Line.first_nonzero_index(n)
            terms = [write_coefficient(n[i], is_initial_term=(i==initial_index)) + 'x_{}'.format(i+1)
                     for i in range(self.dimension) if round(n[i], num_decimal_places) != 0]
            output = ' '.join(terms)

        except Exception as e:
            if str(e) == self.NO_NONZERO_ELTS_FOUND_MSG:
                output = '0'
            else:
                raise e

        constant = round(self.constant_term, num_decimal_places)
        if constant % 1 == 0:
            constant = int(constant)
        output += ' = {}'.format(constant)

        return output

    def is_parallel(self,other):
        return self.normal_vector.is_parallel(other.normal_vector)

    def is_incidental(self,other):
        vector_in_between = self.basepoint - other.basepoint
        #check to see if vector in between is orthogonal to both the normal vectors of each
        if self.is_parallel(other) and vector_in_between.is_orthogonal(self.normal_vector) and vector_in_between.is_orthogonal(other.normal_vector):
           return True
        else: return False

    def intercept(self,other):
        # check if two normal vectors are parallel
        if self.is_parallel(other):
            print ('Both lines are parallel')
            if self.is_incidental(other):
                print ('Both lines are incidental')
        else:
            #not parallel, need to find intercept
            # |A|   |c|
            # |B| x |y| = k1 
            #   
            # |C|   |x|
            # |D| x |y| = k2
            #
            # x = (Dk1 - Bk2)/(AD-BC)
            # y = (-Ck1 + Ak2)/(AD-BC)
            self_norm,targ_norm=self.normal_vector,other.normal_vector

            A,B,k1 = self_norm[0],self_norm[1],self.constant_term
            C,D,k2 = targ_norm[0],targ_norm[1],other.constant_term

            x = (D * k1 - B * k2) / (A * D - B * C)
            y = (-C * k1 + A * k2) / (A * D - B * C)
            return tuple([x,y])

    @staticmethod
    def first_nonzero_index(iterable):
        for k, item in enumerate(iterable.coordinates):
            if not MyDecimal(item).is_near_zero():
                return k
        raise Exception(Line.NO_NONZERO_ELTS_FOUND_MSG)


class MyDecimal(Decimal):
    def is_near_zero(self, eps=1e-10):
        return abs(self) < eps


line1 = Line(Vector([4.046,2.836]),1.21)
line2 = Line(Vector([10.115,7.09]),3.025)

print (line1.intercept(line2))

line3 = Line(Vector([7.204,3.182]),8.68)
line4 = Line(Vector([8.172,4.114]),9.883)

print (line3.intercept(line4))

line5 = Line(Vector([1.182,5.562]),6.744)
line6 = Line(Vector([1.773,8.343]),9.525)

print (line5.intercept(line6))
