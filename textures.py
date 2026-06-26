import pygame

'''
цвета предметов:
камень - #636363
уголь - #1e1e1e
'''

stone_img = pygame.image.load("files/images/stone.png")
grass_img = pygame.image.load("files/images/grass.png")
sand_img = pygame.image.load("files/images/sand.png")
water_img = pygame.image.load("files/images/water.png")
router_img = pygame.image.load("files/images/router.png")
junction_img = pygame.image.load("files/images/junction.png")
overflow_gate_img = pygame.image.load("files/images/overflow_gate.png")
underflow_gate_img = pygame.image.load("files/images/underflow_gate.png")
stone_wall_img = pygame.image.load("files/images/stone_wall.png")
iron_wall_img = pygame.image.load("files/images/iron_wall.png")
enemy_edge_img = pygame.image.load("files/images/enemy_edge.png")
small_turret_img = pygame.image.load("files/images/small_turret.png")
stone_turret_img = pygame.image.load("files/images/stone_turret.png")

hbbar = [
    pygame.image.load("files/images/hpbar1.png"),
    pygame.image.load("files/images/hpbar2.png"),
    pygame.image.load("files/images/hpbar3.png"),
    pygame.image.load("files/images/hpbar4.png"),
    pygame.image.load("files/images/hpbar5.png"),
    pygame.image.load("files/images/hpbar6.png"),
    pygame.image.load("files/images/hpbar7.png"),
    pygame.image.load("files/images/hpbar8.png"),
    pygame.image.load("files/images/hpbar9.png"),
    pygame.image.load("files/images/hpbar10.png")
]

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

sorter_images = {
    "" : pygame.image.load("files/images/sorter_null.png"),#не выбран предмет
    "stone" : pygame.image.load("files/images/sorter_stone.png"),
    "coal" : pygame.image.load("files/images/sorter_coal.png"),
}
inverted_sorter_images = {
    "" : pygame.image.load("files/images/inverted_sorter_null.png"),
    "stone" : pygame.image.load("files/images/inverted_sorter_stone.png"),
    "coal" : pygame.image.load("files/images/inverted_sorter_coal.png"),
}

items = {
    "" : pygame.image.load("files/images/item_null.png"),
    "stone" : pygame.image.load("files/images/item_stone.png"),
    "coal" : pygame.image.load("files/images/item_coal.png"),
}

dig_img = pygame.Surface((16, 16), pygame.SRCALPHA)
dig_img.fill((255, 0, 0, 50))
fog_img = pygame.Surface((16, 16), pygame.SRCALPHA)
fog_img.fill((0, 0, 0, 128))