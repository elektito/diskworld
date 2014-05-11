import unittest
from point import Point
from vector import Vector
from disk import Disk
from world import calculateCollision

class TestCollisions(unittest.TestCase):
    def test_touching_disks_one_moves(self):
        d1 = Disk(Point(0, 0), 2, 1e45, Vector(10, 0))
        d2 = Disk(Point(3, 0), 1, 1, Vector(0, 0))
        c1, c2 = calculateCollision(d1, d2, 1)

        self.assertTrue(c1 is not None)
        self.assertTrue(c2 is not None)

        self.assertEqual(c1.other, d2)
        self.assertEqual(c2.other, d1)

        self.assertEqual(c1.dv, Vector(0, 0))
        self.assertEqual(c2.dv, Vector(20, 0))
