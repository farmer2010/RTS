import pygame
import math
from textures import *

class Chunk():
    def __init__(self, world, pos):
        self.world = world
        self.pos = pos
        self.image = pygame.Surface((256, 256), pygame.SRCALPHA)
        self.fog_image = pygame.Surface((256, 256), pygame.SRCALPHA)
        self.scaled_image = pygame.Surface((256, 256), pygame.SRCALPHA)
        self.scaled_fog_image = pygame.Surface((256, 256), pygame.SRCALPHA)
        #
        self.fog_image.fill((0, 0, 0, 255))
        self.dark_img = pygame.Surface((16, 16), pygame.SRCALPHA)
        self.dark_img.fill((0, 0, 0))
        self.inv_img = pygame.Surface((16, 16), pygame.SRCALPHA)
        #
        self.image_zoom = 0.999
        self.objects = []
        self.update_image()

    def draw(self, screen):
        if self.world.zoom != self.image_zoom:
            self.image_zoom = self.world.zoom
            self.scaled_image = pygame.transform.scale(self.image, (math.ceil(256 * self.world.zoom), math.ceil(256 * self.world.zoom)))
            #self.scaled_fog_image = pygame.transform.scale(self.fog_image, (math.ceil(256 * self.world.zoom), math.ceil(256 * self.world.zoom)))
        screen.blit(self.scaled_image,
                    [(self.pos[0] - self.world.cam_pos[0] / 256) * 256 * self.world.zoom + self.world.display_W / 2,
                     (self.pos[1] - self.world.cam_pos[1] / 256) * 256 * self.world.zoom + self.world.display_H / 2])

    def update_image(self):
        self.fog_image.fill((0, 0, 0, 0))
        self.image = pygame.Surface((256, 256), pygame.SRCALPHA)
        for x in range(16):
            for y in range(16):
                if self.world.field[self.pos[0] * 16 + x][self.pos[1] * 16 + y].type == "air":
                    self.image.blit(self.world.ground_field[self.pos[0] * 16 + x][self.pos[1] * 16 + y].image,(x * 16, y * 16))
                self.image.blit(self.world.field[self.pos[0] * 16 + x][self.pos[1] * 16 + y].image, (x * 16, y * 16))
                if self.world.player.task_field[self.pos[0] * 16 + x][self.pos[1] * 16 + y] == 1:
                    self.image.blit(dig_img,(x * 16, y * 16))
                #if self.world.player.fog[self.pos[0] * 16 + x][self.pos[1] * 16 + y] == 0:
                #    self.fog_image.blit(self.dark_img, (x * 16, y * 16))
                #else:
                #    self.fog_image.blit(self.inv_img, (x * 16, y * 16))
        self.scaled_image = pygame.transform.scale(self.image, (math.ceil(256 * self.world.zoom), math.ceil(256 * self.world.zoom)))
        #self.scaled_fog_image = pygame.transform.scale(self.fog_image, (math.ceil(256 * self.world.zoom), math.ceil(256 * self.world.zoom)))