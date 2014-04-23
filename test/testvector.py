import unittest
from math import pi, tan
from vector import Vector
from point import Point

class TestVector(unittest.TestCase):
    def test_equality(self):
        v1 = Vector(1.000000001, 2.333)
        v2 = Vector(1.000000002, 2.333)
        v3 = Vector(1.000000001, 2.334)
        self.assertEqual(v1, v2)
        self.assertNotEqual(v1, v3)

    def test_addition(self):
        v1 = Vector(-2, 11)
        v2 = Vector(5, 4)
        result = Vector(3, 15)
        self.assertEqual(v1 + v2, result)

    def test_subtraction(self):
        v1 = Vector(4, 8)
        v2 = Vector(7, 5)
        result = Vector(-3, 3)
        self.assertEqual(v1 - v2, result)

    def test_addition_to_point(self):
        p = Point(4, 9)
        v = Vector(3, 1)
        result = Point(7, 10)
        self.assertEqual(p + v, result)

    def test_dot_product(self):
        v1 = Vector(3, 7)
        v2 = Vector(9, 11)
        result = 3 * 9 + 7 * 11
        self.assertEqual(v1 * v2, result)

    def test_length(self):
        v = (3, 4)
        result = 5
        self.assertEqual(len(v), result)

    def test_angle(self):
        v1 = Vector(1, 1)
        v2 = Vector(1, tan(pi / 6))
        v3 = Vector(1, 0)
        self.assertAlmsotEqual(v1.theta, pi / 4)
        self.assertAlmsotEqual(v2.theta, pi / 6)
        self.assertAlmsotEqual(v3.theta, pi / 2)

    def test_projection(self):
        self.assertEqual(v1.project(v2), result)
