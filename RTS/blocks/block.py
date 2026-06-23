import pygame
import math

class Block():
    def __init__(self, world, type, pos):
        self._class = "block"
        self.type = type
        self.world = world
        self.pos = pos
        self.image = pygame.Surface((16, 16))
        self.has_hitbox = 1
        self.progress = 100#прогресс ломания
        self.speed = 1
        self.can_mined = 0

    def update(self, events):
        pass

    def draw(self, screen):
        pos = self.world.game_to_display([self.pos[0] * 16, self.pos[1] * 16])
        screen.blit(self.image, pos)