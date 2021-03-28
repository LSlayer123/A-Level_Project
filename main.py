# Importing libraries
import pygame
from pygame.locals import *
import sys
import random
import math

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
mainScreen = pygame.image.load('Images/UI.png').convert()
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
playerLocation = []
floor = [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]
finalAttack = 0
enemyFinalAttack = 0
roomClear = False
floorNumber = 0
startTime = 0
endTime = 0
updateText = smallFont.render("", True, (0, 0, 0))


# --------------------------------CLASSES------------------------------------------------------------------------------#
class Entity:

    # Initialising the Class and setting each instance's attributes
    def __init__(self, HPMax, MPMax, Strength, Magic, Defence, Resistance, Name):
        self.HPMax = self.HP = HPMax
        self.MPMax = self.MP = MPMax
        self.Strength = Strength
        self.Magic = Magic
        self.Defence = Defence
        self.Resistance = Resistance
        self.Name = Name

    def Attack(self):
        global enemyFinalAttack
        enemyFinalAttack = self.Strength

    def Defend(self):
        self.Defence += 5
        pass


class Player(Entity):
    def __init__(self, HPMax, MPMax, Strength, Magic, Defence, Resistance, Name):
        super().__init__(HPMax, MPMax, Strength, Magic, Defence, Resistance, Name)
        self.Class = ""
        self.statPoints = 5

    def Attack(self):
        global finalAttack
        finalAttack = self.Strength

    def Defend(self):
        global finalAttack
        finalAttack = -1
        self.Defence += 5

    def classChange(self, selection):

        if selection == "warrior":
            self.Strength += 10
            self.Magic += 1
            self.Defence += 5
            self.Resistance += 3
            self.Class = "Warrior"

        elif selection == "mage":
            self.Strength += 1
            self.Magic += 10
            self.Defence += 3
            self.Resistance += 5
            self.Class = "Mage"

        elif selection == "rogue":
            self.Strength += 6
            self.Magic += 5
            self.Defence += 5
            self.Resistance += 4
            self.Class = "Rogue"

    def strengthUp(self):
        self.Strength += 1
        self.statPoints -= 1

    def magicUp(self):
        self.Magic += 1
        self.statPoints -= 1

    def defenceUp(self):
        self.Defence += 1
        self.statPoints -= 1

    def resistanceUp(self):
        self.Resistance += 1
        self.statPoints -= 1

    def Ability1(self):
        pass

    def Ability2(self):
        pass

    def Ability3(self):
        pass

    def Ability4(self):
        pass


# ---------------------------------ADMIN FUNCTIONS---------------------------------------------------------------------#
# Function for creating buttons
def button(start_x, start_y, width, height, function, text, parameter=None):
    if ((start_x / 1280) * world.get_width()) + ((width / 1280) * world.get_width()) > mouse[0] > \
            ((start_x / 1280) * world.get_width()) and (start_y / 720) * world.get_height() \
            + (height / 720) * world.get_height() > mouse[1] > (start_y / 720) * world.get_height():
        pygame.mouse.set_cursor(*pygame.cursors.diamond)
        pygame.draw.rect(frame, (150, 255, 0), (start_x, start_y, width, height))

        if click[0]:
            event = pygame.event.wait()
            if event.type == pygame.MOUSEBUTTONUP and function is not None:
                pygame.mouse.set_cursor(*pygame.cursors.arrow)
                if parameter is not None:
                    function(parameter)
                else:
                    function()

    else:
        pygame.draw.rect(frame, (0, 255, 0), (start_x, start_y, width, height))
    title = smallFont.render(text, True, (0, 0, 0))
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
    elif gameState == 1 or gameState == 2:
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
            layout[i][j] = random.choice([2, 2, 2, 2, 3, 4])
    return layout


