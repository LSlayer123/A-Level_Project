# Importing libraries
import pygame
from pygame.locals import *
import sys
import random

# Initialising Pygame and the mixer
pygame.init()
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.music.load('Music.wav')
pygame.mixer.music.play(-1, 0.0)

# Creating the screen and setting the dimensions
world = pygame.display.set_mode([1280, 720])
frame = pygame.Surface([1280, 720])
pygame.display.set_caption("Game")
clock = pygame.time.Clock()

# Loading Images and converting them
titleScreen = pygame.image.load('Images/Title Screen.png').convert()
mainScreen = pygame.transform.scale(pygame.image.load('Images/UI.png').convert(), (1280, 720))
Blue = pygame.image.load('Images/Blue.png').convert()
Green = pygame.image.load('Images/Green.png').convert()
Orange = pygame.image.load('Images/Orange.png').convert()
Red = pygame.image.load('Images/Red.png').convert()
Yellow = pygame.image.load('Images/Yellow.png').convert()

# Defining variables for the mouse and clicks and base game state
mouse = pygame.mouse.get_pos()
click = pygame.mouse.get_pressed(num_buttons=5)
gameState = 0
resolution = 1
smallFont = pygame.font.SysFont('Arial', 23)
largeFont = pygame.font.SysFont('Arial', 36)
playerLocation = [-1, -1]


# Creating the main class for entities in the game
class Entity:

    # Initialising the Class and setting each instance's attributes
    def __init__(self, HPMax, MPMax, Strength, Magic, Defence, Resistance, Speed):
        self.HPMax, self.HP = HPMax
        self.MPMax, self.MP = MPMax
        self.Strength = Strength
        self.Magic = Magic
        self.Defence = Defence
        self.Resistance = Resistance
        self.Speed = Speed

    # Attack function [WIP]
    def Attack(self):
        pass


class Player(Entity):
    def __init__(self, HPMax, MPMax, Strength, Magic, Defence, Resistance, Speed):
        super().__init__(HPMax, MPMax, Strength, Magic, Defence, Resistance, Speed)


# Function for creating buttons
def button(start_x, start_y, width, height, function, text):
    if ((start_x / 1280) * world.get_width()) + ((width / 1280) * world.get_width()) > mouse[0] > \
            ((start_x / 1280) * world.get_width()) and (start_y / 720) * world.get_height() \
            + (height / 720) * world.get_height() > mouse[1] > (start_y / 720) * world.get_height():
        pygame.mouse.set_cursor(*pygame.cursors.diamond)
        pygame.draw.rect(frame, (150, 255, 0), (start_x, start_y, width, height))

        if click[0]:
            event = pygame.event.wait()
            if event.type == pygame.MOUSEBUTTONUP:
                pygame.mouse.set_cursor(*pygame.cursors.arrow)
                function()

    else:
        pygame.draw.rect(frame, (0, 255, 0), (start_x, start_y, width, height))
    title = smallFont.render(text, True, (0, 0, 255))
    frame.blit(title, (start_x, (start_y + (height / 2))))


# Function for changing the resolution of the screen
def change_Resolution():
    global world, mouse, smallFont, largeFont, resolution

    if resolution < 2:
        resolution += 1
    else:
        resolution = 0

    if resolution == 0:
        world = pygame.display.set_mode([720, 576])
        smallFont = pygame.font.SysFont('Arial', 18)
        largeFont = pygame.font.SysFont('Arial', 25)
    elif resolution == 1:
        world = pygame.display.set_mode([1280, 720])
        smallFont = pygame.font.SysFont('Arial', 23)
        largeFont = pygame.font.SysFont('Arial', 36)
    else:
        world = pygame.display.set_mode([1920, 1080])
        smallFont = pygame.font.SysFont('Arial', 28)
        largeFont = pygame.font.SysFont('Arial', 47)


# Function for setting the background for the current game state
def set_Background():
    global titleScreen, mainScreen
    bg = world.get_rect()

    if gameState == 0:
        frame.blit(titleScreen, bg)
    elif gameState == 1:
        frame.blit(mainScreen, bg)


