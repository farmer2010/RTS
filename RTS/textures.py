import pygame

stone_img = pygame.image.load("files/images/stone.png")
grass_img = pygame.image.load("files/images/grass.png")
sand_img = pygame.image.load("files/images/sand.png")
water_img = pygame.image.load("files/images/water.png")

crack = [
    pygame.image.load("files/images/crack1.png"),
    pygame.image.load("files/images/crack2.png"),
    pygame.image.load("files/images/crack3.png"),
    pygame.image.load("files/images/crack4.png"),
    pygame.image.load("files/images/crack5.png")
]

dig_img = pygame.Surface((16, 16), pygame.SRCALPHA)
dig_img.fill((255, 0, 0, 50))
fog_img = pygame.Surface((16, 16), pygame.SRCALPHA)
fog_img.fill((0, 0, 0, 128))