import pygame
import math

class Block():
    def __init__(self, world, pos):
        self._class = "block"
        self.world = world
        self.pos = pos
        self.world.field[pos[0]][pos[1]] = self
        self.image = pygame.Surface((16, 16))
        self.image_zoom = 1
        self.has_hitbox = 1

    def update(self, events):
        pass

    def draw(self, screen):
        pass