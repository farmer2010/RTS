from farmgui import *
from opensimplex import *
import pygame
from random import randint as rand
import pyperclip
pygame.init()

W = pygame.display.Info().current_w
H = pygame.display.Info().current_h
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Worldgen test")
keep_going = 1
timer = pygame.time.Clock()
font12 = pygame.font.Font("files/Better VCR 6.1.ttf", 12)
font16 = pygame.font.Font("files/Better VCR 6.1.ttf", 16)

w = 256
h = 256
img = pygame.Surface((w, h))

field = [[0 for y in range(h)] for x in range(w)]
ore = [[None for y in range(h)] for x in range(w)]

def regen():
    for x in range(w):
        for y in range(h):
            field[x][y] = 0
            ore[x][y] = 0
    generate(slider1.get_value(), slider2.get_value(), slider3.get_value(), slider4.get_value(), slider5.get_value(), slider6.get_value())

def copy_params():
    txt = ""
    txt += str(slider1.get_value()) + " "
    txt += str(slider2.get_value()) + " "
    txt += str(int(radiobutton1.get_selected())) + " "
    txt += str(slider3.get_value()) + " "
    txt += str(slider4.get_value()) + " "
    txt += str(int(radiobutton2.get_selected())) + " "
    txt += str(slider5.get_value()) + " "
    txt += str(slider6.get_value()) + " "
    txt += str(slider7.get_value()) + " "
    txt += str(slider8.get_value()) + " "
    txt += str(slider9.get_value()) + " "
    txt += str(slider10.get_value()) + " "
    pyperclip.copy(txt)

def paste_params():
    txt = pyperclip.paste().split(" ")
    slider1.set_value(float(txt[0]))
    slider2.set_value(float(txt[1]))
    radiobutton1.set_selected(int(txt[2]))
    slider3.set_value(float(txt[3]))
    slider4.set_value(float(txt[4]))
    radiobutton2.set_selected(int(txt[5]))
    slider5.set_value(float(txt[6]))
    slider6.set_value(float(txt[7]))
    slider7.set_value(float(txt[8]))
    slider8.set_value(float(txt[9]))
    slider9.set_value(float(txt[10]))
    slider10.set_value(float(txt[11]))

def copy_ore():
    txt = ""
    txt += str(slider11.get_value()) + " "
    txt += str(slider12.get_value()) + " "
    txt += str(int(radiobutton3.get_selected())) + " "
    txt += str(slider13.get_value()) + " "
    txt += str(slider14.get_value()) + " "
    txt += str(slider15.get_value()) + " "
    txt += str(slider16.get_value()) + " "
    pyperclip.copy(txt)

def paste_ore():
    txt = pyperclip.paste().split(" ")
    slider11.set_value(float(txt[0]))
    slider12.set_value(float(txt[1]))
    radiobutton3.set_selected(int(txt[2]))
    slider13.set_value(float(txt[3]))
    slider14.set_value(float(txt[4]))
    slider15.set_value(float(txt[5]))
    slider16.set_value(float(txt[6]))

