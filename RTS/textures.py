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

conveyors = [
    [#up
        pygame.image.load("files/images/conveyor1.png"),
        pygame.image.load("files/images/conveyor2.png"),
        pygame.image.load("files/images/conveyor1.png"),
        pygame.image.load("files/images/conveyor3.png"),
        pygame.image.load("files/images/conveyor4.png"),
        pygame.image.load("files/images/conveyor5.png"),
        pygame.image.load("files/images/conveyor6.png"),
        pygame.image.load("files/images/conveyor7.png")
    ],
    [#right
        pygame.transform.rotate(pygame.image.load("files/images/conveyor1.png"), 270),
        pygame.transform.rotate(pygame.image.load("files/images/conveyor2.png"), 270),
        pygame.transform.rotate(pygame.image.load("files/images/conveyor1.png"), 270),
        pygame.transform.rotate(pygame.image.load("files/images/conveyor3.png"), 270),
        pygame.transform.rotate(pygame.image.load("files/images/conveyor4.png"), 270),
        pygame.transform.rotate(pygame.image.load("files/images/conveyor5.png"), 270),
        pygame.transform.rotate(pygame.image.load("files/images/conveyor6.png"), 270),
        pygame.transform.rotate(pygame.image.load("files/images/conveyor7.png"), 270),
    ],
    [#down
        pygame.transform.rotate(pygame.image.load("files/images/conveyor1.png"), 180),
        pygame.transform.rotate(pygame.image.load("files/images/conveyor2.png"), 180),
        pygame.transform.rotate(pygame.image.load("files/images/conveyor1.png"), 180),
        pygame.transform.rotate(pygame.image.load("files/images/conveyor3.png"), 180),
        pygame.transform.rotate(pygame.image.load("files/images/conveyor4.png"), 180),
        pygame.transform.rotate(pygame.image.load("files/images/conveyor5.png"), 180),
        pygame.transform.rotate(pygame.image.load("files/images/conveyor6.png"), 180),
        pygame.transform.rotate(pygame.image.load("files/images/conveyor7.png"), 180),
    ],
    [#left
        pygame.transform.rotate(pygame.image.load("files/images/conveyor1.png"), 90),
        pygame.transform.rotate(pygame.image.load("files/images/conveyor2.png"), 90),
        pygame.transform.rotate(pygame.image.load("files/images/conveyor1.png"), 90),
        pygame.transform.rotate(pygame.image.load("files/images/conveyor3.png"), 90),
        pygame.transform.rotate(pygame.image.load("files/images/conveyor4.png"), 90),
        pygame.transform.rotate(pygame.image.load("files/images/conveyor5.png"), 90),
        pygame.transform.rotate(pygame.image.load("files/images/conveyor6.png"), 90),
        pygame.transform.rotate(pygame.image.load("files/images/conveyor7.png"), 90),
    ]
]

items = {
    "stone" : pygame.image.load("files/images/item_stone.png"),
    "coal" : pygame.image.load("files/images/item_coal.png"),
}

dig_img = pygame.Surface((16, 16), pygame.SRCALPHA)
dig_img.fill((255, 0, 0, 50))
fog_img = pygame.Surface((16, 16), pygame.SRCALPHA)
fog_img.fill((0, 0, 0, 128))