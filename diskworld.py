import pygame
import sys
from pygame.locals import *
from disk import Disk
from vector import Vector
from point import Point
from world import World
from camera import Camera
from renderer import Renderer, Guide

pygame.init()
fps_clock = pygame.time.Clock()

window_surface = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Circle Test")

white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)

paused = True
dragging = False
dragging_start = None
panning = False
panning_start = None
d1 = Disk(Point(20, 20), 2, 1, white, Vector(0, 0))
d2 = Disk(Point(10, 10), 5, 5.97219e+14, white, Vector(0, 0))

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
                elif abs(p - d2.center) > d2.radius:
                    # outside both disks. start panning
                    panning = True
                    panning_start = event.pos
            elif event.button == 4: # scroll up
                camera.zoom(0.1)
            elif event.button == 5: # scroll down
                camera.zoom(-0.1)
        elif event.type == MOUSEMOTION:
            if dragging:
                if len(renderer.guides) == 0:
                    renderer.guides.append(Guide())
                    renderer.guides[0].disk = d1
                renderer.guides[0].start = d1.center
                renderer.guides[0].end = renderer.surfaceToWorldCoord(event.pos)
            elif panning:
                new_pos = event.pos
                p1 = renderer.surfaceToWorldCoord(panning_start)
                p2 = renderer.surfaceToWorldCoord(new_pos)
                v = p1 - p2
                panning_start = new_pos
                camera.pan(v)
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
                    d1.velocity = p2 - p1
                    renderer.guides = []
                    paused = False
                dragging = False
                panning = False
        elif event.type == KEYDOWN:
            if event.key == K_n:
                world.update(dt / 1000.0)
            if event.key == K_p:
                paused = not paused
                print "Paused." if paused else "Un-paused."
            if event.key == K_q:
                pygame.event.post(pygame.event.Event(QUIT))
            if event.key == K_ESCAPE:
                dragging = False
                renderer.guides = []

    pygame.display.update()
    dt = fps_clock.tick(30)
    if not paused:
        # fixed time-step for physics
        world.update(33 / 1000.0)