buttons = ButtonManager(background_color=(0, 0, 0, 0))
buttons.add(TextLabel("LANDSCAPE: ", (0, 0), font=font16))
#
buttons.add(TextLabel("Octave 1: ", (0, 20), font=font16))
slider1 = Slider((0, 40, 350, 30), (22, 22), preset_value=0.1, min_value=0, max_value=1, period=3, font_size=20, font_color=(200, 200, 200))
slider1.add_update_text(lambda x: "scaling: " + str(x))
buttons.add(slider1)
slider2 = Slider((0, 70, 350, 30), (22, 22), preset_value=1, min_value=0, max_value=1, period=3, font_size=20, font_color=(200, 200, 200))
slider2.add_update_text(lambda x: "amplitude: " + str(x))
buttons.add(slider2)
#
buttons.add(TextLabel("Octave 2: ", (0, 100), font=font16))
slider3 = Slider((0, 120, 350, 30), (22, 22), preset_value=0.1, min_value=0, max_value=1, period=3, font_size=20, font_color=(200, 200, 200))
slider3.add_update_text(lambda x: "scaling: " + str(x))
buttons.add(slider3)
slider4 = Slider((0, 150, 350, 30), (22, 22), preset_value=1, min_value=0, max_value=1, period=3, font_size=20, font_color=(200, 200, 200))
slider4.add_update_text(lambda x: "amplitude: " + str(x))
buttons.add(slider4)
radiobutton1 = RadioButton((150, 100, 20, 20), text="Enable", offset=1, font=font16)
buttons.add(radiobutton1)
#
buttons.add(TextLabel("Octave 3: ", (0, 180), font=font16))
slider5 = Slider((0, 200, 350, 30), (22, 22), preset_value=0.1, min_value=0, max_value=1, period=3, font_size=20, font_color=(200, 200, 200))
slider5.add_update_text(lambda x: "scaling: " + str(x))
buttons.add(slider5)
slider6 = Slider((0, 230, 350, 30), (22, 22), preset_value=1, min_value=0, max_value=1, period=3, font_size=20, font_color=(200, 200, 200))
slider6.add_update_text(lambda x: "amplitude: " + str(x))
buttons.add(slider6)
radiobutton2 = RadioButton((150, 180, 20, 20), text="Enable", offset=1, font=font16)
buttons.add(radiobutton2)
#
buttons.add(TextLabel("Levels: ", (0, 260), font=font16))
#
slider7 = Slider((0, 280, 350, 30), (22, 22), preset_value=1, min_value=0, max_value=2, period=3, font_size=20, font_color=(200, 200, 200))
slider7.add_update_text(lambda x: "water level: " + str(round(x - 1, 3)))
buttons.add(slider7)
#
slider8 = Slider((0, 310, 350, 30), (22, 22), preset_value=1.1, min_value=0, max_value=2, period=3, font_size=20, font_color=(200, 200, 200))
slider8.add_update_text(lambda x: "sandy water level: " + str(round(x - 1, 3)))
buttons.add(slider8)
#
slider9 = Slider((0, 340, 350, 30), (22, 22), preset_value=1.2, min_value=0, max_value=2, period=3, font_size=20, font_color=(200, 200, 200))
slider9.add_update_text(lambda x: "sand level: " + str(round(x - 1, 3)))
buttons.add(slider9)
#
slider10 = Slider((0, 370, 350, 30), (22, 22), preset_value=1.3, min_value=0, max_value=2, period=3, font_size=20, font_color=(200, 200, 200))
slider10.add_update_text(lambda x: "grass level: " + str(round(x - 1, 3)))
buttons.add(slider10)
#
#
#
buttons.add(TextLabel("ORE: ", (0, 400), font=font16))
#
buttons.add(TextLabel("Octave 1: ", (0, 420), font=font16))
slider11 = Slider((0, 440, 350, 30), (22, 22), preset_value=0.1, min_value=0, max_value=1, period=3, font_size=20, font_color=(200, 200, 200))
slider11.add_update_text(lambda x: "scaling: " + str(x))
buttons.add(slider11)
slider12 = Slider((0, 470, 350, 30), (22, 22), preset_value=1, min_value=0, max_value=1, period=3, font_size=20, font_color=(200, 200, 200))
slider12.add_update_text(lambda x: "amplitude: " + str(x))
buttons.add(slider12)
#
buttons.add(TextLabel("Octave 2: ", (0, 500), font=font16))
slider13 = Slider((0, 520, 350, 30), (22, 22), preset_value=0.1, min_value=0, max_value=1, period=3, font_size=20, font_color=(200, 200, 200))
slider13.add_update_text(lambda x: "scaling: " + str(x))
buttons.add(slider13)
slider14 = Slider((0, 550, 350, 30), (22, 22), preset_value=1, min_value=0, max_value=1, period=3, font_size=20, font_color=(200, 200, 200))
slider14.add_update_text(lambda x: "amplitude: " + str(x))
buttons.add(slider14)
radiobutton3 = RadioButton((150, 500, 20, 20), text="Enable", offset=1, font=font16)
buttons.add(radiobutton3)
#
buttons.add(TextLabel("Level: ", (0, 580), font=font16))
slider15 = Slider((0, 600, 350, 30), (22, 22), preset_value=1, min_value=0, max_value=2, period=3, font_size=20, font_color=(200, 200, 200))
slider15.add_update_text(lambda x: "vein level: " + str(round(x - 1, 3)))
buttons.add(slider15)
slider16 = Slider((0, 630, 350, 30), (22, 22), preset_value=1, min_value=0, max_value=2, period=3, font_size=20, font_color=(200, 200, 200))
slider16.add_update_text(lambda x: "cluster level: " + str(round(x - 1, 3)))
buttons.add(slider16)
#
#
gen_button = Button((120, 0, 80, 30), "Generate", font=font12)
gen_button.add_onrelease(regen)
buttons.add(gen_button)
#
cop_button = Button((210, 0, 80, 30), "Copy", font=font12)
cop_button.add_onrelease(copy_params)
buttons.add(cop_button)
#
paste_button = Button((300, 0, 80, 30), "Paste", font=font12)
paste_button.add_onrelease(paste_params)
buttons.add(paste_button)
#
cop_ore_button = Button((210, 400, 80, 30), "Copy", font=font12)
cop_ore_button.add_onrelease(copy_ore)
buttons.add(cop_ore_button)
#
paste_ore_button = Button((300, 400, 80, 30), "Paste", font=font12)
paste_ore_button.add_onrelease(paste_ore)
buttons.add(paste_ore_button)

