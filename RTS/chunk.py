import pygame
import math

class Chunk():
    def __init__(self, world, pos):
        self.world = world
        self.pos = pos
        self.image = pygame.Surface((256, 256))
        self.scaled_image = pygame.Surface((256, 256))
        self.image_zoom = 0.999
        self.objects = []
        for x in range(16):
            for y in range(16):
                self.image.blit(self.world.field[self.pos[0] * 16 + x][self.pos[1] * 16 + y].image, (x * 16, y * 16))

    def draw(self, screen):
        if self.world.zoom != self.image_zoom:
            self.image_zoom = self.world.zoom
            self.scaled_image = pygame.transform.scale(self.image, (math.ceil(256 * self.world.zoom), math.ceil(256 * self.world.zoom)))
        screen.blit(self.scaled_image,
                    [(self.pos[0] - self.world.cam_pos[0] / 256) * 256 * self.world.zoom + self.world.display_W / 2,
                     (self.pos[1] - self.world.cam_pos[1] / 256) * 256 * self.world.zoom + self.world.display_H / 2])

    def update_image(self):
        self.image = pygame.Surface((256, 256))
        for x in range(16):
            for y in range(16):
                self.image.blit(self.world.field[self.pos[0] * 16 + x][self.pos[1] * 16 + y].image, (x * 16, y * 16))
        self.scaled_image = pygame.transform.scale(self.image, (math.ceil(256 * self.world.zoom), math.ceil(256 * self.world.zoom)))