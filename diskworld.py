import pygame
import sys
from pygame.locals import *
from disk import Disk
from vector import Vector
from point import Point
from world import World
from camera import Camera
from renderer import Renderer, Guide, Trail

def get_disk_from_surface_point(point, world, renderer):
    ret = None
    for d in world.disks:
        p = renderer.surfaceToWorldCoord(point)
        if abs(p - d.center) < d.radius:
            ret = d
    return ret

pygame.init()
fps_clock = pygame.time.Clock()

window_surface = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Circle Test")

white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)

paused = True
throwing = False
throwing_start = None
throwing_disk = None
dragging_disk = None
dragging_offset = None
panning = False
panning_start = None
d1 = Disk(Point(20, 20), 2, 1, Vector(0, 0))
d1.visuals.color = white
d1.visuals.trail = Trail(1, 10)
d2 = Disk(Point(10, 10), 5, 5.97219e+14, Vector(0, 0))
d2.visuals.color = white

world = World()
world.disks = [d1, d2]
camera = Camera(bottomleft=Point(0, 0), topright=Point(39, 29))
renderer = Renderer(world, camera, window_surface)

dt = 0

while True:
    window_surface.fill(blue)

    renderer.update(dt / 1000.0)

    for event in pygame.event.get():
        if event.type == QUIT:
            print "Going away!"
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 3: # right button
                throwing_disk = get_disk_from_surface_point(event.pos, world, renderer)
                if throwing_disk is not None:
                    # inside a disk
                    throwing = True
                    throwing_start = renderer.worldToSurfaceCoord(throwing_disk.center)
            elif event.button == 2: # middle button
                d = get_disk_from_surface_point(event.pos, world, renderer)
                if d is None:
                    d1.center = renderer.surfaceToWorldCoord(event.pos)
                    if d1.visuals is not None and d1.visuals.trail is not None:
                        d1.visuals.trail.clear()
                    d1.velocity = Vector(0, 0)
            elif event.button == 1: # left button
                dragging_disk = get_disk_from_surface_point(event.pos, world, renderer)
                if dragging_disk is not None:
                    p = renderer.surfaceToWorldCoord(event.pos)
                    dragging_offset = p - dragging_disk.center
                    dragging_disk.velocity = Vector(0, 0)
                else:
                    # outside both disks. start panning
                    panning = True
                    panning_start = event.pos
            elif event.button == 4: # scroll up
                camera.zoom(0.1)
            elif event.button == 5: # scroll down
                camera.zoom(-0.1)
        elif event.type == MOUSEMOTION:
            if throwing:
                if throwing_disk.visuals.guide == None:
                    throwing_disk.visuals.guide = Guide()
                throwing_disk.visuals.guide.start = throwing_disk.center
                throwing_disk.visuals.guide.end = renderer.surfaceToWorldCoord(event.pos)
            elif dragging_disk is not None:
                p = renderer.surfaceToWorldCoord(event.pos)
                dragging_disk.center = p - dragging_offset
            elif panning:
                new_pos = event.pos
                p1 = renderer.surfaceToWorldCoord(panning_start)
                p2 = renderer.surfaceToWorldCoord(new_pos)
                v = p1 - p2
                panning_start = new_pos
                camera.pan(v)
        elif event.type == MOUSEBUTTONUP:
            if event.button == 1: # left button
                dragging_disk = None
                panning = False
            elif event.button == 3: # right button
                if throwing:
                    p1 = renderer.surfaceToWorldCoord(throwing_start)
                    p2 = renderer.surfaceToWorldCoord(event.pos)
                    throwing_disk.velocity = p2 - p1
                    throwing_disk.visuals.guide = None
                    paused = False
                throwing = False
                throwing_disk = None
        elif event.type == KEYDOWN:
            if event.key == K_n:
                world.update(dt / 1000.0)
            if event.key == K_p:
                paused = not paused
                print "Paused." if paused else "Un-paused."
            if event.key == K_q:
                pygame.event.post(pygame.event.Event(QUIT))
            if event.key == K_ESCAPE:
                throwing = False
                if throwing_disk is not None \
                   and throwing_disk.visuals is not None:
                    throwing_disk.visuals.guide = None
                throwing_disk = None

    pygame.display.update()
    dt = fps_clock.tick(30)
    if not paused:
        # fixed time-step for physics
        world.update(33 / 1000.0)
