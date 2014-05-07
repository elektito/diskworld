import pygame
from point import Point
from world import calculateCollision
from disk import Disk
from vector import Vector

class Guide:
    def __init__(self):
        self.start = None
        self.end = None

class Renderer:
    def __init__(self, world, camera, surface):
        self.world = world
        self.camera = camera
        self.surface = surface

        self.guides = []

    def calcDiskSurfaceMetrics(self, center, radius):
        scrw, scrh = self.surface.get_size()
        ratio = float(scrw) / self.camera.width

        x, y = self.worldToSurfaceCoord(center)
        r = int(radius * ratio)

        return x, y, r

    def drawDisk(self, center, radius, color):
        x, y, r = self.calcDiskSurfaceMetrics(center, radius)

        pygame.gfxdraw.filled_circle(self.surface, x, y, r, color)
        pygame.gfxdraw.aacircle(self.surface, x, y, r, color)

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
        red = pygame.Color(255, 0, 0)
        black = pygame.Color(0, 0, 0)

        for d in self.world.disks:
            if d.visuals.guide is not None:
                g = d.visuals.guide
                start = self.worldToSurfaceCoord(g.start)
                end = self.worldToSurfaceCoord(g.end)
                pygame.draw.line(self.surface, red, start, end)
                pygame.draw.circle(self.surface, red, end, 5, 0)

                d.velocity = g.end - g.start

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
                    while collisions[i] - first < 0.000001:
                        i += 1
                    collisions = collisions[:i]

                if len(collisions) > 0:
                    dr = d.velocity * collisions[0].toi
                else:
                    dr = d.velocity * 1.0
                self.drawGhost(d.center + dr, d.radius, black)

    def update(self):
        for d in self.world.disks:
            if self.camera.isInView(d):
                self.drawDisk(d.center, d.radius, d.visuals.color)

        self.drawGuides()
