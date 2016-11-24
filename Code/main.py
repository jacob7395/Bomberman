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
screen_Size = (1280, 720)
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
# bomb group and factry init
bomb_List = pygame.sprite.Group()
bomb_Factory = Class_Factory("Bomb", Sprite_Bomb)
# make bomber man
man_List = pygame.sprite.Group()
man_Factory = Class_Factory("Man", Sprite_Bomberman)
man_Count = 0
for x in background_List:
    if(x.class_Name == "Spawn"):
        man = man_Factory.New(x.Position(), False, sprite_Scale, man_Count)
        man.Alphe_Con()
        man_List.add(man)
        man_Count += 1
# adds alpha color for bushes, color = default = BLACK = (0,0,0)
for sprite in bush_List:
    sprite.Alphe_Con()

# loop until the user clicks the close button.
done = False
# used to manage how fast the screen updates
clock = pygame.time.Clock()
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
                        man.current_Direction = "man_Up"
                        man.begin_Run()
            elif event.key == pygame.K_s:
                for man in man_List:
                    if man.ID == 1:
                        man.current_Direction = "man_Down"
                        man.begin_Run()
            elif event.key == pygame.K_d:
                for man in man_List:
                    if man.ID == 1:
                        man.current_Direction = "man_Right"
                        man.begin_Run()
            elif event.key == pygame.K_a:
                for man in man_List:
                    if man.ID == 1:
                        man.current_Direction = "man_Left"
                        man.begin_Run()
            elif event.key == pygame.K_SPACE:
                for man in man_List:
                    if man.ID == 1:
                        bomb = bomb_Factory.New(man.Position(), False, sprite_Scale, 1)
                        bomb.Alphe_Con()
                        bomb_List.add(bomb)

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                for man in man_List:
                    if man.ID == 1:
                        if(man.current_Direction == "man_Up"):
                            man.stop_Run()
            elif event.key == pygame.K_s:
                for man in man_List:
                    if man.ID == 1:
                        if(man.current_Direction == "man_Down"):
                            man.stop_Run()
            elif event.key == pygame.K_a:
                for man in man_List:
                    if man.ID == 1:
                        if(man.current_Direction == "man_Left"):
                            man.stop_Run()
            elif event.key == pygame.K_d:
                for man in man_List:
                    if man.ID == 1:
                        if(man.current_Direction == "man_Right"):
                            man.stop_Run()
        # Mouse click event currently spawning bomb
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = mouse.get_pos()
            bomb = bomb_Factory.New(pos, False, sprite_Scale, 1)
            bomb.Alphe_Con()
            bomb_List.add(bomb)

    # --- Game logic should go here
    # Calculate collitions with Bman
    man_Collitions = pygame.sprite.groupcollide(man_List, wall_List, False, False)
    man_Collitions.update(pygame.sprite.groupcollide(man_List, bush_List, False, False))
    if(man_Collitions):
        for man in man_Collitions.keys():
            man.stop_Run()
            collition_Pos = man_Collitions[man][0].Position()
            man.Position(man.position_Old[0], man.position_Old[1])
    # Update curret bombs
    for bomb in bomb_List:
        if(bomb.update() == True):
            bomb_List.remove(bomb)
    for man in man_List:
        man.update()
        if(man.ID == 1):
            pass
            # print("Pos:" + str(man.Position()))

            # if(man.current_Direction == "man_Down" or man.current_Direction == "man_Up"):
            #     S = sign(collition_Pos[1] - man.Position()[1])
            #     man.position_y = collition_Pos[1] + sprite_Scale * S
            # elif(man.current_Direction == "man_Left" or man.current_Direction == "man_Right"):
            #     S = sign(collition_Pos[0] - man.Position()[0])
            #     man.position_x = collition_Pos[0] + sprite_Scale * S

            # --- Screen-clearing code goes here

            # Here, we clear the screen to white. Don't put other drawing commands
            # above this, or they will be erased with this command.

            # If you want a background image, replace this clear with blit'ing the
            # background image.
    screen.fill(BLACK)
    # --- Drawing code should go here
    if(bDrwan == False):
        background_List.draw(screen)
        wall_List.draw(screen)
        bush_List.draw(screen)
        bomb_List.draw(screen)
        bDrawn = True
    man_List.draw(screen)
    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
    # --- Limit to 60 frames per second
    clock.tick(60)
    if(clock.get_fps() > 20):
        print ("fps:" + str(clock.get_fps()))

# Close the window and quit.
pygame.quit()
