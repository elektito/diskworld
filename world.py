import itertools

class World:
    def __init__(self):
        self.disks = []

    def update(self, dt):
        for d in self.disks:
            d.force = Vector(0, 0)

        # Calculate non-contact forces
        for d1, d2 in itertools.combinations(self.disks, 2):
            # gravity
            fg = (G * d1.mass * d2.mass) / (d2.center - d1.center).magnitude ** 2
            d1.force = Vector(angle=(d2.center - d1.center).angle, magnitude=fg)
            d2.force = Vector(angle=(d1.center - d2.center).angle, magnitude=fg)

        # Calculate contact forces
        for d1, d2 in itertools.combinations(self.disks, 2):
            # normal force
            if d1.isInContact(d2):
                fy = d1.force.project(d2.center - d1.center)
                d1.force -= fy
                d2.force += fy

        # Calculate accelerations
        for d in self.disks:
            d.acceleration = d.force * (1.0 / d.mass)

        # Calculate velocities
        for d in self.disks:
            d.velocity += d.acceleration * dt * d.velocity

        # Calculate collisions
        for d1, d2 in itertools.combinations(self.disks, 2):
            collision = self.calculateCollision(d1, d2, dt)
            if collision is not None:
                pass