land_oct1 = OpenSimplex(seed=rand(-99999999, 99999999))
land_oct2 = OpenSimplex(seed=rand(-99999999, 99999999))
land_oct3 = OpenSimplex(seed=rand(-99999999, 99999999))
ore_oct1 = OpenSimplex(seed=rand(-99999999, 99999999))
ore_oct2 = OpenSimplex(seed=rand(-99999999, 99999999))
def generate(f1, a1, f2, a2, f3, a3):
    for x in range(w):
        for y in range(h):
            noise = 0
            noise += land_oct1.noise2(x * f1, y * f1) * a1
            if radiobutton1.get_selected():
                noise += land_oct2.noise2(x * f2, y * f2) * a2
            if radiobutton2.get_selected():
                noise += land_oct3.noise2(x * f3, y * f3) * a3
            #
            if noise < slider7.get_value() - 1:#water
                field[x][y] = 2
            elif noise < slider8.get_value() - 1:#sand water
                field[x][y] = 4
            elif noise < slider9.get_value() - 1:#sand
                field[x][y] = 3
            elif noise < slider10.get_value() - 1:#grass
                field[x][y] = 0
            else:#stone
                field[x][y] = 1
            #
            ore_noise1 = ore_oct1.noise2(x * slider11.get_value(), y * slider11.get_value()) * slider12.get_value()
            ore_noise2 = 0
            if radiobutton3.get_selected():
                ore_noise2 = ore_oct2.noise2(x * slider13.get_value(), y * slider13.get_value()) * slider14.get_value()
            #field[x][y] = 1
            if ore_noise2 > slider15.get_value() - 1 and ore_noise1 > slider16.get_value() - 1:
                if field[x][y] == 0 or field[x][y] == 3:
                    ore[x][y] = 1
                elif field[x][y] == 1:
                    field[x][y] = 5
            #
            if field[x][y] == 0:#grass
                pygame.draw.rect(img, (0, 167, 0), (x, y, 1, 1))
            elif field[x][y] == 1:#stone
                pygame.draw.rect(img, (105, 105, 105), (x, y, 1, 1))
            elif field[x][y] == 2:#water
                pygame.draw.rect(img, (0, 133, 254), (x, y, 1, 1))
            elif field[x][y] == 3:#sand
                pygame.draw.rect(img, (251, 222, 133), (x, y, 1, 1))
            elif field[x][y] == 4:#sand water
                pygame.draw.rect(img, (125, 177, 193), (x, y, 1, 1))
            elif field[x][y] == 5:#coal
                pygame.draw.rect(img, (14, 14, 14), (x, y, 1, 1))
            elif field[x][y] == 6:#iron
                pygame.draw.rect(img, (170, 142, 117), (x, y, 1, 1))
            elif field[x][y] == 7:#copper
                pygame.draw.rect(img, (213, 90, 29), (x, y, 1, 1))
            #
            if (x + y) % 2 == 0:
                if ore[x][y] == 1:
                    pygame.draw.rect(img, (14, 14, 14), (x, y, 1, 1))
                elif ore[x][y] == 2:
                    pygame.draw.rect(img, (204, 170, 139), (x, y, 1, 1))
                elif ore[x][y] == 3:
                    pygame.draw.rect(img, (213, 90, 29), (x, y, 1, 1))

while keep_going:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            keep_going = 0
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                keep_going = 0
    #
    screen.fill((255, 255, 255))
    pygame.draw.rect(screen, (128, 128, 128), (0, 0, 400, 1080))
    buttons.update(screen, events)
    #
    screen.blit(pygame.transform.scale(img, (w * 4, h * 4)), (1160 - w * 2, 540 - w * 2))
    #
    screen.blit(font16.render("fps: " + str(round(timer.get_fps(), 2)), True, (255, 0, 0)), (400, 0))
    pygame.display.update()
    timer.tick(60)#0.162
pygame.quit()
#0.032 1.0 1 0.097 0.503 1 0.509 0.065 0.672 0.845 1.067 1.404 - big seas
#coal
#0.039 0.426 1 0.382 0.792 1.28 1.162
#iron
#0.045 0.51 1 0.163 0.447 1.131 1.192
#copper
#0.02 0.752 1 1.0 0.768 1.155 1.298 

#0.066 1 1 0.159 0.428 1 0.509 0.065 0.739 0.907 1.135 1.404 - small seas