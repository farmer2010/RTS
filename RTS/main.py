from farmgui import *
from world import *
import pygame
pygame.init()

screen = pygame.display.set_mode((1920, 1080))
pygame.display.set_caption("RTS game")
keep_going = 1
timer = pygame.time.Clock()

buttons = ButtonManager(background_color=(255, 255, 255))
buttons.add(World())

font = pygame.font.SysFont(None, 25)

while keep_going:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            keep_going = 0
    #
    screen.fill((255, 255, 255))
    buttons.update(screen, events)
    screen.blit(font.render(str(round(timer.get_fps(), 2)), True, (255, 0, 0)), (0, 0))
    pygame.display.update()
    timer.tick(60)
pygame.quit()