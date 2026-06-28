import pygame
import math
from textures import *
from blocks import *

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
        #
        self.fog_changes = 0
        self.image_changes = 0
        self.fog_blocks = [[pygame.Surface((16, 16), pygame.SRCALPHA) for x in range(16)] for y in range(16)]

    def draw(self, screen):
        if self.world.zoom != self.image_zoom:
            self.image_zoom = self.world.zoom
            self.scaled_image = pygame.transform.scale(self.image, (math.ceil(256 * self.world.zoom), math.ceil(256 * self.world.zoom)))
            self.scaled_fog_image = pygame.transform.scale(self.fog_image, (math.ceil(256 * self.world.zoom), math.ceil(256 * self.world.zoom)))
        screen.blit(self.scaled_image,
                    [(self.pos[0] - self.world.cam_pos[0] / 256) * 256 * self.world.zoom + self.world.display_W / 2,
                     (self.pos[1] - self.world.cam_pos[1] / 256) * 256 * self.world.zoom + self.world.display_H / 2])

    def update_image(self):
        for x in range(16):
            for y in range(16):
                self.image.blit(self.draw_block_image((self.pos[0] * 16 + x, self.pos[1] * 16 + y)), (x * 16, y * 16))
        self.scaled_image = pygame.transform.scale(self.image, (math.ceil(256 * self.world.zoom), math.ceil(256 * self.world.zoom)))

    def update_fog_image(self):
        self.fog_image.fill((0, 0, 0, 0))
        for x in range(16):
            for y in range(16):
                if self.world.player.fog[self.pos[0] * 16 + x][self.pos[1] * 16 + y] == 0:
                    self.fog_image.blit(self.dark_img, (x * 16, y * 16))
                elif self.world.player.fog[self.pos[0] * 16 + x][self.pos[1] * 16 + y] == 1:
                    self.fog_image.blit(self.fog_blocks[x][y], (x * 16, y * 16))
                    self.fog_image.blit(fog_img, (x * 16, y * 16))
                #self.fog[x][y] = self.world.player.fog[self.pos[0] * 16 + x][self.pos[1] * 16 + y]
        self.scaled_fog_image = pygame.transform.scale(self.fog_image, (math.ceil(256 * self.world.zoom), math.ceil(256 * self.world.zoom)))

    def draw_block_image(self, pos):
        img = pygame.Surface((16, 16))
        bl = self.world.field[pos[0]][pos[1]]
        if bl.type == "air" or bl.type == "work in progress":
            img.blit(self.world.ground_field[pos[0]][pos[1]].get_image(), (0, 0))
            if self.world.ore_field[pos[0]][pos[1]] != None:
                img.blit(ore_img[self.world.ore_field[pos[0]][pos[1]][0]], (0, 0))
        img.blit(bl.get_image(), (0, 0))
        if bl.player is self.world.players[1]:
            img.blit(enemy_edge_img, (0, 0))
        if bl.type != "work in progress":
            pr = int((1000 - bl.progress) // 170)
            if pr > 0:
                img.blit(crack[pr - 1], (0, 0))
        ts = self.world.player.task_field[pos[0]][pos[1]]
        if ts == 1:
            img.blit(dig_img, (0, 0))
        elif ts != 0:
            img.blit(get_block_preview(ts[0], rotate=ts[1]))
        return(img)

    def redraw_block(self, pos):
        self.image.blit(self.draw_block_image(pos), (pos[0] % 16 * 16, pos[1] % 16 * 16))
        self.scaled_image = pygame.transform.scale(self.image, (math.ceil(256 * self.world.zoom), math.ceil(256 * self.world.zoom)))