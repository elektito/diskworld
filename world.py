import itertools

class Collision:
    def __init__(self):
        self.toi = 0 # time of impact
        self.disk1 = None
        self.disk2 = None
        self.disk1DeltaV = Vector(0, 0)
        self.disk2DeltaV = Vector(0, 0)

def velocitiesAfterCollision(disk1, disk2):
    # Calculate collision impulse from conservation of momentum and
    # conservation of energy. Look at this for details:
    # http://www.imada.sdu.dk/~rolf/Edu/DM815/E10/2dcollisions.pdf
    m1 = disk1.mass
    m2 = disk2.mass
    v1 = disk1.velocity
    v2 = disk2.velocity
    n = disk2.center - disk1.center # normal vector
    un = n / n.magnitude # unit normal vector
    ut = Vector(-un.y, un.x) # unit tangent vector (perpendicular to normal)
    v1n = un * v1 # normal component of disk 1 velocity
    v1t = ut * v1 # tangential component of disk 1 velocity
    v2n = un * v2 # normal component of disk 2 velocity
    v2t = ut * v2 # tangential component of disk 2 velocity
    nv1t = ut * v1t # new tangential component of disk 1 velocity
    nv2t = ut * v2t # new tangential component of disk 2 velocity

    # magnitude of the new normal component of disk 1 velocity
    nv1n_mag = (v1n * (m1 - m2) + v2n * 2 * m2) / (m1 + m2)

    # magnitude of the new normal component of disk 2 velocity
    nv2n_mag = (v2n * (m2 - m1) + v1n * 2 * m1) / (m1 + m2)

    # new normal component of velocities
    nv1n = un * nv1n_mag
    nv2n = un * nv2n_mag

    # new velocities
    nv1 = nv1n + nv1t
    nv2 = nv2n + nv2t

    return nv1, nv2

def calculateCollision(disk1, disk2, dt):
    R = disk1.radius + disk2.radius
    dv = disk2.velocity - disk1.velocity
    dr = disk2.center - disk1.center

    t1 = (R * dv * t - dv * dr * dt) / (dv ** 2)
    t2 = (-R * dv * t - dv * dr * dt) / (dv ** 2)

    t1 = t1 if 0 < t1 <= dt else None
    t2 = t2 if 0 < t2 <= dt else None

    c = Collision()
    if t1 is None and t2 is None:
        return None
    elif t1 is None and t2 is not None:
        c.toi = t2
    elif t2 is None and t1 is not None:
        c.toi = t1
    else:
        c.toi = min(t1, t2)

    c.disk1 = disk1
    c.disk2 = disk2

    v1, v2 = velocitiesAfterCollision(disk1, disk2)
    c.disk1DeltaV = v1 - disk1.velocity
    c.disk2DeltaV = v2 - disk2.velocity

    return c

class World:
    def __init__(self):
        self.disks = []

    def update(self, dt):
        for d in self.disks:
            d.force = Vector(0, 0)
            d.collisions = []

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
            collision = calculateCollision(d1, d2, dt)
            if collision is not None:
                d1.collisions.append(collision)
                d2.collisions.append(collision)

        # Prune extra collisions; that is, remove collisions that are
        # happen after another collision and therefore will never
        # happen.
        for d in self.disks:
            if len(d.collisions) > 1:
                d.collisions.sort(key=lambda c: c.toi)

                # Bypass the collisions with the same time of impact
                # (toi).
                first = d.collisions[0]
                i = 1
                while d.collisions[i] - first < 0.000001:
                    i += 1
                rest = d.collisions[i:]
                d.collisions = d.collisions[:i]
                for c in rest:
                    other = c.disk1 if c.disk2 == d else c.disk2
                    other.collisions.remove(c)

        # Move the disks
        for d in self.disks:
            if len(d.collisions) > 0:
                for c in d.collisions:
                    d.velocity += c.disk1DeltaV if d == c.disk1 else c.disk2DeltaV
            d.center += d.velocity * dt