# Function for rendering the map of the current floor on screen
def render_Map(rooms):
    global playerLocation, roomClear

    pygame.draw.rect(frame, [204, 153, 255], [17.5, 62, 40, 40])
    pygame.draw.rect(frame, [204, 153, 255], [318.5, 62, 40, 40])

    for i in range(len(rooms)):
        for j in range(len(rooms[i])):
            if ((17.0 + (i * 45)) / 720) * world.get_height() + (40.0 / 720) * world.get_height() > mouse[1] > \
                    ((17.0 + (i * 45)) / 720) * world.get_height() and (((60.5 + (j * 43)) / 1280) * world.get_width()) \
                    + ((40.0 / 1280) * world.get_width()) > mouse[0] > (((60.5 + (j * 43)) / 1280) * world.get_width()) \
                    and gameState == 1:
                if rooms[i][j] == 2:
                    pygame.draw.rect(frame, [255, 165, 0], [60.5 + (j * 43), 17 + (i * 45), 40, 40], True)
                elif rooms[i][j] == 3:
                    pygame.draw.rect(frame, [255, 0, 0], [60.5 + (j * 43), 17 + (i * 45), 40, 40], True)
                elif rooms[i][j] == 4:
                    pygame.draw.rect(frame, [0, 0, 255], [60.5 + (j * 43), 17 + (i * 45), 40, 40], True)

                if click[0] and playerLocation[1] == j - 1 and gameState == 1:
                    playerLocation = [i, j]
                    roomClear = False
            else:
                if rooms[i][j] == 2:
                    pygame.draw.rect(frame, [255, 165, 0], [60.5 + (j * 43), 17 + (i * 45), 40, 40])
                elif rooms[i][j] == 3:
                    pygame.draw.rect(frame, [255, 0, 0], [60.5 + (j * 43), 17 + (i * 45), 40, 40])
                elif rooms[i][j] == 4:
                    pygame.draw.rect(frame, [0, 0, 255], [60.5 + (j * 43), 17 + (i * 45), 40, 40])

    if playerLocation != [-1, -1]:
        pygame.draw.rect(frame, [0, 255, 0], [60.5 + (playerLocation[1] * 43), 17 + (playerLocation[0] * 45), 40, 40])


# Character Creation Function
def characterCreation():
    global gameState, world, mouse, click, floor, updateText
    characterCreated = False
    User = Player(150, 50, 0, 0, 0, 0, "Player")

    while not characterCreated:

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed(num_buttons=5)

        set_Background()

        pygame.mouse.set_cursor(*pygame.cursors.arrow)

        currentFloorNumber = largeFont.render(str(floorNumber), True, (0, 0, 0))
        frame.blit(currentFloorNumber, (557.0, 75.0))

        if User.Class == "":
            button(30, 170, 80, 50, User.classChange, "Warrior", "warrior")
            button(130, 170, 80, 50, User.classChange, "Mage", "mage")
            button(230, 170, 80, 50, User.classChange, "Rogue", "rogue")
        else:
            button(30, 170, 80, 50, None, "Warrior")
            button(130, 170, 80, 50, None, "Mage")
            button(230, 170, 80, 50, None, "Rogue")

        statPointText = smallFont.render("Stat Points remaining:" + str(User.statPoints), True, (0, 0, 0))
        frame.blit(statPointText, (30, 240))

        strengthText = smallFont.render("Strength:" + str(User.Strength), True, (0, 0, 0))
        frame.blit(strengthText, (30, 270))
        magicText = smallFont.render("Magic:" + str(User.Magic), True, (0, 0, 0))
        frame.blit(magicText, (130, 270))
        defenceText = smallFont.render("Defence:" + str(User.Defence), True, (0, 0, 0))
        frame.blit(defenceText, (230, 270))
        resistanceText = smallFont.render("Resistance:" + str(User.Resistance), True, (0, 0, 0))
        frame.blit(resistanceText, (330, 270))

        if User.statPoints != 0:
            button(30, 300, 80, 50, User.strengthUp, "+")
            button(130, 300, 80, 50, User.magicUp, "+")
            button(230, 300, 80, 50, User.defenceUp, "+")
            button(330, 300, 80, 50, User.resistanceUp, "+")
        else:
            button(30, 300, 80, 50, None, "+")
            button(130, 300, 80, 50, None, "+")
            button(230, 300, 80, 50, None, "+")
            button(330, 300, 80, 50, None, "+")

        updateText = smallFont.render("Your class is " + User.Class, True, (0, 0, 0))
        frame.blit(updateText, (17.5, 545.0))

        if User.Class != "" and User.statPoints == 0:
            characterCreated = True

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

    return User


# Enemy Creation Function
def enemyCreation(number=None):
    global floorNumber

    if number == 1:
        enemy = Entity(100 + (floorNumber * 5), 50, 10 + floorNumber, 0, 5 + floorNumber, 0, "Troll")
    else:
        enemy = Entity(50 + (floorNumber * 5), 50, 7 + floorNumber, 2, 2 + (floorNumber / 5), 2 + (floorNumber / 5), "Golbin")

    return enemy