# Function for redrawing the assets to the displayed surface at the correct resolution
def redraw_World():
    world.fill((0, 0, 0))
    frameCopy = pygame.transform.scale(frame, (world.get_width(), world.get_height()))
    world.blit(frameCopy, frameCopy.get_rect())


# Function for generating the layout of the floors in the game
def generate_Floor():
    layout = [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]
    for i in range(len(layout)):
        for j in range(len(layout[i])):
            layout[i][j] = random.randint(2, 4)
    return layout


# Function for rendering the map of the current floor on screen
def render_Map(rooms):
    global playerLocation

    pygame.draw.rect(frame, [204, 153, 255], [17.5, 62, 40, 40])
    pygame.draw.rect(frame, [204, 153, 255], [318.5, 62, 40, 40])

    for i in range(len(rooms)):
        for j in range(len(rooms[i])):
            if ((17.0 + (i * 45)) / 720) * world.get_height() + (40.0 / 720) * world.get_height() > mouse[1] > \
                    ((17.0 + (i * 45)) / 720) * world.get_height() and (((60.5 + (j * 43)) / 1280) * world.get_width())\
                    + ((40.0 / 1280) * world.get_width()) > mouse[0] > (((60.5 + (j * 43)) / 1280) * world.get_width()):
                if rooms[i][j] == 2:
                    pygame.draw.rect(frame, [255, 165, 0], [60.5 + (j * 43), 17 + (i * 45), 40, 40], True)
                elif rooms[i][j] == 3:
                    pygame.draw.rect(frame, [255, 0, 0], [60.5 + (j * 43), 17 + (i * 45), 40, 40], True)
                elif rooms[i][j] == 4:
                    pygame.draw.rect(frame, [0, 0, 255], [60.5 + (j * 43), 17 + (i * 45), 40, 40], True)

                if click[0] and playerLocation[1] == j-1 and gameState == 1:
                    playerLocation = [i, j]
                    print(playerLocation)
            else:
                if rooms[i][j] == 2:
                    pygame.draw.rect(frame, [255, 165, 0], [60.5 + (j * 43), 17 + (i * 45), 40, 40])
                elif rooms[i][j] == 3:
                    pygame.draw.rect(frame, [255, 0, 0], [60.5 + (j * 43), 17 + (i * 45), 40, 40])
                elif rooms[i][j] == 4:
                    pygame.draw.rect(frame, [0, 0, 255], [60.5 + (j * 43), 17 + (i * 45), 40, 40])

    if playerLocation != [-1, -1]:
        pygame.draw.rect(frame, [0, 255, 0], [60.5 + (playerLocation[1] * 43), 17 + (playerLocation[0] * 45), 40, 40])


# Opening Screen for the Game
def main_Menu():
    global mouse, click, world
    while True:

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed(num_buttons=5)

        set_Background()

        pygame.mouse.set_cursor(*pygame.cursors.arrow)

        button(100.0, 200.0, 100.0, 50.0, main_Game, 'Start')
        button(100.0, 300.0, 100.0, 50.0, load_Game, 'Continue?')
        button(100.0, 400.0, 100.0, 50.0, change_Resolution, 'Toggle Resolution')

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == K_f:
                    pygame.display.toggle_fullscreen()

        redraw_World()

        pygame.display.update()
        clock.tick(60)


# Main game state
def main_Game():
    global gameState, world, mouse, click, playerLocation
    gameState = 1
    floor = generate_Floor()
    print(floor)
    playerLocation = [-1, -1]
    while gameState == 1:

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed(num_buttons=5)

        set_Background()
        render_Map(floor)

        pygame.mouse.set_cursor(*pygame.cursors.arrow)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == K_f:
                    pygame.display.toggle_fullscreen()

        redraw_World()
        pygame.display.update()
        clock.tick(60)


# Save Game
def save_Game():
    global gameState
    gameState = 3
    pass


# Load Game
def load_Game():
    global gameState
    gameState = 4
    pass


# Test Function
def test():
    print("Hi")


main_Menu()
