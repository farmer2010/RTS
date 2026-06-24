import pygame
import math
from blocks import *

class Block():
    def __init__(self, world, type, pos):
        self._class = "block"
        self.type = type
        self.world = world
        self.pos = pos
        self.image = pygame.Surface((16, 16))
        self.has_hitbox = 1
        self.progress = 1000#прогресс ломания
        self.mining_speed = 50
        self.speed = 1
        self.can_mined = 0
        self.health = 100

    def update(self, events):
        pass

    def remove_block(self):
        self.world.field[self.pos[0]][self.pos[1]] = self.world.air_generator(self.world, self.pos)
        self.world.chunks[int(self.pos[0] // 16)][int(self.pos[1] // 16)].image_changes = 1
        self.world.player.task_units[self.pos[0]][self.pos[1]] = None
        self.world.player.task_field[self.pos[0]][self.pos[1]] = 0

    def draw(self, screen):
        pos = self.world.game_to_display([self.pos[0] * 16, self.pos[1] * 16])
        screen.blit(self.image, pos)