import unittest
from point import Point
from vector import Vector

class TestPoint(unittest.TestCase):
    def test_accessors(self):
        p = Point(11, 12)
        self.assertEqual(p.x, 11)
        self.assertEqual(p.y, 12)
        self.assertEqual(p[0], 11)
        self.assertEqual(p[1], 12)

        p[0] = 13
        self.assertEqual(p.x, 13)
        p[1] = -7
        self.assertEqual(p.y, -7)

        p.x = 1
        self.assertEqual(p[0], 1)
        p.y = 0
        self.assertEqual(p[1], 0)

    def test_invalid_index(self):
        p = Point(4, 5)
        with self.assertRaises(IndexError):
            p[2]
        with self.assertRaises(IndexError):
            p[2] = 1
        with self.assertRaises(IndexError):
            p[-1]
        with self.assertRaises(IndexError):
            p[-1] = 1

    def test_point_subtraction(self):
        p1 = Point(5, 7)
        p2 = Point(3, 1)
        result = Vector(2, 6)
        self.assertEqual(p1 - p2, result)

    def test_addition_with_vector(self):
        p = Point(4, 10)
        v = Vector(1, -2)
        self.assertTrue(isinstance(p + v, Point))
        self.assertEqual(p + v, Point(5, 8))

    def test_subtracting_a_vector(self):
        p = Point(5.5, 6)
        v = Vector(2, 3.4)
        self.assertTrue(isinstance(p - v, Point))
        self.assertEqual(p - v, Point(3.5, 2.6))
