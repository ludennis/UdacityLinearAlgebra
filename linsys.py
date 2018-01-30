from decimal import Decimal, getcontext
from copy import deepcopy

from vector import Vector
from plane import Plane

getcontext().prec = 30


class LinearSystem(object):

    ALL_PLANES_MUST_BE_IN_SAME_DIM_MSG = 'All planes in the system should live in the same dimension'
    NO_SOLUTIONS_MSG = 'No solutions'
    INF_SOLUTIONS_MSG = 'Infinitely many solutions'

    def __init__(self, planes):
        try:
            d = planes[0].dimension
            for p in planes:
                assert p.dimension == d

            self.planes = planes
            self.dimension = d

        except AssertionError:
            raise Exception(self.ALL_PLANES_MUST_BE_IN_SAME_DIM_MSG)


    def swap_rows(self, row1, row2):
        self[row1],self[row2] = self[row2],self[row1]
        # print('{} swapped with {}'.format(row1,row2))


    def multiply_coefficient_and_row(self, coefficient, row):
        self[row] = Plane(self[row].normal_vector * coefficient,self[row].constant_term*coefficient)
        #print('row {} multiplied with coefficient {}'.format(row,coefficient))


    def add_multiple_times_row_to_row(self, coefficient, row_to_add, row_to_be_added_to):
        self[row_to_be_added_to] = \
            Plane(self[row_to_be_added_to].normal_vector + self[row_to_add].normal_vector * coefficient,
                  self[row_to_be_added_to].constant_term + self[row_to_add].constant_term * coefficient)
        #print('row {} multiplied with coefficient {} and added to {}'.format(row_to_add,coefficient,row_to_be_added_to))


    def indices_of_first_nonzero_terms_in_each_row(self):
        num_equations = len(self)
        num_variables = self.dimension

        indices = [-1] * num_equations

        for i,p in enumerate(self.planes):
            try:
                indices[i] = p.first_nonzero_index(p.normal_vector)
            except Exception as e:
                if str(e) == Plane.NO_NONZERO_ELTS_FOUND_MSG:
                    continue
                else:
                    raise e

        return indices

    def __len__(self):
        return len(self.planes)


    def __getitem__(self, i):
        return self.planes[i]


    def __setitem__(self, i, x):
        try:
            assert x.dimension == self.dimension
            self.planes[i] = x

        except AssertionError:
            raise Exception(self.ALL_PLANES_MUST_BE_IN_SAME_DIM_MSG)


    def __str__(self):
        ret = 'Linear System:\n'
        temp = ['Equation {}: {}'.format(i+1,p) for i,p in enumerate(self.planes)]
        ret += '\n'.join(temp)
        return ret

    def compute_triangular_form(self):
        for cur_row in range(0,len(self)):
            cur_dim = cur_row if cur_row < self.dimension else self.dimension-1
            # print ('cur_row {}, plane {}, dimension {}'.format(cur_row,self[cur_row],self.dimension))
            #swap if leading coefficient of cur_row is 0
            if self[cur_row].normal_vector.is_zero_vector(): return self
            if self[cur_row].normal_vector[cur_dim] == 0:
                for other_row in range(cur_row,len(self)):
                    # print('other_row {}\n'.format(self[other_row]))
                    if self[other_row].normal_vector[cur_dim] != 0:
                        self.swap_rows(row1=cur_row,row2=other_row)
                        break
            # print('operating on plane {}'.format(self[cur_row]))
            #reduce to coefficient of 1 and then reduce other planes
            self.multiply_coefficient_and_row(coefficient=Decimal(1.0)/self[cur_row].normal_vector[cur_dim],row=cur_row)
            #reduce other rows
            for other_row in range(cur_row+1,len(self)):
                # print ('other_row {}: {}\n'.format(other_row,self[other_row]))
                if (self[other_row].normal_vector[cur_dim]!=0):
                    self.add_multiple_times_row_to_row(coefficient=-1*self[other_row].normal_vector[cur_dim],
                                                       row_to_add=cur_row,row_to_be_added_to=other_row)
            # print('{}\n'.format(self))
        return self


class MyDecimal(Decimal):
    def is_near_zero(self, eps=1e-10):
        return abs(self) < eps


p1 = Plane(normal_vector=Vector(['1','1','1']), constant_term='1')
p2 = Plane(normal_vector=Vector(['0','1','1']), constant_term='2')
s = LinearSystem([p1,p2])
t = s.compute_triangular_form()
if not (t[0] == p1 and
        t[1] == p2):
    print ('test case 1 failed')

p1 = Plane(normal_vector=Vector(['1','1','1']), constant_term='1')
p2 = Plane(normal_vector=Vector(['1','1','1']), constant_term='2')
s = LinearSystem([p1,p2])
t = s.compute_triangular_form()
if not (t[0] == p1 and
        t[1] == Plane(constant_term='1')):
    print ('test case 2 failed')

p1 = Plane(normal_vector=Vector(['1','1','1']), constant_term='1')
p2 = Plane(normal_vector=Vector(['0','1','0']), constant_term='2')
p3 = Plane(normal_vector=Vector(['1','1','-1']), constant_term='3')
p4 = Plane(normal_vector=Vector(['1','0','-2']), constant_term='2')
s = LinearSystem([p1,p2,p3,p4])

t = s.compute_triangular_form()
if not (t[0] == p1 and
        t[1] == p2 and
        t[2] == Plane(normal_vector=Vector(['0','0','-2']), constant_term='2') and
        t[3] == Plane()):
    print ('test case 3 failed')

p1 = Plane(normal_vector=Vector(['0','1','1']), constant_term='1')
p2 = Plane(normal_vector=Vector(['1','-1','1']), constant_term='2')
p3 = Plane(normal_vector=Vector(['1','2','-5']), constant_term='3')
s = LinearSystem([p1,p2,p3])
t = s.compute_triangular_form()
if not (t[0] == Plane(normal_vector=Vector(['1','-1','1']), constant_term='2') and
        t[1] == Plane(normal_vector=Vector(['0','1','1']), constant_term='1') and
        t[2] == Plane(normal_vector=Vector(['0','0','-9']), constant_term='-2')):
    print ('test case 4 failed')