import pygame
from entity import *

class Projectile(Entity):
    def __init__(self, world, pos, w, h, rotate, speed, distance):
        Entity.__init__(self, world, "bullet", pos, w, h)
        self.world = world
        self.pos = pos
        self.w = w
        self.h = h
        self.rotate = rotate
        self.speed = speed
        self.max_distance = distance
        self.distance = 0
        self.image.fill((0, 0, 255))

    def update(self, events):
        self.move(self.speed, self.rotate)
        self.distance += self.speed
        if self.distance >= self.max_distance:
            self.kill()

    def move(self, speed, rotate):
        if not self.collide(0, 0)[0]:
            dx = math.cos(rotate) * speed
            dy = math.sin(rotate) * speed
            self.pos[0] += dx
            self.pos[1] += dy
        else:
            self.kill()