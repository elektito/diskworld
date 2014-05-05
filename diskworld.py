import pygame
import sys
import itertools
from math import sqrt
from collections import defaultdict
from pygame.locals import *
import pygame.gfxdraw
from disk import Disk
from vector import Vector
from point import Point

pygame.init()
fps_clock = pygame.time.Clock()

window_surface = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Circle Test")

white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)

class WorldX:
    def __init__(self, width, height, screen, disks):
        if float(width) / height != float(screen.get_size()[0]) / screen.get_size()[1]:
            raise Exception(
                "width/height ratio for the game world should be the"
                " same as screen width/height ratio.")

        self.width = float(width)
        self.height = float(height)
        self.screen = screen
        self.disks = disks

    def drawDisk(self, disk):
        # convert to pygame coordinates
        scrw, scrh = self.screen.get_size()
        nx = int(float(disk.center.x) /  self.width * scrw)
        ny = int(scrh - float(disk.center.y) / self.height * scrh)
        nr = int(float(disk.radius) * (scrw / self.width))

        pygame.draw.circle(self.screen, disk.color, (nx, ny), nr, 0)

    def update(self, dt):
        G = 6.674e-11
        forces = defaultdict(list)

        # Calculate non-contact forces.
        for d1, d2 in itertools.combinations(self.disks, 2):
            # gravity
            fg = (G * d1.mass * d2.mass) / (d2.center - d1.center).magnitude ** 2
            forces[d1].append(Vector(angle=(d2.center - d1.center).angle, magnitude=fg))
            forces[d2].append(Vector(angle=(d1.center - d2.center).angle, magnitude=fg))

        # Calculate contact forces.
        for d1, d2 in itertools.combinations(self.disks, 2):
            # normal force
            if d1.isInContact(d2):
                fy = sum(forces[d1], Vector(0, 0)).project(d2.center - d1.center)
                forces[d1].append(-fy)
                forces[d2].append(fy)

                # Calculate collision impulse from conservation of
                # momentum and conservation of energy. Look at this
                # for details:
                # http://www.imada.sdu.dk/~rolf/Edu/DM815/E10/2dcollisions.pdf
                m1 = d1.mass
                m2 = d2.mass
                v1 = d1.velocity
                v2 = d2.velocity
                n = d2.center - d1.center # normal vector
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

                d1.velocity = nv1
                d2.velocity = nv2

        for d in self.disks:
            f = sum(forces[d], Vector(0, 0))
            a = f / float(d.mass)
            d.velocity += a * dt
            d.updatePosition(dt)
            self.drawDisk(d)

paused = True
dragging = False
dragging_start = None
d1 = Disk(Point(20, 20), 2, 1, white, Vector(0, 0))
d2 = Disk(Point(10, 10), 5, 5.97219e+14, white, Vector(0, 0))
#world = World(40, 30, window_surface, [d1, d2])
from world import World
from camera import Camera
from renderer import Renderer, Guide
world = World()
world.disks = [d1, d2]
camera = Camera(0, 0, 39, 29)
renderer = Renderer(world, camera, window_surface)

dt = 0

while True:
    window_surface.fill(blue)

    renderer.update()

    for event in pygame.event.get():
        if event.type == QUIT:
            print "Going away!"
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 1: # left button
                x, y = event.pos
                p = renderer.surfaceToWorldCoord(x, y)
                if abs(p - d1.center) < d1.radius:
                    # inside the disk
                    dragging = True
                    dragging_start = renderer.worldToSurfaceCoord(d1.center)
        elif event.type == MOUSEMOTION:
            if dragging:
                if len(renderer.guides) == 0:
                    renderer.guides.append(Guide())
                    renderer.guides[0].disk = d1
                renderer.guides[0].start = d1.center
                renderer.guides[0].end = renderer.surfaceToWorldCoord(event.pos)
        elif event.type == MOUSEBUTTONUP:
            if event.button == 3: # right button
                # Move the smaller disk to the point clicked.
                p = renderer.surfaceToWorldCoord(event.pos)
                d1.center = p
                d1.velocity = Vector(0, 0)
            elif event.button == 1: # left button
                if dragging:
                    p1 = renderer.surfaceToWorldCoord(dragging_start)
                    p2 = renderer.surfaceToWorldCoord(event.pos)
                    d1.velocity = 2 * (p2 - p1)
                    renderer.guides = []
                    paused = False
                dragging = False
        elif event.type == KEYDOWN:
            if event.key == K_n:
                world.update(dt / 1000.0)
            if event.key == K_p:
                paused = not paused
                print "Paused." if paused else "Un-paused."
            if event.key == K_LEFT:
                d1.velocity.x -= 0.5
            if event.key == K_RIGHT:
                d1.velocity.x += 0.5
            if event.key == K_UP:
                d1.velocity.y += 0.5
            if event.key == K_DOWN:
                d1.velocity.y -= 0.5
            print "New speed:", d1.velocity
            if event.key == K_q:
                pygame.event.post(pygame.event.Event(QUIT))

    pygame.display.update()
    dt = fps_clock.tick(30)
    if not paused:
        world.update(dt / 1000.0)
