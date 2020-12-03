# Importing libraries
import pygame
from pygame.locals import *
import sys

# Initialising Pygame
pygame.init()

# Creating the screen and setting the dimensions
world = pygame.display.set_mode([1080, 720])
pygame.display.set_caption("Game")
clock = pygame.time.Clock()


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


def button(start_x, start_y, width, height, function):
    if start_x + width > mouse[0] > start_x and start_y + height > mouse[1] > start_y:
        pygame.draw.rect(world, (50, 255, 50), (start_x, start_y, width, height))
    else:
        pygame.draw.rect(world, (255, 255, 255), (start_x, start_y, width, height))


def redraw_World():
    world.fill((0, 0, 0))


# Opening Screen for the Game
def main_Menu():
    global mouse, click
    while True:

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        redraw_World()

        button(300, 450, 50, 50, None)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        clock.tick(60)


# Main game state
def main_Game():
    pass


# Options Menu
def options():
    pass


main_Menu()
