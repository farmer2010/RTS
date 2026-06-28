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

def set_block(world, pos, player, type, rotate=0):
    if world.field[pos[0]][pos[1]].type == "air":
        if type == "stone":
            world.field[pos[0]][pos[1]] = Stone(world, pos)
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