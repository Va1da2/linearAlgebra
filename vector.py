from math import sqrt, acos, pi
from decimal import Decimal, getcontext

class Vector(object):

    CANNOT_NORMALIZE_ZERO_VECTOR_MSG = 'Cannot normalize the zero vector'
    NO_UNIQUE_PARALLEL_COMPONEN_MSG = 'There is no unique parallel vector to a zero vector'
    NO_UNIQUE_ORTHOGONAL_COMPONENT_MSG = ' There is no unique orthogonal component'
    ONLY_DEFINED_IN_TWO_TRHEE_DIMS_MSG = 'Operation is defined only int three or two dimensions'

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

    def plus(self, v):
        new_coordinates = [x+y for x, y in zip(self.coordinates, v.coordinates)]
        return Vecotr(new_coordinates)

    def minus(self, v):
        new_coordinates = [x-y for x,y in zip(self.coordinates, v.coordinates)]
        return Vector(new_coordinates)
    
    def times_scalar(self, c):
        new_coordinates = [Decimal(c) * x for x in self.coordinates]
        return Vector(new_coordinates)

    def magnitude(self):
        return Decimal(sqrt(sum([x*x for x in self.coordinates])))

    def normalize(self):
        try:
            magnitude = self.magnitude()
            return self.times_scalar(Decimal('1.0') / self.magnitude())
        except ZeroDivisionError:
            raise Exception(self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG)

    def dot(self, v):
        return sum([x*y for x,y in zip(self.coordinates, v.coordinates)])

    def angle_with(self, v, in_degrees=False):
        try:
            u1 = self.normalize()
            u2 = v.normalize()
            angle_in_radians = acos(u1.dot(u2))

            if in_degrees:
                degrees_per_radian = Decimal('180.0') / pi
                return angle_in_radians * degrees_per_radian
            else:
                return angle_in_radians

        except Exception as e:
            if str(e) ==self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG:
                raise Exception('Cannot compute an angle with the zero vector')
            else:
                raise e

    def is_orthogonal_to(self, v, tolerance=1e-10):
        return abs(self.dot(v)) < tolerance

    def is_zero(self, tolerance=1e-10):
        return self.magnitude() < tolerance

    def is_parallel_to(self, v):
        return ( self.is_zero() or
                v.is_zero() or
                self.angle_with(v) == 0 or
                self.angle_with(v) == pi )

    def component_parallel_to(self, basis):
        try:
            u = basis.normalize()
            weight = self.dot(u)
            return u.times_scala(weight)

        except Exception as e:
            if str(e) == self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG:
                raise Exception(self.NO_UNIQUE_PARALLEL_COMPONEN_MSG)
            else:
                raise e


    def component_orthogonal_to(self, basis):
        try:
            projection = self.component_parallel_to(basis)
            return self.minus(projection)

        except Exception as e:
            if str(e) == self.NO_UNIQUE_PARALLEL_COMPONEN_MSG:
                raise Exception(self.NO_UNIQUE_ORTHOGONAL_COMPONENT_MSG)
            else:
                raise e

    def cross(self, v):
        try:
            x_1, y_1, z_1 = self.coordinates
            x_2, y_2, z_2 = v.coordinates
            new_coordinates = [ y_1 * z_2 - y_2 * z_1,
                                -( x_1 * z_2 - x_2 * z_1 ),
                                x_1 * y_2 - x_2 * y_1 ]
            return Vector(new_coordinates)

        except ValueError as e:
            msg = str(e)
            if msg == 'need more than 2 values to unpack':
                self_embedded_in_R3 = Vector(self.coordinates + ('0',))
                v_embedded_in_R3 = Vector(v.coordinates + ('0',))
                return self_embedded_in_R3.cross(v_embedded_in_R3)
            elif (msg == 'too many values to unpack' or 
                    msg == 'need more than 1 value to unpack'):
                raise Exception('self.ONLY_DEFINED_IN_TWO_TRHEE_DIMS_MSG')
            else:
                raise e

    def area_parallelogram(self, v):
        return self.cross(v).magnitude()

    def area_triangle(self, v):
        return self.area_parallelogram(v) * Decimal('0.5')


        