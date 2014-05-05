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

    def drawDisk(self, disk, ghost=False):
        scrw, scrh = self.surface.get_size()
        ratiow = float(scrw) / self.camera.width
        ratioh = float(scrh) / self.camera.height
        assert(ratiow - ratioh < .0001)
        ratio = ratiow

        x = int((disk.center.x - self.camera.x1) * ratio)
        y = int((disk.center.y - self.camera.y1) * ratio)
        y = int(scrh - y) # The y axis in pygame is top-down.
        r = int(disk.radius * ratio)

        if not ghost:
            pygame.gfxdraw.filled_circle(self.surface, x, y, r, disk.color)
            pygame.gfxdraw.aacircle(self.surface, x, y, r, disk.color)
        else:
            #pygame.gfxdraw.filled_circle(self.surface, x, y, r, disk.color)
            pygame.gfxdraw.aacircle(self.surface, x, y, r-1, disk.color)
            pygame.gfxdraw.aacircle(self.surface, x, y, r, disk.color)

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
        for g in self.guides:
            start = self.worldToSurfaceCoord(g.start)
            end = self.worldToSurfaceCoord(g.end)
            pygame.draw.line(self.surface, red, start, end)
            pygame.draw.circle(self.surface, red, end, 5, 0)

            g.disk.velocity = g.end - g.start

            collisions = []
            for d in self.world.disks:
                if d != g.disk:
                    c1, c2 = calculateCollision(g.disk, d, 1.0)
                    if c1 is not None:
                        collisions.append(c1)

            if len(collisions) > 1:
                collisions.sort(key=lambda c: c.toi)

                # Bypass the collisions with the same time of impact
                # (toi).
                first = collisions[0]
                i = 1
                while collisions[i] - first < 0.000001:
                    i += 1
                collisions = collisions[:i]

            if len(collisions) > 0:
                dr = g.disk.velocity * collisions[0].toi
                d = Disk(g.disk.center + dr, g.disk.radius, g.disk.mass, black, Vector(0, 0))
                self.drawDisk(d, ghost=True)
            else:
                dr = g.disk.velocity * 1.0
                d = Disk(g.disk.center + dr, g.disk.radius, g.disk.mass, black, Vector(0, 0))
                self.drawDisk(d, ghost=True)

    def update(self):
        for d in self.world.disks:
            if self.camera.isInView(d):
                self.drawDisk(d)

        self.drawGuides()
