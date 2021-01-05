# Importing libraries
import pygame
from pygame.locals import *
import sys

# Initialising Pygame and the mixer
pygame.init()
pygame.mixer.pre_init(44100, -16, 2, 512)

# Creating the screen and setting the dimensions
world = pygame.display.set_mode([1280, 720])
pygame.display.set_caption("Game")
clock = pygame.time.Clock()

monitor_dimensions = [pygame.display.Info().current_w, pygame.display.Info().current_h]

# Loading Images
titleScreen = pygame.image.load('Images/Title Screen.png')
mainScreen = pygame.image.load('Images/UI.png')
optionScreen = pygame.image.load('Images/OPTION.png')
titleScreen.convert()
mainScreen.convert()
optionScreen.convert()

# Defining variables for the mouse and clicks
mouse = pygame.mouse.get_pos()
click = pygame.mouse.get_pressed(num_buttons=5)
gameState = 0


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
def button(start_x, start_y, width, height, function):
    if start_x + width > mouse[0] > start_x and start_y + height > mouse[1] > start_y:
        pygame.mouse.set_cursor(*pygame.cursors.diamond)
        pygame.draw.rect(world, (150, 255, 0), (start_x, start_y, width, height))
        if click[0]:
            event = pygame.event.wait()
            if event.type == pygame.MOUSEBUTTONUP:
                function()
    else:
        pygame.draw.rect(world, (0, 255, 0), (start_x, start_y, width, height))


# Function for changing the resolution of the screen
def change_Resolution():
    global world, mouse
    if 200 <= mouse[1] <= 250:
        world = pygame.display.set_mode([640, 480])
    elif 300 <= mouse[1] <= 350:
        world = pygame.display.set_mode([1280, 720])
    else:
        world = pygame.display.set_mode([1920, 1080])


# Function for redrawing the graphics in the game
def redraw_World():
    global titleScreen, mainScreen, optionScreen
    world.fill((0, 0, 0))
    bg = world.get_rect()
    if gameState == 0:
        titleScreenCopy = pygame.transform.scale(titleScreen, (bg[2], bg[3]))
        world.blit(titleScreenCopy, bg)
    elif gameState == 1:
        mainScreenCopy = pygame.transform.scale(mainScreen, (bg[2], bg[3]))
        world.blit(mainScreenCopy, bg)
    elif gameState == 2:
        optionScreenCopy = pygame.transform.scale(optionScreen, (bg[2], bg[3]))
        world.blit(optionScreenCopy, bg)


# Opening Screen for the Game
def main_Menu():
    global mouse, click, world
    while True:

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed(num_buttons=5)

        redraw_World()
        pygame.mouse.set_cursor(*pygame.cursors.arrow)

        button(100, 200, 100, 50, main_Game)
        button(100, 300, 100, 50, load_Game)
        button(100, 400, 100, 50, options)

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

        pygame.display.update()
        clock.tick(60)


# Main game state
def main_Game():
    global gameState, world
    gameState = 1
    while gameState == 1:

        redraw_World()
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


# Options Menu
def options():
    global gameState, world, mouse, click
    gameState = 2
    while gameState == 2:

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed(num_buttons=5)

        redraw_World()
        pygame.mouse.set_cursor(*pygame.cursors.arrow)

        button(100, 200, 100, 50, change_Resolution)
        button(100, 300, 100, 50, change_Resolution)
        button(100, 400, 100, 50, change_Resolution)

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

        pygame.display.update()
        clock.tick(60)

    pass


# Test Function
def test():
    print("Hi")


main_Menu()
