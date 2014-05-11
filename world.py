import itertools
import pygame.gfxdraw
from math import sqrt
from vector import Vector
from helpers import float_eq

class Collision(object):
    def __init__(self, disk, otherDisk):
        self.disk = disk
        self.other = otherDisk

        self.toi = 0 # time of impact
        self.dv = Vector(0, 0)

    def __repr__(self):
        return '<Collision toi={} dv={}>'.format(self.toi, self.dv)

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
    # The vector from the center of the other disk to the center of
    # this disk.
    centers_vector = disk2.center - disk1.center

    # The ralative velocity of the two disks.
    vr = disk2.velocity - disk1.velocity

    # If the relative velocity has a component along the normal vector
    # of the two disks (centers_vector), it means the two disks are
    # not moving towards each other.
    if vr * centers_vector >= 0:
        print "XXXXX", disk1.center, disk1.velocity, disk2.center, disk2.velocity
        return None, None

    if disk1.isInContact(disk2):
        t1 = t2 = 0.0
    else:
        R = disk1.radius + disk2.radius
        dv = disk2.velocity - disk1.velocity
        dr = disk2.center - disk1.center

        delta = R**2 * (dv * dv) - \
                dr.x**2 * dv.y **2 + \
                2 * dr.x * dr.y * dv.x * dv.y - \
                dr.y**2 * dv.x**2
        if delta < 0:
            return None, None
        t1 = -((dr * dv) + sqrt(delta)) / (dv * dv)
        t2 = -((dr * dv) + sqrt(delta)) / (dv * dv)

        t1 = t1 if 0 <= t1 <= dt else None
        t2 = t2 if 0 <= t2 <= dt else None

    c1, c2 = Collision(disk1, disk2), Collision(disk2, disk1)
    if t1 is None and t2 is None:
        return None, None
    elif t1 is None and t2 is not None:
        c1.toi = c2.toi = t2
    elif t2 is None and t1 is not None:
        c1.toi = c2.toi = t1
    else:
        c1.toi = c2.toi = min(t1, t2)

    v1, v2 = velocitiesAfterCollision(disk1, disk2)
    c1.dv = v1 - disk1.velocity
    c2.dv = v2 - disk2.velocity

    return c1, c2

class World(object):
    def __init__(self):
        self.disks = []

    def update(self, dt):
        for d in self.disks:
            d.force = Vector(0, 0)
            d.collisions = []

        print
        print "force before:", [d.force for d in self.disks]
        # Calculate non-contact forces
        for d1, d2 in itertools.combinations(self.disks, 2):
            # gravity
            G = 6.674e-11
            fg = (G * d1.mass * d2.mass) / (d2.center - d1.center).magnitude ** 2
            d1.force += Vector(angle=(d2.center - d1.center).angle, magnitude=fg)
            d2.force += Vector(angle=(d1.center - d2.center).angle, magnitude=fg)
        print "force after:", [d.force for d in self.disks]

        print "force before:", [d.force for d in self.disks]
        # Calculate contact forces
        for d1, d2 in itertools.combinations(self.disks, 2):
            # normal force
            if d1.isInContact(d2):
                print "NNNNNNNNNNNNNNNNNN"
                fy = d1.force.project(d2.center - d1.center)
                d1.force -= fy
                d2.force += fy
            else:
                print "UUUUUUUUUUUUUUUUUUUUUN"
        print "force after:", [d.force for d in self.disks]

        print "accel. before:", [d.acceleration for d in self.disks]
        # Calculate accelerations
        for d in self.disks:
            d.acceleration = d.force * (1.0 / d.mass)
        print "accel. after:", [d.acceleration for d in self.disks]

        print "vel. before:", [d.velocity for d in self.disks]
        # Calculate velocities
        for d in self.disks:
            d.velocity += d.acceleration * dt
        print "vel. after:", [d.velocity for d in self.disks]

        print "cols. before:", [d.collisions for d in self.disks]
        # Calculate collisions
        for d1, d2 in itertools.combinations(self.disks, 2):
            c1, c2 = calculateCollision(d1, d2, dt)
            if c1 is not None:
                d1.collisions.append(c1)
                d2.collisions.append(c2)
        print "cols. after:", [d.collisions for d in self.disks]

        print "cols.before:", [d.collisions for d in self.disks]
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
                    c.other.collisions.remove(c)
        print "cols. after:", [d.collisions for d in self.disks]

        print "pos. before:", [d.center for d in self.disks]
        # Move the disks
        for d in self.disks:
            if len(d.collisions) > 0:
                # Move the disk to where the collisions occurs
                d.center += d.velocity * d.collisions[0].toi

                # Apply the impulses caused by the collisions
                for c in d.collisions:
                    d.velocity += c.dv
            else:
                d.center += d.velocity * dt
        print "pos. after:", [d.center for d in self.disks]
        print "vel. after:", [d.velocity for d in self.disks]
        for d in self.disks:
            if len(d.collisions) > 0:
                if not d.isInContact(c.other):
                    print "FOOOOOOUUUUL: Collision detected, but no contact!"
                    #exit(0)
        for d1, d2 in itertools.combinations(self.disks, 2):
            if abs(d2.center - d1.center) - (d1.radius + d2.radius) < 0.000001:
                print "NOOOOOOOOOOOOOO!", abs(d2.center - d1.center), d1.radius + d2.radius, d1.collisions, d2.collisions
                #exit(0)
