import unittest
from math import pi
from disk import Disk
from materialdb import TestMaterialDatabase

class TestDisk(unittest.TestCase):
    def setUp(self):
        mdb = TestMaterialDatabase()
        self.material = mdb.testMaterial1

        self.disk1 = Disk((100, 100), 20, self.material)
        self.disk2 = Disk((130, 140), 30, self.material)
        self.disk3 = Disk((120, 130), 30, self.material)
        self.disk4 = Disk((150, 150), 30, self.material)

    def test_contact(self):
        self.assertTrue(self.disk1.isInContact(self.disk2))
        self.assertTrue(self.disk1.isInContact(self.disk3))
        self.assertFalse(self.disk1.isInContact(self.disk4))

    def test_surface(self):
        self.assertAlmostEqual(
            self.disk1.surface,
            pi * self.disk1.radius ** 2)

    def test_mass(self):
        self.assertAlmostEqual(
            self.disk1.mass,
            self.disk1.surface * self.disk1.material.density)

    def test_update_velocity(self):
        pass
