from vector import Vector
from helpers import float_eq

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __getitem__(self, index):
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        else:
            raise IndexError("Vector index can be either 0 or 1.")

    def __setitem__(self, index, value):
        if index == 0:
            self.x = value
        elif index == 1:
            self.y = value
        else:
            raise IndexError("Vector index can be either 0 or 1.")

    def __sub__(self, arg):
        if isinstance(arg, Point):
            return Vector(self.x - arg.x, self.y - arg.y)
        else:
            return Point(self.x - arg.x, self.y - arg.y)

    def __add__(self, v):
        if not isinstance(v, Vector):
            raise TypeError("Only a vector can be added to a point.")

        return Point(self.x + v.x, self.y + v.y)

    def __eq__(self, p):
        if not isinstance(p, Point):
            raise TypeError("A point can only be compared with another point.")

        return float_eq(self.x, p.x) and float_eq(self.y, p.y)

    def __repr__(self):
        return "<Point ({}, {})>".format(self.x, self.y)
