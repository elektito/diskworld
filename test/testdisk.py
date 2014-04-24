import unittest
from math import pi
from disk import Disk
from vector import Vector
from point import Point
from materialdb import TestMaterialDatabase

class TestDisk(unittest.TestCase):
    def setUp(self):
        mdb = TestMaterialDatabase()
        self.material = mdb.testMaterial1

        self.disk1 = Disk(Point(100, 100), 20, self.material)
        self.disk2 = Disk(Point(130, 140), 30, self.material)
        self.disk3 = Disk(Point(120, 130), 30, self.material)
        self.disk4 = Disk(Point(150, 150), 30, self.material)

    def test_contact_with_touching_disk(self):
        self.assertTrue(self.disk1.isInContact(self.disk2))

    def test_contact_with_overlapping_disk(self):
        self.assertTrue(self.disk1.isInContact(self.disk3))

    def test_contact_with_non_touching_disk(self):
        self.assertFalse(self.disk1.isInContact(self.disk4))

    def test_collision_with_touching_object_moving_against(self):
        self.disk1.velocity = Vector(1, 1)
        self.disk2.velocity = Vector(-1, -1)
        self.assertTrue(self.disk1.isInCollision(self.disk2))

    def test_collision_with_touching_object_at_rest(self):
        self.disk1.velocity = Vector(1, 1)
        self.disk2.velocity = Vector(0, 0)
        self.assertTrue(self.disk1.isInCollision(self.disk2))

    def test_collision_with_touching_object_moving_alongside(self):
        self.disk1.velocity = Vector(1, 1)
        self.disk2.velocity = Vector(1, 1)
        self.assertFalse(self.disk1.isInCollision(self.disk2))

    def test_collision_with_overlapping_object_moving_against(self):
        self.disk1.velocity = Vector(1, 1)
        self.disk3.velocity = Vector(-1, -1)
        self.assertTrue(self.disk1.isInCollision(self.disk3))

    def test_collision_with_overlapping_object_at_rest(self):
        self.disk1.velocity = Vector(1, 1)
        self.disk3.velocity = Vector(0, 0)
        self.assertTrue(self.disk1.isInCollision(self.disk3))

    def test_collision_with_overlapping_object_moving_alongside(self):
        self.disk1.velocity = Vector(1, 1)
        self.disk3.velocity = Vector(1, 1)
        self.assertFalse(self.disk1.isInCollision(self.disk3))

    def test_collision_with_non_touching_object_moving_against(self):
        self.disk1.velocity = Vector(1, 1)
        self.disk4.velocity = Vector(-1, -1)
        self.assertFalse(self.disk1.isInCollision(self.disk4))

    def test_collision_with_non_touching_object_at_rest(self):
        self.disk1.velocity = Vector(1, 1)
        self.disk4.velocity = Vector(0, 0)
        self.assertFalse(self.disk1.isInCollision(self.disk4))

    def test_collision_with_non_touching_object_moving_alongside(self):
        self.disk1.velocity = Vector(1, 1)
        self.disk4.velocity = Vector(1, 1)
        self.assertFalse(self.disk1.isInCollision(self.disk4))

    def test_surface(self):
        self.assertAlmostEqual(
            self.disk1.surface,
            pi * self.disk1.radius ** 2)

    def test_mass(self):
        self.assertAlmostEqual(
            self.disk1.mass,
            self.disk1.surface * self.disk1.material.density)

    def test_total_force(self):
        pass

    def test_update_velocity(self):
        pass

    def test_update_position(self):
        self.disk1.velocity = Vector(2, 3)

        dt = 0.1
        pos = self.disk1.center
        destination = pos[0] + 2 * dt, pos[1] + 3 * dt
        self.disk1.updatePosition()
        self.assertAlmostEqual(destination[0], self.disk1.center[0])
        self.assertAlmostEqual(destination[1], self.disk1.center[1])
