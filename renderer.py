import pygame
from point import Point
from world import calculateCollision
from disk import Disk
from vector import Vector

red = pygame.Color(255, 0, 0)
black = pygame.Color(0, 0, 0)

class Guide:
    def __init__(self):
        self.start = None
        self.end = None

class Trail:
    def __init__(self, time=0, size=0):
        self.time = time
        self.size = size
        self.prev = []

    def clear(self):
        self.prev = []

class Renderer:
    def __init__(self, world, camera, surface):
        self.world = world
        self.camera = camera
        self.surface = surface
        self.currentTime = 0.0

    def drawFilledCircle(self, x, y, r, color):
        pygame.gfxdraw.filled_circle(self.surface, x, y, r, color)
        pygame.gfxdraw.aacircle(self.surface, x, y, r, color)

    def calcDiskSurfaceMetrics(self, center, radius):
        scrw, scrh = self.surface.get_size()
        ratio = float(scrw) / self.camera.width

        x, y = self.worldToSurfaceCoord(center)
        r = int(radius * ratio)

        return x, y, r

    def drawDisk(self, center, radius, color):
        x, y, r = self.calcDiskSurfaceMetrics(center, radius)
        self.drawFilledCircle(x, y, r, color)

    def drawGhost(self, center, radius, color):
        x, y, r = self.calcDiskSurfaceMetrics(center, radius)

        pygame.gfxdraw.aacircle(self.surface, x, y, r-1, color)
        pygame.gfxdraw.aacircle(self.surface, x, y, r, color)

    def surfaceToWorldCoord(self, x, y=None):
        '''Converts the given coordinate in the graphics surface to a point in
the world coordinate. Instead of two separate coordinates, a 2-tuple
can be passed.

        '''

        if y is None:
            x, y = x

        w, h = self.surface.get_size()
        y = h - y
        return Point(self.camera.x1 + (float(x) / w) * self.camera.width,
                     self.camera.y1 + (float(y) / h) * self.camera.height)

    def worldToSurfaceCoord(self, p):
        '''Converts the given point from world coordinates into surface
coordinates and returns the results as a 2-tuple.'''

        w, h = self.surface.get_size()
        x = float(p.x - self.camera.x1) / self.camera.width * w
        y = float(p.y - self.camera.y1) / self.camera.height * h
        return int(x), int(h - y)

    def drawGuides(self):
        for d in self.world.disks:
            if d.visuals.guide is not None:
                g = d.visuals.guide
                start = self.worldToSurfaceCoord(g.start)
                end = self.worldToSurfaceCoord(g.end)
                pygame.draw.aaline(self.surface, red, start, end, True)
                self.drawFilledCircle(end[0], end[1], 5, red)

                v = g.end - g.start
                original_v = d.velocity
                d.velocity = v

                collisions = []
                for d2 in self.world.disks:
                    if d2 != d:
                        c1, c2 = calculateCollision(d, d2, 1.0)
                        if c1 is not None:
                            collisions.append(c1)

                if len(collisions) > 1:
                    collisions.sort(key=lambda c: c.toi)

                    # Bypass the collisions with the same time of
                    # impact (toi).
                    first = collisions[0]
                    i = 1
                    while collisions[i].toi - first.toi < 0.000001:
                        i += 1
                    collisions = collisions[:i]

                dr = v * collisions[0].toi if len(collisions) > 0 else v
                self.drawGhost(d.center + dr, d.radius, black)

                d.velocity = original_v

    def drawTrails(self):
        for d in self.world.disks:
            trail = d.visuals.trail
            if trail is not None and \
               trail.time > 0 and \
               trail.size > 0:
                # Find all the points in the desired time window
                trail.prev = [(pos, time)
                              for pos, time in trail.prev
                              if time >= self.currentTime - trail.time]

                if trail.size >= len(trail.prev):
                    # Not enough previous locations available. Draw
                    # what we have.
                    points = [pos for pos, prev in trail.prev]
                else:
                    # Choose `size` points in the time window.

                    # Always use the first previous location
                    points = [trail.prev[0][0]]

                    # From the rest we choose enough, as evenly timed
                    # as possible, to create a trail.
                    allpoints = trail.prev[0:]
                    time = trail.prev[0][1]
                    step = float(trail.time) / trail.size
                    while len(points) < trail.size:
                        time += step

                        # Go forward among previous locations until we
                        # reach one after `time`.
                        span = []
                        i = 0
                        for pos, t in trail.prev[0:]:
                            i += 1
                            span.append((i, pos, t))
                            if t >= time:
                                break

                        # Choose the point as close to the time we want as possible
                        p = min(span, key=lambda r: abs(time - r[2]))
                        points.append(p[1])

                        # Continue from this point
                        allpoints = trail.prev[p[0]:]
                        time = p[2]

                # Now draw the points in the trail. Start with a
                # smaller radius (r) and alpha channel (a).
                r = 2.0
                a = 128
                if len(points) > 0:
                    dr = 3.0 / len(points)
                    da = (255 - a) / len(points)
                for p in points:
                    x, y = self.worldToSurfaceCoord(p)
                    color = pygame.Color(255, 0, 0, int(a))
                    self.drawFilledCircle(x, y, int(r), color)
                    r += dr
                    a += da

                # Add this location to the list of previous locations.
                trail.prev.append((d.center, self.currentTime))

    def update(self, dt):
        self.currentTime += dt

        self.drawTrails()

        for d in self.world.disks:
            if self.camera.isInView(d):
                self.drawDisk(d.center, d.radius, d.visuals.color)

        self.drawGuides()
