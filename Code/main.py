# -----------------------------------------------
# Load functions and calsses form remote locations
import random
import os
import time
import threading
from multiprocessing.pool import ThreadPool
from multiprocessing import Process, Queue

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

sys.path.insert(0, path_Map_Gen)
# import test sprite
from Map_Maker import Map_Load


def sign(x):
    if (x <= 0):
        return 1
    else:
        return -1

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
# bomb group and factry init
bomb_List = pygame.sprite.Group()
explotion_List = pygame.sprite.Group()
# make bomber man
# get number of plugged in controllers
number_Of_Players = joystick.get_count()
man_List = pygame.sprite.Group()
man_Factory = Class_Factory("Man", Sprite_Bomberman)
man_Count = 0
for tile in background_List:
    if(tile.class_Name == "Spawn" and man_Count < number_Of_Players):
        man = man_Factory.New(tile.Position(), False, sprite_Scale, man_Count)
        man_List.add(man)
        man_Count += 1
# controller initalization
controllers = []
for count in range(joystick.get_count()):
    for bomberman in man_List:
        if(bomberman.ID - 1 == count):
            controllers.append(controller_Object(bomberman, count))

done = False
# used to manage how fast the screen updates
clock = pygame.time.Clock()
oldrects = pygame.Rect(10, 10, 10, 10)
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
        for man in man_List:
            done = True

    # --- Screen-clearing code goes here
    # Here, we clear the screen to white. Don't put other drawing commandsd
    # above this, or they will be erased with this command.
    # If you want a background image, replace this clear with blit'ing the
    # background image.
    # --- Drawing code should go here
    background_List.draw(screen)
    wall_List.draw(screen)
    bomb_List.draw(screen)
    bush_List.draw(screen)
    explotion_List.draw(screen)
    man_List.draw(screen)
    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
    # --- Limit to 60 frames per second
    clock.tick(60)

# Close the window and quit.
pygame.quit()