# -------------------------------MAIN GAME FUNCTIONS-------------------------------------------------------------------#
# Opening Screen for the Game
def main_Menu():
    global mouse, click, world, startTime, endTime
    while True:

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed(num_buttons=5)

        set_Background()

        pygame.mouse.set_cursor(*pygame.cursors.arrow)

        button(100.0, 200.0, 100.0, 50.0, main_Game, 'Start')
        button(100.0, 300.0, 100.0, 50.0, load_Game, 'Continue?')
        button(100.0, 400.0, 150.0, 50.0, change_Resolution, 'Toggle Resolution')

        totalTime = endTime - startTime
        seconds = int((totalTime / 1000) % 60)
        minutes = int((totalTime / (1000 * 60)) % 60)
        hours = int((totalTime / (1000 * 60 * 60)) % 60)
        Time = str(hours) + ":" + str(minutes) + ":" + str(seconds)

        previousTime = smallFont.render("You're previous attempt was " + Time, True, (0, 0, 0))
        frame.blit(previousTime, (100.0, 500.0))

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
    global gameState, world, mouse, click, playerLocation, floor, roomClear, floorNumber, startTime, updateText
    gameState = 1

    playerCharacter = characterCreation()

    floor = generate_Floor()
    playerLocation = [-1, -1]

    startTime = pygame.time.get_ticks()

    while gameState == 1:

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed(num_buttons=5)

        set_Background()
        render_Map(floor)

        pygame.mouse.set_cursor(*pygame.cursors.arrow)

        playerHealth = smallFont.render(str(playerCharacter.HP), True, (0, 0, 0))
        frame.blit(playerHealth, (76.0, 588.0))
        playerMaxHealth = smallFont.render(str(playerCharacter.HPMax), True, (0, 0, 0))
        frame.blit(playerMaxHealth, (197.0, 588.0))
        playerMana = smallFont.render(str(playerCharacter.MP), True, (0, 0, 0))
        frame.blit(playerMana, (76.0, 629.0))
        playerMaxMana = smallFont.render(str(playerCharacter.MPMax), True, (0, 0, 0))
        frame.blit(playerMaxMana, (197.0, 629.0))

        playerStrength = smallFont.render("Strength: " + str(playerCharacter.Strength), True, (0, 0, 0))
        frame.blit(playerStrength, (980.0, 275.0))
        playerMagic = smallFont.render("Magic: " + str(playerCharacter.Magic), True, (0, 0, 0))
        frame.blit(playerMagic, (980.0, 300.0))
        playerDefence = smallFont.render("Defence: " + str(playerCharacter.Defence), True, (0, 0, 0))
        frame.blit(playerDefence, (980.0, 325.0))
        playerResistance = smallFont.render("Resistance: " + str(playerCharacter.Resistance), True, (0, 0, 0))
        frame.blit(playerResistance, (980.0, 350.0))

        currentFloorNumber = largeFont.render(str(floorNumber), True, (0, 0, 0))
        frame.blit(currentFloorNumber, (557.0, 75.0))

        frame.blit(updateText, (17.5, 545.0))

        if playerCharacter.statPoints != 0:
            button(1095, 275.0, 25, 20, playerCharacter.strengthUp, "")
            button(1095, 300.0, 25, 20, playerCharacter.magicUp, "")
            button(1095, 325.0, 25, 20, playerCharacter.defenceUp, "")
            button(1095, 350.0, 25, 20, playerCharacter.resistanceUp, "")

        if not roomClear:
            if floor[playerLocation[0]][playerLocation[1]] == 2 and playerLocation != [-1, -1]:
                combat(playerCharacter, enemyCreation())
            elif floor[playerLocation[0]][playerLocation[1]] == 3 and playerLocation != [-1, -1]:
                combat(playerCharacter, enemyCreation(1))
            elif floor[playerLocation[0]][playerLocation[1]] == 4 and playerLocation != [-1, -1]:
                Effect = random.randint(0, 4)
                if Effect == 0:
                    playerCharacter.HP += 50
                    if playerCharacter.HP > playerCharacter.HPMax:
                        playerCharacter.HP = playerCharacter.HPMax
                    roomClear = True
                    updateText = smallFont.render("You found a holy spring that heals 50HP.", True, (0, 0, 0))
                elif Effect == 1:
                    playerCharacter.Strength += 2
                    roomClear = True
                    updateText = smallFont.render("You found a demon fruit - raising your strength.", True, (0, 0, 0))
                elif Effect == 2:
                    playerCharacter.Defence += 2
                    roomClear = True
                    updateText = smallFont.render("You found a shield fruit - raising your defence.", True, (0, 0, 0))
                elif Effect == 3:
                    combat(playerCharacter, enemyCreation())
                elif Effect == 4:
                    combat(playerCharacter, enemyCreation(1))
        elif playerLocation[1] == 5:
            floorNumber += 1
            playerCharacter.statPoints += 1
            floor = generate_Floor()
            playerLocation = [-1, -1]

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


