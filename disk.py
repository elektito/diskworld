from math import sqrt, pi

class Disk:
    def __init__(self, center, radius, material, velocity=(0, 0)):
        self.center = center
        self.radius = radius
        self.material = material
        self.velocity = velocity

    @property
    def surface(self):
        return pi * self.radius ** 2

    @property
    def mass(self):
        return self.surface * self.material.density

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
        comp = vr * centers_vector / len(centers_vector)

        return self.isInContact(disk) and comp > 0

    def updatePosition(self):
        pass
