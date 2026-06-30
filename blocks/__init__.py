from textures import *

from blocks.block import *
from blocks.air import *
from blocks.stone import *
from blocks.sand import *
from blocks.water import *
from blocks.grass import *
from blocks.conveyor import *
from blocks.router import *
from blocks.junction import *
from blocks.sorter import *
from blocks.item_vacuum import *
from blocks.gate import *
from blocks.wall import *
from blocks.turret import *
from blocks.stone_floor import *
from blocks.drill import *
from blocks.factory import *
from blocks.work_in_progress import *
from blocks.ore import *
from blocks.sandy_water import *
from blocks.core import *

def set_block(world, pos, player, type, rotate=0):
    if world.field[pos[0]][pos[1]].type == "air" or world.field[pos[0]][pos[1]].type == "work in progress":
        if type == "stone":
            world.field[pos[0]][pos[1]] = Stone(world, pos)
        elif type == "coal ore":
            world.field[pos[0]][pos[1]] = Ore(world, pos, "coal ore")
        elif type == "iron ore":
            world.field[pos[0]][pos[1]] = Ore(world, pos, "iron ore")
        elif type == "copper ore":
            world.field[pos[0]][pos[1]] = Ore(world, pos, "copper ore")
        elif type == "water":
            world.field[pos[0]][pos[1]] = Water(world, pos)
        elif type == "conveyor":
            world.field[pos[0]][pos[1]] = Conveyor(world, pos, player, rotate=rotate)
        elif type == "router":
            world.field[pos[0]][pos[1]] = Router(world, pos, player)
        elif type == "junction":
            world.field[pos[0]][pos[1]] = Junction(world, pos, player)
        elif type == "sorter":
            world.field[pos[0]][pos[1]] = Sorter(world, pos, player, "sorter")
        elif type == "inverted sorter":
            world.field[pos[0]][pos[1]] = Sorter(world, pos, player, "inverted sorter")
        elif type == "overflow gate":
            world.field[pos[0]][pos[1]] = Gate(world, pos, player, "overflow gate")
        elif type == "underflow gate":
            world.field[pos[0]][pos[1]] = Gate(world, pos, player, "underflow gate")
        elif type == "stone wall":
            world.field[pos[0]][pos[1]] = Wall(world, pos, player, "stone wall")
        elif type == "iron wall":
            world.field[pos[0]][pos[1]] = Wall(world, pos, player, "iron wall")
        elif type == "stone turret":
            world.field[pos[0]][pos[1]] = Turret(world, pos, player, "stone turret")
        elif type == "drill":
            world.field[pos[0]][pos[1]] = Drill(world, pos, player, "drill")
        elif type == "iron furnace":
            world.field[pos[0]][pos[1]] = Factory(world, pos, player, "iron furnace")
        elif type == "copper furnace":
            world.field[pos[0]][pos[1]] = Factory(world, pos, player, "copper furnace")
        if world.player.fog[pos[0]][pos[1]] == 2:
            world.update_minimap(pos)
        world.chunks[pos[0] // 16][pos[1] // 16].update_image()

def get_block(type):
    if type == "air":
        return(Air)
    elif type == "stone":
        return(Stone)
    elif type == "sand":
        return(Sand)
    elif type == "grass":
        return(Grass)
    elif type == "water":
        return(Water)

def get_block_image(type):
    if type == "conveyor":
        return(pygame.transform.scale(conveyors[0][0], (48, 48)))
    elif type == "router":
        return(pygame.transform.scale(router_img, (48, 48)))
    elif type == "junction":
        return(pygame.transform.scale(junction_img, (48, 48)))
    elif type == "sorter":
        return(pygame.transform.scale(sorter_images[""], (48, 48)))
    elif type == "inverted sorter":
        return(pygame.transform.scale(inverted_sorter_images[""], (48, 48)))
    elif type == "overflow gate":
        return(pygame.transform.scale(overflow_gate_img, (48, 48)))
    elif type == "underflow gate":
        return(pygame.transform.scale(underflow_gate_img, (48, 48)))
    elif type == "stone wall":
        return(pygame.transform.scale(stone_wall_img, (48, 48)))
    elif type == "iron wall":
        return(pygame.transform.scale(iron_wall_img, (48, 48)))
    elif type == "stone turret":
        img = pygame.transform.scale(small_turret_img, (48, 48))
        img.blit(pygame.transform.scale(stone_turret_img, (48, 48)), (0, 0))
        return(img)
    elif type == "drill":
        return(pygame.transform.scale(drill_images["stone"], (48, 48)))
    elif type == "iron furnace":
        return(pygame.transform.scale(iron_furnace_img, (48, 48)))
    elif type == "copper furnace":
        return(pygame.transform.scale(copper_furnace_img, (48, 48)))
    else:
        return(pygame.Surface((48, 48)))

def get_block_preview(type, rotate=0):
    img = pygame.Surface((16, 16))
    if type == "conveyor":
        img.blit(conveyors[rotate][0], (0, 0))
    elif type == "router":
        img.blit(router_img, (0, 0))
    elif type == "junction":
        img.blit(junction_img, (0, 0))
    elif type == "sorter":
        img.blit(sorter_images[""], (0, 0))
    elif type == "inverted sorter":
        img.blit(inverted_sorter_images[""], (0, 0))
    elif type == "overflow gate":
        img.blit(overflow_gate_img, (0, 0))
    elif type == "underflow gate":
        img.blit(underflow_gate_img, (0, 0))
    elif type == "stone wall":
        img.blit(stone_wall_img, (0, 0))
    elif type == "iron wall":
        img.blit(iron_wall_img, (0, 0))
    elif type == "stone turret":
        img.blit(small_turret_img, (0, 0))
        img.blit(stone_turret_img, (0, 0))
    elif type == "drill":
        img.blit(drill_images["stone"], (0, 0))
    elif type == "iron furnace":
        img.blit(iron_furnace_img, (0, 0))
    elif type == "copper furnace":
        img.blit(copper_furnace_img, (0, 0))
    #
    img2 = pygame.Surface((16, 16), pygame.SRCALPHA)
    img2.fill((0, 128, 255, 128))
    img.blit(img2, (0, 0))
    img.set_alpha(128)
    return(img)

cost = {
    "stone" : [
        ["stone", 3]
    ],
    "coal ore" : [
        ["stone", 2],
        ["coal", 2]
    ],
    "iron ore" : [
        ["stone", 2],
        ["iron", 2]
    ],
    "copper ore": [
        ["stone", 2],
        ["copper", 2]
    ],
    "conveyor": [
        ["stone", 1]
    ],
    "router": [
        ["stone", 3],
    ],
    "junction": [
        ["stone", 3],
    ],
    "sorter": [
        ["stone", 5],
        ["iron", 1]
    ],
    "inverted sorter": [
        ["stone", 5],
        ["iron", 1]
    ],
    "overflow gate": [
        ["stone", 6],
        ["iron", 2],
        ["copper", 1]
    ],
    "underflow gate": [
        ["stone", 6],
        ["iron", 2],
        ["copper", 1]
    ],
    "drill" : [
        ["stone", 12],
        ["iron ore", 8],
        ["copper ore", 5]
    ],
    "stone wall": [
        ["stone", 25],
    ],
    "iron wall": [
        ["iron bar", 25],
    ],
    "steel wall": [
        ["steel", 25],
    ],
    "stone turret": [
        ["stone", 40],
        ["iron", 10]
    ],
    "iron furnace": [
        ["stone", 30],
        ["iron", 15],
        ["copper", 10]
    ],
    "copper furnace": [
        ["stone", 30],
        ["iron", 10],
        ["copper", 15]
    ],
}

build_time = {
    "stone" : 70,
    "coal ore" : 120,
    "iron ore" : 120,
    "copper ore": 120,
    "conveyor" : 5,
    "router" : 5,
    "junction" : 5,
    "sorter" : 10,
    "inverted sorter" : 10,
    "overflow gate" : 10,
    "underflow gate" : 10,
    "drill" : 40,
    "stone wall" : 120,#120
    "iron wall" : 220,
    "stone turret" : 600,
    "iron furnace" : 180,
    "copper furnace" : 180,
}