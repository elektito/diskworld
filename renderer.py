import pygame
from point import Point

class Renderer:
    def __init__(self, world, camera, surface):
        self.world = world
        self.camera = camera
        self.surface = surface

    def drawDisk(self, disk):
        scrw, scrh = self.surface.get_size()
        ratiow = float(scrw) / self.camera.width
        ratioh = float(scrh) / self.camera.height
        assert(ratiow - ratioh < .0001)
        ratio = ratiow

        x = int((disk.center.x - self.camera.x1) * ratio)
        y = int((disk.center.y - self.camera.y1) * ratio)
        y = int(scrh - y) # The y axis in pygame is top-down.
        r = int(disk.radius * ratio)

        pygame.draw.circle(self.surface, disk.color, (x, y), r, 0)

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
        return x, h - y

    def update(self):
        for d in self.world.disks:
            if self.camera.isInView(d):
                self.drawDisk(d)
