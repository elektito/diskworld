import unittest
import pygame
from camera import Camera
from point import Point
from vector import Vector
from disk import Disk

class TestCamera(unittest.TestCase):
    def setUp(self):
        self.camera = Camera(bottomleft=Point(2, 2),
                             topright=Point(20, 20))

    def test_creation_with_two_points(self):
        c = Camera(bottomleft=Point(2.5, 3), topright=Point(10.5, 9))
        self.assertAlmostEqual(c.width, 8.0)
        self.assertAlmostEqual(c.height, 6)

    def test_creation_with_bottomleft_and_width_and_height(self):
        c = Camera(bottomleft=Point(2, 3), width=8.5, height=6)
        self.assertEqual(c.topright, Point(10.5, 9))

    def test_creation_with_nonpositive_width(self):
        with self.assertRaises(ValueError):
            c = Camera(bottomleft=Point(4, 4), width=-0.5, height=0.5)
        with self.assertRaises(ValueError):
            c = Camera(bottomleft=Point(4, 4), width=0, height=5)

    def test_creation_with_negative_height(self):
        with self.assertRaises(ValueError):
            c = Camera(bottomleft=Point(4, 4), width=0.5, height=-0.5)
        with self.assertRaises(ValueError):
            c = Camera(bottomleft=Point(4, 4), width=0.5, height=0)

    def test_creation_with_invalid_coordinates(self):
        with self.assertRaises(ValueError):
            c = Camera(bottomleft=Point(20, 2), topright=Point(2, 20))

        with self.assertRaises(ValueError):
            c = Camera(bottomleft=Point(2, 20), topright=Point(2, 2))

    def test_creation_with_missing_bottomleft(self):
        with self.assertRaises(ValueError):
            c = Camera(topright=Point(2, 2))

        with self.assertRaises(ValueError):
            c = Camera(width=3, height=4)

    def test_creation_with_only_bottomleft(self):
        with self.assertRaises(ValueError):
            c = Camera(bottomleft=Point(2, 2))

    def test_creation_with_missing_width_or_height(self):
        with self.assertRaises(ValueError):
            c = Camera(bottomleft=Point(2, 2), width=4)

        with self.assertRaises(ValueError):
            c = Camera(bottomleft=Point(2, 2), height=4)

    def test_creation_with_non_point(self):
        with self.assertRaises(ValueError):
            c = Camera(bottomleft=(1, 1), topright=(2, 2))
            c = Camera(bottomleft=(1, 1), topright=Point(2, 2))
            c = Camera(bottomleft=Point(1, 1), topright=(2, 2))

    def test_creation_with_additional_arguments(self):
        with self.assertRaises(ValueError):
            c = Camera(bottomleft=(1, 1), topright=Point(2, 2), width=4.0)

        with self.assertRaises(ValueError):
            c = Camera(bottomleft=(1, 1), topright=Point(2, 2), height=4.0)

    def test_setting_attributes(self):
        c = Camera(bottomleft=Point(2, 2), topright=Point(4, 5))
        with self.assertRaises(AttributeError):
            c.bottomleft = Point(1, 1)
        with self.assertRaises(AttributeError):
            c.topright = Point(1, 1)
        with self.assertRaises(AttributeError):
            c.width = 10
        with self.assertRaises(AttributeError):
            c.height = 10
        with self.assertRaises(AttributeError):
            c.center = Point(1, 1)

    def test_center(self):
        camera = Camera(bottomleft=Point(2, 4), topright=Point(7, 15))
        center = Point(4.5, 9.5)
        self.assertEqual(camera.center, center)

    def test_panning(self):
        c = Camera(bottomleft=Point(1, 1.5), topright=Point(2, 3))
        c.pan(Vector(0.5, -0.3))
        self.assertEqual(c.bottomleft, Point(1.5, 1.2))
        self.assertEqual(c.topright, Point(2.5, 2.7))

    def test_zooming(self):
        # zooming out
        c = Camera(bottomleft=Point(1, 1), width=4, height=2)
        c.zoom(-0.2)
        self.assertAlmostEqual(c.width, 4.8)
        self.assertAlmostEqual(c.height, 2.4)
        self.assertEqual(c.bottomleft, Point(0.6, 0.8))
        self.assertEqual(c.topright, Point(6.4, 3.2))

        # zooming in
        c = Camera(bottomleft=Point(1, 1), width=4, height=2)
        c.zoom(0.4)
        self.assertAlmostEqual(c.width, 2.4)
        self.assertAlmostEqual(c.height, 1.2)
        self.assertEqual(c.bottomleft, Point(1.8, 1.4))
        self.assertEqual(c.topright, Point(4.2, 2.6))

    def test_completely_in_view(self):
        disk = Disk(Point(10, 10), 5, 1)
        self.assertTrue(self.camera.isInView(disk))

    def test_part_of_top_right_in_view(self):
        disk = Disk(Point(0, 0), 5, 1)
        self.assertTrue(self.camera.isInView(disk))

    def test_part_of_top_left_in_view(self):
        disk = Disk(Point(22, 1), 5, 1)
        self.assertTrue(self.camera.isInView(disk))

    def test_part_of_bottom_left_in_view(self):
        disk = Disk(Point(22, 24), 5, 1)
        self.assertTrue(self.camera.isInView(disk))

    def test_part_of_bottom_right_in_view(self):
        disk = Disk(Point(1, 23), 5, 1)
        self.assertTrue(self.camera.isInView(disk))

    def test_part_of_top_in_view(self):
        disk = Disk(Point(10, 1), 5, 1)
        self.assertTrue(self.camera.isInView(disk))

    def test_part_of_bottom_in_view(self):
        disk = Disk(Point(10, 22), 5, 1)
        self.assertTrue(self.camera.isInView(disk))

    def test_part_of_left_in_view(self):
        disk = Disk(Point(21, 11), 5, 1)
        self.assertTrue(self.camera.isInView(disk))

    def test_part_of_right_in_view(self):
        disk = Disk(Point(1.5, 10), 5, 1)
        self.assertTrue(self.camera.isInView(disk))

    def test_not_in_view_below(self):
        disk = Disk(Point(10, -5), 5, 1)
        self.assertFalse(self.camera.isInView(disk))

    def test_not_in_view_above(self):
        disk = Disk(Point(10, 25.5), 5, 1)
        self.assertFalse(self.camera.isInView(disk))

    def test_not_in_view_to_the_left(self):
        disk = Disk(Point(-5, 10), 5, 1)
        self.assertFalse(self.camera.isInView(disk))

    def test_not_in_view_to_the_right(self):
        disk = Disk(Point(26, 10), 5, 1)
        self.assertFalse(self.camera.isInView(disk))

    def test_not_in_view_to_the_bottom_right(self):
        disk = Disk(Point(26, -4), 5, 1)
        self.assertFalse(self.camera.isInView(disk))

    def test_not_in_view_to_the_bottom_left(self):
        disk = Disk(Point(-6, -6), 5, 1)
        self.assertFalse(self.camera.isInView(disk))

    def test_not_in_view_to_the_top_left(self):
        disk = Disk(Point(-5, 26), 5, 1)
        self.assertFalse(self.camera.isInView(disk))

    def test_not_in_view_to_the_top_right(self):
        disk = Disk(Point(27, 26), 5, 1)
        self.assertFalse(self.camera.isInView(disk))
