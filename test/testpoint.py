import unittest
from point import Point
from vector import Vector

class TestPoint(unittest.TestCase):
    def test_point_subtraction(self):
        p1 = Point(5, 7)
        p2 = point(3, 1)
        result = Vector(2, 6)
        self.assertEqual(p1 - p2, result)
