import pygame
import sys
from pygame.locals import *
import pygame.gfxdraw

pygame.init()
fps_clock = pygame.time.Clock()

window_surface = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Circle Test")

white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)

class Circle:
    def __init__(self, x, y, r, color, v=(0, 0)):
        self.x = float(x)
        self.y = float(y)
        self.r = float(r)
        self.v = v
        self.color = color

    def update(self, dt):
        self.x += self.v[0] * dt
        self.y += self.v[1] * dt

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), int(self.r), 0)

c1 = Circle(300, 50, 20, white, (0, 0.2))

dt = 0

while True:
    window_surface.fill(blue)

    c1.update(dt)
    c1.draw(window_surface)

    for event in pygame.event.get():
        if event.type == QUIT:
            print "Going away!"
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_LEFT:
                c1.v = c1.v[0] - .1, c1.v[1]
            if event.key == K_RIGHT:
                c1.v = c1.v[0] + .1, c1.v[1]
            if event.key == K_UP:
                c1.v = c1.v[0], c1.v[1] - .1
            if event.key == K_DOWN:
                c1.v = c1.v[0], c1.v[1] + .1
            c1.v = round(c1.v[0], 4), round(c1.v[1], 4)
            print "New speed:", c1.v
            if event.key == K_q:
                pygame.event.post(pygame.event.Event(QUIT))

    pygame.display.update()
    dt = fps_clock.tick(30)
