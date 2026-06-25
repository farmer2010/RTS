from blocks.block import *
from blocks.air import *
from blocks.stone import *
from blocks.sand import *
from blocks.water import *
from blocks.grass import *
from blocks.conveyor import *
from blocks.router import *

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