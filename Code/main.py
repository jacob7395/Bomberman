# -----------------------------------------------
# Load functions and calsses form remote locations
import random
import os
import time

import pygame
from pygame import draw, display, rect
from pygame.sprite import groupcollide
# setup to improt files fomr MyLib
path = os.path.realpath(__file__)
for i in range(0, 1):
    path = os.path.dirname(path)
# File path for custom liberys
path_JacobLib = path + "/JacobLib"
path_Sprite = path + "/Sprite"
path_Assets = os.path.dirname(path) + "/Assets/"

import sys
sys.path.insert(0, path_JacobLib)
# import from MyLib
from Error_Report import Report_Error, Make_Error_File
from Class_Factory import Class_Factory

sys.path.insert(0, path_Sprite)
# import test sprite
from Example_Sprite import Sprite_Example
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
screen_Size = (700, 500)
screen = display.set_mode(screen_Size)
# Define spawn Area
spawn_Area = (-100, -50, 0, screen_Size[1])
# Set game window
pygame.display.set_caption("Bomberman")
# -----------------------------------------------
# Sprite populations and generation
# This is a list of 'sprites.' Each pepe in the program is
# added to this list. The list is managed by a class called 'Group.'
test_List = pygame.sprite.Group()
# define test asset propertys

test = Sprite_Example((500, 60), False)
test_List.add(test)
# populate my pepe_list
for i in range(0):
    Pep = test_Factory.New(spawn_Area, False, (3, 10))
    # add pepe to sprite lists
    pepe_List.add(Pep)
    all_Sprites_List.add(Pep)

# loop until the user clicks the close button.
done = False
# used to manage how fast the screen updates
clock = pygame.time.Clock()
# -----------------------------------------------
# COLLISTION TEST CODE
# collitions = groupcollide(pepe_List, pepe_List, False, False)
# collitions_Keys = collitions.keys()
# collitions_Values = collitions.values()
#
# for i in range(len(collitions.keys())):
#     l = list(str(collitions_Keys[i]))
#     x = l.index(' ')
#     collitions_Keys[i] = str(collitions_Keys[i])[1:x]
#
# for values in range(len(collitions_Values)):
#     for elements in range(len(collitions_Values[values])):
#         l = list(str(collitions_Values[values][elements]))
#         x = l.index(' ')
#         collitions_Values[values][elements] = str(collitions_Values[values][elements])[1:x]
# -------------------------------------------------------------
# -------- Main Program Loop -----------
while not done:
    # --- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    # --- Game logic should go here

    # --- Screen-clearing code goes here

    # Here, we clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.

    # If you want a background image, replace this clear with blit'ing the
    # background image.
    screen.fill(BLACK)
    # --- Drawing code should go here
    test_List.draw(screen)
    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
    # --- Limit to 60 frames per second
    clock.tick(60)

# Close the window and quit.
pygame.quit()
