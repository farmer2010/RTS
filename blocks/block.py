import pygame
import math
from blocks import *

class Block():
    def __init__(self, world, type, pos, player=None, health=50):
        self._class = "block"
        self.type = type
        self.player = player
        self.world = world
        self.pos = pos
        self.image = pygame.Surface((16, 16))
        self.has_hitbox = 1
        self.progress = 1000#прогресс ломания
        self.mining_speed = 50
        self.speed = 1
        self.can_mined = 0
        self.health = health
        self.max_health = health
        self.is_conveyor = 0
        self.is_construction = 0
        self.killed = 0

    def update(self, events):
        pass

    def remove_block(self):
        self.world.field[self.pos[0]][self.pos[1]] = self.world.air_generator(self.world, self.pos)
        self.world.chunks[int(self.pos[0] // 16)][int(self.pos[1] // 16)].image_changes = 1
        self.world.player.task_units[self.pos[0]][self.pos[1]] = None
        self.world.player.task_field[self.pos[0]][self.pos[1]] = 0
        self.killed = 1
        if self.world.player.fog[self.pos[0]][self.pos[1]] == 2:
            self.world.update_minimap(self.pos)

    def kill(self):
        self.remove_block()
        self.killed = 1

    def draw(self, screen):
        pos = self.world.game_to_display([self.pos[0] * 16, self.pos[1] * 16])
        screen.blit(self.image, pos)

    def get_image(self):
        return(self.image)

    def is_connect_conveyor(self, rotate):
        return(False)

    def can_take_item(self, rotate):
        return(False)

    def action(self):#нажатие на блок
        pass