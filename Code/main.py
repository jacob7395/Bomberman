# -----------------------------------------------
# Load functions and calsses form remote locations
import random
import os
import time
import threading
from multiprocessing.pool import ThreadPool
from multiprocessing import Process, Queue
import time
import pygame
from pygame import draw, display, rect, mouse, joystick
from pygame.sprite import groupcollide
# setup to improt files fomr MyLib
path = os.path.realpath(__file__)
for i in range(0, 1):
    path = os.path.dirname(path)
# File path for custom liberys
path_JacobLib = path + "/JacobLib"
path_Sprite = path + "/Sprite"
path_Josh = path + "/Josh"
controller_Sprite = path + "/controller"
path_Assets = os.path.dirname(path) + "/Assets/"
path_Map_Gen = os.path.dirname(path) + "/Code" + "/Map_Gen"

import sys
sys.path.insert(0, path_JacobLib)
# import from MyLib
from Error_Report import Report_Error, Make_Error_File
from Class_Factory import Class_Factory

sys.path.insert(0, controller_Sprite)
# import from controller
from controller import controller_Object

sys.path.insert(0, path_Sprite)
# import bomb sprite
from Bomb import Sprite_Bomb
# import bomberman sprite
from Bomberman import Sprite_Bomberman

sys.path.insert(0, path_Josh)
import AIBot
import StartMenu
import GameEnd


sys.path.insert(0, path_Map_Gen)
# import test sprite
from Map_Maker import Map_Load
# -----------------------------------------------
# Reset error file
Make_Error_File()
# -----------------------------------------------
# section for Pygame initalization
# Define some colors
BLACK = (0,   0,   0)
WHITE = (255, 255, 255)
GREEN = (0, 255,   0)
RED = (255,   0,   0)
# default pygame init functions
pygame.init()
# Set the width and height of the screen [width, height]
screen_Size = (714, 374)
# screen_Size = (1428, 748)
screen = display.set_mode(screen_Size)
scree_Fullscreen = True
# Define spawn Area
spawn_Area = (-100, -50, 0, screen_Size[1])
# Set game window
pygame.display.set_caption("Bomberman")
# -----------------------------------------------
# Sprite populations and generation
# This is a list of 'sprites.' Each pepe in the program is
# added to this list. The list is managed by a class called 'Group.'
# make backgroud using map reader Function
# background runs in a threadList
sprite_Lists = Map_Load(screen_Size, 21)
background_List = sprite_Lists[0]
bDrwan = False
bush_List = sprite_Lists[1]
bushes_to_Destroyed = []
wall_List = sprite_Lists[2]
sprite_Scale = sprite_Lists[3]
Map_O = sprite_Lists[4]


# bot = AIBot.AIBot(int(len(Map_O.map_Grid[0])), int(len(Map_O.map_Grid) - 1))
# bot.setList(Map_O.map_Grid)


# for bush in Map_O.bush_List:
# print(bush)
# bomb group and factry init
bomb_List = pygame.sprite.Group()
explotion_List = pygame.sprite.Group()
# make bomber man
# get number of plugged in controllers
number_Of_Players = 4
man_List = pygame.sprite.Group()
man_Factory = Class_Factory("Man", Sprite_Bomberman)
man_Count = 0
for tile in background_List:
    if(tile.class_Name == "Spawn" and man_Count < number_Of_Players):
        man = man_Factory.New(tile.Position(), False, sprite_Scale, man_Count)
        man.AI = True
        man_List.add(man)
        man_Count += 1

bot_Count = man_Count
# controller initalization
controllers = []
for count in range(joystick.get_count()):
    for bomberman in man_List:
        if(bomberman.ID - 1 == count):
            bomberman.AI = True
            bot_Count -= 1
            controllers.append(controller_Object(bomberman, count))

botList = list()
for x in range(bot_Count + 1):
    botList.append(AIBot.AIBot(int(len(Map_O.map_Grid[0])), int(len(Map_O.map_Grid) - 1)))
    botList[x].setList(Map_O.map_Grid)

done = False
# used to manage how fast the screen updates
clock = pygame.time.Clock()
oldrects = pygame.Rect(10, 10, 10, 10)

for man in man_List:
    # get a list of all men withouth me in it
    man_List_Not_Me = []
    for not_Me in man_List:
        if(not_Me.ID != man.ID):
            man_List_Not_Me.append(not_Me)
    target = random.choice(man_List_Not_Me)
    # gets the tiles posion on the map object for the mans location
    pos = (Map_O.pos_To_Location([man.get_Sprite_Center()]))[0]
    tagert_Pos = (Map_O.pos_To_Location([target.get_Sprite_Center()]))[0]
    # get path with dicstra
    path = botList[man.ID].pathFinding.getPath(pos, tagert_Pos, Map_O.map_Grid)
    print("Target Pos = {},Current Pos = {},Target path = {}".format(tagert_Pos, pos, path))
    botList[man.ID].getPath(pos, Map_O.map_Grid)

