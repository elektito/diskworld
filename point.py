from vector import Vector

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

    def __sub__(self, p2):
        return Vector(self.x - p2.x, self.y - p2.y)

    def __add__(self, v):
        if not isinstance(v, Vector):
            raise TypeError("Only a vector can be added to a point.")

        return Point(self.x + v.x, self.y + v.y)

    def __eq__(self, p):
        if not isinstance(p, Point):
            raise TypeError("A point can only be compared with another point.")

        return self.x == p.x and self.y == p.y


    def __repr__(self):
        return "<Point ({}, {})>".format(self.x, self.y)
