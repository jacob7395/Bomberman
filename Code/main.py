# -----------------------------------------------
# Load functions and calsses form remote locations
import random
import os
import time
import threading
from multiprocessing.pool import ThreadPool
from multiprocessing import Process, Queue

import pygame
from pygame import draw, display, rect, mouse
from pygame.sprite import groupcollide
# setup to improt files fomr MyLib
path = os.path.realpath(__file__)
for i in range(0, 1):
    path = os.path.dirname(path)
# File path for custom liberys
path_JacobLib = path + "/JacobLib"
path_Sprite = path + "/Sprite"
path_Assets = os.path.dirname(path) + "/Assets/"
path_Map_Gen = os.path.dirname(path) + "/Code" + "/Map_Gen"

import sys
sys.path.insert(0, path_JacobLib)
# import from MyLib
from Error_Report import Report_Error, Make_Error_File
from Class_Factory import Class_Factory

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
wall_List = sprite_Lists[2]
sprite_Scale = sprite_Lists[3]
Map_O = sprite_Lists[4]
# bomb group and factry init
bomb_List = pygame.sprite.Group()
# make bomber man
man_List = pygame.sprite.Group()
man_Factory = Class_Factory("Man", Sprite_Bomberman)
man_Count = 0
for x in background_List:
    if(x.class_Name == "Spawn"):
        man = man_Factory.New(x.Position(), False, sprite_Scale, man_Count)
        man_List.add(man)
        man_Count += 1

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
            elif event.key == pygame.K_w:
                for man in man_List:
                    if man.ID == 1:
                        man.current_Image_Name = "man_Up"
                        man.begin_Run()
            elif event.key == pygame.K_s:
                for man in man_List:
                    if man.ID == 1:
                        man.current_Image_Name = "man_Down"
                        man.begin_Run()
            elif event.key == pygame.K_d:
                for man in man_List:
                    if man.ID == 1:
                        man.current_Image_Name = "man_Right"
                        man.begin_Run()
            elif event.key == pygame.K_a:
                for man in man_List:
                    if man.ID == 1:
                        man.current_Image_Name = "man_Left"
                        man.begin_Run()
            elif event.key == pygame.K_SPACE:
                for man in man_List:
                    if man.ID == 1:
                        man.spawn_B = True

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                for man in man_List:
                    if man.ID == 1:
                        if(man.current_Image_Name == "man_Up"):
                            man.stop_Run()
            elif event.key == pygame.K_s:
                for man in man_List:
                    if man.ID == 1:
                        if(man.current_Image_Name == "man_Down"):
                            man.stop_Run()
            elif event.key == pygame.K_a:
                for man in man_List:
                    if man.ID == 1:
                        if(man.current_Image_Name == "man_Left"):
                            man.stop_Run()
            elif event.key == pygame.K_d:
                for man in man_List:
                    if man.ID == 1:
                        if(man.current_Image_Name == "man_Right"):
                            man.stop_Run()
        # Mouse click event currently spawning bomb
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = mouse.get_pos()

    # --- Game logic should go hered
    for man in man_List:
        bomb_List.add(man.update(Map_O))
    for bomb in bomb_List:
        if(bomb.update(Map_O) == True):
            tiles = Map_O.tile_At(bomb.get_Collision_Coners())
            for tile in tiles:
                tile["Bomb"] = False
            bomb.bomberman.bomb_List.remove(bomb)
            bomb_List.remove(bomb)

    # --- Screen-clearing code goes here

    # Here, we clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.
    # If you want a background image, replace this clear with blit'ing the
    # background image.
    # --- Drawing code should go here
    background_List.draw(screen)
    wall_List.draw(screen)
    bomb_List.draw(screen)
    bush_List.draw(screen)
    man_List.draw(screen)
    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
    # --- Limit to 60 frames per second
    clock.tick(60)
    # print fps
    # print(clock.get_fps())

# Close the window and quit.
pygame.quit()