startMenu = StartMenu.StartMenu(path_Assets + "background.JPG", screen_Size)
endScreen = GameEnd.GameEnd(path_Assets + "background.JPG", screen_Size)

pygame.mixer.music.load(path_Assets + "StartScreen.wav")
pygame.mixer.music.play(-1, 0.0)


start = False
while start:
    screen.fill(BLACK)
    startMenu.controllers(pygame.joystick.get_count())
    startMenu.update(screen)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            start = False
            break
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if startMenu.state == 0:
                keyPress = startMenu.keyPress(pos)
                if keyPress == "playButton":
                    startMenu.state = 1
                elif keyPress == "exitButton":
                    pygame.quit()
                    # Need to make this exit the program properly
            elif startMenu.state == 1:
                keyPress = startMenu.keyPress(pos)
                if keyPress == "confirmButton":
                    start = False
                elif keyPress == "backButton":
                    startMenu.state = 0
    pygame.display.flip()


# pygame.mixer.music.stop()
# pygame.mixer.music.load(path_Assets + "Battle.mp3")
# pygame.mixer.music.play(-1,0.0)


gameOver = False
while gameOver == True:
    screen.fill(BLACK)
    endScreen.update(screen)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            start = False
            break
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            keyPress = endScreen.keyPress(pos)
            if keyPress == "mainMenuButton":
                print("Go back to the main menu")
    pygame.display.flip()


# -------- Main Program Loop -----------
while not done:
    # --- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F1:
                if scree_Fullscreen == True:
                    screen = display.set_mode(screen_Size)
                    scree_Fullscreen = False
                else:
                    screen = display.set_mode(screen_Size, pygame.FULLSCREEN)
                    scree_Fullscreen = True
            elif event.key == pygame.K_F2:
                done = True
    # --- Update controller logic loop
    for controller in controllers:
        controller.EventManager()

    # --- Game logic should go hered
    for man in man_List:
        if man.AI == True:
         #   pos = man.Position()
         #   botList[man.ID].getPath([int(pos[0] / 34), int(pos[1] / 34)], Map_O.map_Grid)
            # gets the tiles posion on the map object for the mans location
            pos = (Map_O.pos_To_Location([man.get_Sprite_Center()]))[0]
            # get the sprites coliton coreners
            cornors = Map_O.pos_To_Location(man.get_Collision_Coners())
            # check the postion is the same as all the conrets
            equle = True
            for p in cornors:
                if(pos != p):
                    equle = False
            # if the posiont matches all the corners update the ai's position
            if(equle == True):
                botList[man.ID].moving_Pos = pos

            direction = botList[man.ID].update(screen, Map_O, man)

            if direction != None:
                if direction == "BOOM":
                    man.spawn_Bomb(Map_O)
                    continue
                elif direction == "NewTarget":
                    pass
                    # pos = man.Position()
                    # botList[man.ID].getPath([int(pos[0] / 34), int(pos[1] / 34)], Map_O.map_Grid)
                else:
                    man.changeDirection(direction)
                    if(man.running == False):
                        man.begin_running()
            else:
                man.stop_running()

        bomb_List.add(man.update(Map_O))
        # check if men are in explotion
        for explotion in explotion_List:
            # if a man is in any explotion remove them from existance
            if(explotion.position_In_Collition(man.get_Sprite_Center()) == True):
                man_List.remove(man)

    for bomb in bomb_List:
        if(bomb.update(Map_O) == True):
            tiles = Map_O.tile_At(bomb.get_Collision_Coners())
            for tile in tiles:
                tile["Bomb"] = False
            for explotion in bomb.explotion_List:
                explotion_List.remove(explotion)
                bomb.explotion_List.remove(explotion)
            bomb.owner.bomb_List.remove(bomb)
            bomb_List.remove(bomb)
        if(len(bomb.explotion_List) > 0):
            explotion_List.add(bomb.explotion_List)
    # find all bushes that need to be desroyed
    for explotion in explotion_List:
        for bush in explotion.bushes_to_Destroyed:
            bushes_to_Destroyed.append(bush)
            explotion.bushes_to_Destroyed = []
    # if there is a bush to destroy find it then remove it form the game
    if(len(bushes_to_Destroyed) > 0):
        for bush in bush_List:
            for bush_Destroy in bushes_to_Destroyed:
                if(bush.Position() == bush_Destroy):
                    bush_List.remove(bush)
    # --- Check win condition
    if(len(man_List) == 6):
        done = True

    # --- Screen-clearing code goes here
    # Here, we clear the screen to white. Don't put other drawing commandsd
    # above this, or they will be erased with this command.
    # If you want a background image, replace this clear with blit'ing the
    # background image.
    # --- Drawing code should go here

    background_List.draw(screen)
    wall_List.draw(screen)
    explotion_List.draw(screen)
    man_List.draw(screen)
    bomb_List.draw(screen)
    bush_List.draw(screen)

    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
    # --- Limit to 60 frames per second
    clock.tick(60)
    # pygame.time.delay(100)
# Close the window and quit.
pygame.quit()