# Function for the combat encounters in the game
def combat(player, enemy):
    global gameState, world, mouse, click, playerLocation, floor, finalAttack, enemyFinalAttack, roomClear, floorNumber \
        , endTime, updateText
    basePlayerDefence = player.Defence
    baseEnemyDefence = enemy.Defence
    enemyDamageText = smallFont.render("", True, (0, 0, 0))
    playerDamageText = smallFont.render("", True, (0, 0, 0))
    gameState = 2

    updateText = smallFont.render("You encountered " + enemy.Name, True, (0, 0, 0))

    while enemy.HP > 0 and player.HP > 0:
        finalAttack = 0
        enemyFinalAttack = 0

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

        playerHealth = smallFont.render(str(player.HP), True, (0, 0, 0))
        frame.blit(playerHealth, (76.0, 588.0))
        playerMaxHealth = smallFont.render(str(player.HPMax), True, (0, 0, 0))
        frame.blit(playerMaxHealth, (197.0, 588.0))
        playerMana = smallFont.render(str(player.MP), True, (0, 0, 0))
        frame.blit(playerMana, (76.0, 629.0))
        playerMaxMana = smallFont.render(str(player.MPMax), True, (0, 0, 0))
        frame.blit(playerMaxMana, (197.0, 629.0))

        playerStrength = smallFont.render("Strength: " + str(player.Strength), True, (0, 0, 0))
        frame.blit(playerStrength, (980.0, 275.0))
        playerMagic = smallFont.render("Magic: " + str(player.Magic), True, (0, 0, 0))
        frame.blit(playerMagic, (980.0, 300.0))
        playerDefence = smallFont.render("Defence: " + str(player.Defence), True, (0, 0, 0))
        frame.blit(playerDefence, (980.0, 325.0))
        playerResistance = smallFont.render("Resistance: " + str(player.Resistance), True, (0, 0, 0))
        frame.blit(playerResistance, (980.0, 350.0))

        enemyName = smallFont.render(str(enemy.Name), True, (0, 0, 0))
        frame.blit(enemyName, (371.0, 588.0))
        enemyHealth = smallFont.render(str(enemy.HP), True, (0, 0, 0))
        frame.blit(enemyHealth, (371.0, 629.0))
        enemyMaxHealth = smallFont.render(str(enemy.HPMax), True, (0, 0, 0))
        frame.blit(enemyMaxHealth, (492.0, 629.0))

        currentFloorNumber = largeFont.render(str(floorNumber), True, (0, 0, 0))
        frame.blit(currentFloorNumber, (557.0, 75.0))

        frame.blit(updateText, (17.5, 545.0))

        frame.blit(enemyDamageText, (17.5, 160.0))
        frame.blit(playerDamageText, (17.5, 180.0))

        button(740, 33, 140, 55, player.Attack, "Attack")
        button(740, 92, 140, 55, player.Ability1, "Ability1")
        button(740, 151, 140, 55, player.Ability2, "Ability2")
        button(884, 33, 140, 55, player.Ability3, "Ability3")
        button(884, 92, 140, 55, player.Ability4, "Ability4")
        button(884, 151, 140, 55, player.Defend, "Defend")

        if finalAttack != 0:

            finalAttack -= enemy.Defence
            if finalAttack < 0:
                finalAttack = 0
            enemy.HP -= math.floor(finalAttack)
            enemyDamageText = smallFont.render("You did " + str(finalAttack) + " damage to " + enemy.Name, True,
                                               (0, 0, 0))
            if enemy.HP > 0:
                enemy.Attack()
                enemyFinalAttack -= player.Defence
                if enemyFinalAttack < 0:
                    enemyFinalAttack = 0
                player.HP -= math.floor(enemyFinalAttack)
                playerDamageText = smallFont.render("You took " + str(enemyFinalAttack) + " damage from " + enemy.Name,
                                                    True, (0, 0, 0))

        player.Defence = basePlayerDefence
        enemy.Defence = baseEnemyDefence

        redraw_World()
        pygame.display.update()
        clock.tick(60)

    if enemy.HP <= 0:
        gameState = 1
        roomClear = True
        updateText = smallFont.render("You beat " + enemy.Name, True, (0, 0, 0))
    else:
        gameState = 0
        endTime = pygame.time.get_ticks()


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


main_Menu()
