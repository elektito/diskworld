from math import sqrt, pi
from vector import Vector
from point import Point
from helpers import float_eq

class Visual:
    def __init__(self):
        self.color = None
        self.trail = None
        self.guide = None

class Disk:
    def __init__(self, center, radius, mass, velocity=Vector(0, 0)):
        if not isinstance(center, Point):
            raise TypeError('Disk center must be a point.')

        if not isinstance(velocity, Vector):
            raise TypeError('Disk velocity must be a vector.')

        self.center = center
        self.radius = radius
        self.velocity = velocity
        self.mass = mass

        self.force = Vector(0, 0)
        self.acceleration = Vector(0, 0)
        self.collisions = []

        self.visuals = Visual()

    @property
    def surface(self):
        return pi * self.radius ** 2

    def isInContact(self, disk):
        distance = abs(self.center - disk.center)
        R = self.radius + disk.radius

        # return distance <= R
        return distance < R or float_eq(distance, R)

    def isInCollision(self, disk):
        # The vector from the center of the other disk to the center
        # of this disk.
        centers_vector = disk.center - self.center

        # The ralative velocity of the two disks.
        vr = disk.velocity - self.velocity

        # The component of the relative velocity along centers_vector.
        comp = vr * centers_vector / centers_vector.magnitude

        return self.isInContact(disk) and comp > 0

    def updatePosition(self, dt):
        self.center.x += self.velocity.x * dt
        self.center.y += self.velocity.y * dt

    def __repr__(self):
        return "<Disk mass={} radius={} center={} velocity={}>".format(self.mass, self.radius, self.center, self.velocity)
