import unittest
import pygame
from camera import Camera
from point import Point
from disk import Disk

WHITE = pygame.Color(255, 255, 255)

class TestCamera(unittest.TestCase):
    def setUp(self):
        self.camera = Camera(2, 2, 20, 20)

    def test_invalid_coordinates(self):
        with self.assertRaises(ValueError):
            camera = Camera(20, 2, 2, 20)

        with self.assertRaises(ValueError):
            camera = Camera(2, 20, 2, 2)

    def test_width(self):
        camera = Camera(2.5, 5, 21, 14)
        self.assertAlmostEqual(camera.width, 18.5)

    def test_height(self):
        camera = Camera(48.5, 31.2, 71.2, 89.9)
        self.assertAlmostEqual(camera.height, 58.7)

    def test_center(self):
        camera = Camera(2, 4, 7, 15)
        center = Point(4.5, 9.5)
        self.assertEqual(camera.center, center)

    def test_completely_in_view(self):
        disk = Disk(Point(10, 10), 5, 1, WHITE)
        self.assertTrue(self.camera.isInView(disk))

    def test_part_of_top_right_in_view(self):
        disk = Disk(Point(0, 0), 5, 1, WHITE)
        self.assertTrue(self.camera.isInView(disk))

    def test_part_of_top_left_in_view(self):
        disk = Disk(Point(22, 1), 5, 1, WHITE)
        self.assertTrue(self.camera.isInView(disk))

    def test_part_of_bottom_left_in_view(self):
        disk = Disk(Point(22, 24), 5, 1, WHITE)
        self.assertTrue(self.camera.isInView(disk))

    def test_part_of_bottom_right_in_view(self):
        disk = Disk(Point(1, 23), 5, 1, WHITE)
        self.assertTrue(self.camera.isInView(disk))

    def test_part_of_top_in_view(self):
        disk = Disk(Point(10, 1), 5, 1, WHITE)
        self.assertTrue(self.camera.isInView(disk))

    def test_part_of_bottom_in_view(self):
        disk = Disk(Point(10, 22), 5, 1, WHITE)
        self.assertTrue(self.camera.isInView(disk))

    def test_part_of_left_in_view(self):
        disk = Disk(Point(21, 11), 5, 1, WHITE)
        self.assertTrue(self.camera.isInView(disk))

    def test_part_of_right_in_view(self):
        disk = Disk(Point(1.5, 10), 5, 1, WHITE)
        self.assertTrue(self.camera.isInView(disk))

    def test_not_in_view_below(self):
        disk = Disk(Point(10, -5), 5, 1, WHITE)
        self.assertFalse(self.camera.isInView(disk))

    def test_not_in_view_above(self):
        disk = Disk(Point(10, 25.5), 5, 1, WHITE)
        self.assertFalse(self.camera.isInView(disk))

    def test_not_in_view_to_the_left(self):
        disk = Disk(Point(-5, 10), 5, 1, WHITE)
        self.assertFalse(self.camera.isInView(disk))

    def test_not_in_view_to_the_right(self):
        disk = Disk(Point(26, 10), 5, 1, WHITE)
        self.assertFalse(self.camera.isInView(disk))

    def test_not_in_view_to_the_bottom_right(self):
        disk = Disk(Point(26, -4), 5, 1, WHITE)
        self.assertFalse(self.camera.isInView(disk))

    def test_not_in_view_to_the_bottom_left(self):
        disk = Disk(Point(-6, -6), 5, 1, WHITE)
        self.assertFalse(self.camera.isInView(disk))

    def test_not_in_view_to_the_top_left(self):
        disk = Disk(Point(-5, 26), 5, 1, WHITE)
        self.assertFalse(self.camera.isInView(disk))

    def test_not_in_view_to_the_top_right(self):
        disk = Disk(Point(27, 26), 5, 1, WHITE)
        self.assertFalse(self.camera.isInView(disk))
