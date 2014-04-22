from math import sqrt

class Disk:
    def __init__(self, center, radius, material, velocity=(0, 0)):
        self.center = center
        self.radius = radius
        self.material = material
        self.velocity = velocity

    def isInContact(self, disk):
        distance = sqrt((self.center[0] - disk.center[0]) ** 2 +
                        (self.center[1] - disk.center[1]) ** 2)
        return distance <= self.radius + disk.radius
