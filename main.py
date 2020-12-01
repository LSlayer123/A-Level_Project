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


# Opening Screen for the Game
def main_Menu():
    while True:

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        clock.tick(60)


# Main game state
def main_Game():
    pass


# Options Menu
def options():
    pass


main_Menu()
