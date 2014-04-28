from math import sqrt, atan2, sin, cos
from numbers import Number

class Vector:
    def __init__(self, x=None, y=None, magnitude=None, angle=None):
        if x is not None and y is not None:
            self.x = x
            self.y = y
        elif magnitude is not None and angle is not None:
            self.x = magnitude * cos(angle)
            self.y = magnitude * sin(angle)
        else:
            raise TypeError(
                "Either cartesian or polar coordinates must be"
                "specified when creating a vector.")

    @property
    def magnitude(self):
        return sqrt(self.x ** 2 + self.y ** 2)

    @property
    def angle(self):
        return atan2(self.y, self.x)

    def project(self, v):
        return v * (self * v / v.magnitude ** 2)

    def __getitem__(self, index):
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        else:
            raise IndexError("Point index can be either 0 or 1.")

    def __setitem__(self, index, value):
        if index == 0:
            self.x = value
        elif index == 1:
            self.y = value
        else:
            raise IndexError("Point index can be either 0 or 1.")

    def __sub__(self, v2):
        return Vector(self.x - v2.x, self.y - v2.y)

    def __add__(self, v2):
        return Vector(self.x + v2.x, self.y + v2.y)

    def __eq__(self, v2):
        if not isinstance(v2, Vector):
            raise TypeError("A vector can only be compared with another vector.")

        return round(self.x) == round(v2.x) and \
            round(self.y) == round(v2.y)

    def __mul__(self, arg):
        if not isinstance(arg, (Vector, Number)):
            raise TypeError("A vector can only be dot-multiplied with another vector or a scalar.")

        if isinstance(arg, Vector):
            return self.x * arg.x + self.y * arg.y
        else:
            return Vector(self.x * arg, self.y * arg)

    def __rmul__(self, arg):
        return Vector(self.x * arg, self.y * arg)

    def __div__(self, scalar):
        return self * (1.0 / scalar)

    def __neg__(self):
        return self * -1

    def __repr__(self):
        return "<Vector ({}, {})>".format(self.x, self.y)
