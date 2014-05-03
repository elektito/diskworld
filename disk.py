from math import sqrt, pi
from vector import Vector
from point import Point

class Disk:
    def __init__(self, center, radius, mass, color, velocity=Vector(0, 0)):
        if not isinstance(center, Point):
            raise TypeError('Disk center must be a point.')

        if not isinstance(velocity, Vector):
            raise TypeError('Disk velocity must be a vector.')

        self.center = center
        self.radius = radius
        self.velocity = velocity
        self.mass = mass
        self.color = color

        self.force = Vector(0, 0)
        self.acceleration = Vector(0, 0)
        self.collisions = []

    @property
    def surface(self):
        return pi * self.radius ** 2

    def isInContact(self, disk):
        distance = sqrt((self.center[0] - disk.center[0]) ** 2 +
                        (self.center[1] - disk.center[1]) ** 2)
        return distance <= self.radius + disk.radius

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
        return "<Disk mass={} radius={} color={}>".format(self.mass, self.radius, self.color)
