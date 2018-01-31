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


    def multiply_coefficient_and_row(self, coefficient, row):
        self[row] = Plane(self[row].normal_vector * coefficient,self[row].constant_term*coefficient)


    def add_multiple_times_row_to_row(self, coefficient, row_to_add, row_to_be_added_to):
        self[row_to_be_added_to] = \
            Plane(self[row_to_be_added_to].normal_vector + (self[row_to_add].normal_vector * coefficient),
                  self[row_to_be_added_to].constant_term + (self[row_to_add].constant_term * coefficient))


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
            if self[cur_row].normal_vector.is_zero_vector(): return self
            if MyDecimal(self[cur_row].normal_vector[cur_dim]).is_near_zero():
                for other_row in range(cur_row,len(self)):
                    if not MyDecimal(self[other_row].normal_vector[cur_dim]).is_near_zero():
                        self.swap_rows(row1=cur_row,row2=other_row)
                        break
            self.multiply_coefficient_and_row(coefficient=Decimal(1.0)/self[cur_row].normal_vector[cur_dim],row=cur_row)
            for other_row in range(cur_row+1,len(self)):
                if not MyDecimal(self[other_row].normal_vector[cur_dim]).is_near_zero():
                    self.add_multiple_times_row_to_row(coefficient=self[other_row].normal_vector[cur_dim].copy_negate(),
                                                       row_to_add=cur_row,row_to_be_added_to=other_row)
        return self


    def compute_rref(self):
        tf = self.compute_triangular_form()
        for cur_row in range(1,len(tf)):
            if not tf[cur_row].normal_vector.is_zero_vector():
                cur_dim = cur_row if cur_row < tf.dimension else tf.dimension-1
                for row_above in range(0,cur_row):
                    tf.add_multiple_times_row_to_row(coefficient=tf[row_above].normal_vector[cur_dim].copy_negate(),
                                                       row_to_add=cur_row,row_to_be_added_to=row_above)
        return tf

class MyDecimal(Decimal):
    def is_near_zero(self, eps=1e-10):
        return abs(self) < eps

p1 = Plane(normal_vector=Vector([5.862,1.178,-10.366]),constant_term=-8.15)
p2 = Plane(normal_vector=Vector([-2.931,-0.589,5.183]),constant_term=-4.075)

s = LinearSystem([p1,p2])
r = s.compute_rref()
print(r)


p1 = Plane(normal_vector=Vector([8.631,5.112,-1.816]),constant_term=-5.113)
p2 = Plane(normal_vector=Vector([4.315,11.132,-5.27]),constant_term=-6.775)
p3 = Plane(normal_vector=Vector([-2.158,3.01,-1.727]),constant_term=-0.831)

s = LinearSystem([p1,p2,p3])
r = s.compute_rref()
print(r)


p1 = Plane(normal_vector=Vector([5.262,2.739,-9.878]),constant_term=-3.441)
p2 = Plane(normal_vector=Vector([5.111,6.358,7.638]),constant_term=-2.152)
p3 = Plane(normal_vector=Vector([2.016,-9.924,-1.367]),constant_term=-9.278)
p4 = Plane(normal_vector=Vector([2.167,-13.543,-18.883]),constant_term=-10.567)

s = LinearSystem([p1,p2,p3,p4])
r = s.compute_rref()
print(r)

# p1 = Plane(normal_vector=Vector(['1','1','1']), constant_term='1')
# p2 = Plane(normal_vector=Vector(['0','1','1']), constant_term='2')
# s = LinearSystem([p1,p2])
# r = s.compute_rref()
# if not (r[0] == Plane(normal_vector=Vector(['1','0','0']), constant_term='-1') and
#         r[1] == p2):
#     print ('test case 1 failed')

# p1 = Plane(normal_vector=Vector(['1','1','1']), constant_term='1')
# p2 = Plane(normal_vector=Vector(['1','1','1']), constant_term='2')
# s = LinearSystem([p1,p2])
# r = s.compute_rref()
# if not (r[0] == p1 and
#         r[1] == Plane(constant_term='1')):
#     print ('test case 2 failed')

# p1 = Plane(normal_vector=Vector(['1','1','1']), constant_term='1')
# p2 = Plane(normal_vector=Vector(['0','1','0']), constant_term='2')
# p3 = Plane(normal_vector=Vector(['1','1','-1']), constant_term='3')
# p4 = Plane(normal_vector=Vector(['1','0','-2']), constant_term='2')
# s = LinearSystem([p1,p2,p3,p4])
# r = s.compute_rref()
# if not (r[0] == Plane(normal_vector=Vector(['1','0','0']), constant_term='0') and
#         r[1] == p2 and
#         r[2] == Plane(normal_vector=Vector(['0','0','-2']), constant_term='2') and
#         r[3] == Plane()):
#     print ('test case 3 failed')

# p1 = Plane(normal_vector=Vector(['0','1','1']), constant_term='1')
# p2 = Plane(normal_vector=Vector(['1','-1','1']), constant_term='2')
# p3 = Plane(normal_vector=Vector(['1','2','-5']), constant_term='3')
# s = LinearSystem([p1,p2,p3])
# r = s.compute_rref()
# if not (r[0] == Plane(normal_vector=Vector(['1','0','0']), constant_term=Decimal('23')/Decimal('9')) and
#         r[1] == Plane(normal_vector=Vector(['0','1','0']), constant_term=Decimal('7')/Decimal('9')) and
#         r[2] == Plane(normal_vector=Vector(['0','0','1']), constant_term=Decimal('2')/Decimal('9'))):
#     print ('test case 4 failed')