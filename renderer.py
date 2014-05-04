import pygame

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

    def update(self):
        for d in self.world.disks:
            if self.camera.isInView(d):
                self.drawDisk(d)
