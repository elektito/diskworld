import unittest
from disk import Disk
from color import white
from materialdb import TestMaterialDatabase

class TestDisk(unittest.TestCase):
    def setUp(self):
        mdb = TestMaterialDatabase()
        self.material = mdb.testMaterial1

    def test_contact(self):
        disk1 = Disk((100, 100), 20, self.material)
        disk2 = Disk((130, 140), 30, self.material)
        self.assertTrue(disk1.isInContact(disk2))

        disk3 = Disk((120, 130), 30, self.material)
        self.assertTrue(disk1.isInContact(disk3))

        disk4 = Disk((150, 150), 30, self.material)
        self.assertFalse(disk1.isInContact(disk4))
