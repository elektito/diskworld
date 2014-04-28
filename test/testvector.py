import unittest
from math import pi, tan, sin, cos
from vector import Vector
from point import Point

class TestVector(unittest.TestCase):
    def test_accessors(self):
        v = Vector(11, 12)
        self.assertEqual(v.x, 11)
        self.assertEqual(v.y, 12)
        self.assertEqual(v[0], 11)
        self.assertEqual(v[1], 12)

        v[0] = 13
        self.assertEqual(v.x, 13)
        v[1] = -7
        self.assertEqual(v.y, -7)

        v.x = 1
        self.assertEqual(v[0], 1)
        v.y = 0
        self.assertEqual(v[1], 0)

    def test_init_with_polar_coordintates(self):
        v1 = Vector(magnitude=2, angle=pi/3)
        v2 = Vector(2*cos(pi/3), 2*sin(pi/3))
        self.assertEqual(v1, v2)

    def test_invalid_initialization(self):
        with self.assertRaises(TypeError):
            v = Vector()

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

    def test_multiplication_with_scalar(self):
        v = Vector(4, 5)
        scalar = 2
        result = Vector(8, 10)
        self.assertEqual(v * scalar, result)

    def test_reverse_multiplication_with_scalar(self):
        v = Vector(4, 5)
        scalar = 2
        result = Vector(8, 10)
        self.assertEqual(scalar * v, result)

    def test_division_by_scalar(self):
        v = Vector(8, 4)
        scalar = 2
        result = Vector(4, 2)
        self.assertEqual(v / scalar, result)

    def test_negation(self):
        v = Vector(4, -3)
        result = Vector(-4, 3)
        self.assertEqual(-v, result)

    def test_length(self):
        v = Vector(3, 4)
        result = 5
        self.assertEqual(v.magnitude, result)

    def test_angle(self):
        v1 = Vector(1, 1)
        v2 = Vector(1, tan(pi / 6))
        v3 = Vector(0, 1)
        v4 = Vector(-1, -1)
        self.assertAlmostEqual(v1.angle, pi / 4)
        self.assertAlmostEqual(v2.angle, pi / 6)
        self.assertAlmostEqual(v3.angle, pi / 2)
        self.assertAlmostEqual(v4.angle, pi * -0.75)

    def test_projection(self):
        v1 = Vector(1, 2)
        v2 = Vector(3, 4)
        #result = 9 / 5 * Vector(3, 4)
        result = Vector(33.0 / 25, 44.0 / 25)
        self.assertEqual(v1.project(v2), result)
