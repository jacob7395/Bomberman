import pygame
import os
from os import path

import random
from random import randrange
# setup to improt files fomr MyLib
path = os.path.realpath(__file__)
for i in range(0, 2):
    path = os.path.dirname(path)

path_JacobLib = path + "/JacobLib"
path_Assets = os.path.dirname(path) + "/Assets/"
path_Maps = path + "/Map_Gen/"
path_Sprites = path + "/Sprite"
import sys
sys.path.insert(0, path_JacobLib)
# import from MyLib
from Sprite_Two_D import Sprite_Two_Dimensions
from Error_Report import Report_Error
from Class_Factory import Class_Factory
# import sprites
sys.path.insert(0, path_Sprites)
from Wall import Sprite_Wall
from Grass import Sprite_Grass
from Pillar import Sprite_Pillar


def Map_Reader():
    """Read the map file then returns the group for that."""
    # Setup map path
    path = os.path.realpath(__file__)
    for i in range(0, 2):
        path = os.path.dirname(path)
    path_Maps = path + "/Map_Gen/" + "Map"
    # Make sprite factorys for each sprite
    wall_Factory = Class_Factory("WallID", Sprite_Wall)
    grass_Factory = Class_Factory("GrassID", Sprite_Grass)
    pillar_Factory = Class_Factory("GrassID", Sprite_Pillar)
    # make a list for the baground this will be retuned
    background_List = pygame.sprite.Group()
    # Read each line of the map
    with open(path_Maps, "r") as f:
        lines = f.readlines()
        f.close

    y = 0
    x = 0

    for line in lines:
        for character in line:
            if (character == 'w'):
                sprite = wall_Factory.New((x, y), True)
            elif(character == 'g'):
                sprite = grass_Factory.New((x, y), True)
            elif(character == 'p'):
                sprite = pillar_Factory.New((x, y), True)
            background_List.add(sprite)
            x += 16
        x = 0
        y += 16
    # return the populated background_List
    return background_List

Map_Reader()
# with open(file_Path, "r") as f:
#     lines = f.readlines()
#     choice = random.choice(lines)
#     f.close
#
# with open(file_Path, "w") as f:
#     for line in lines:
#         if line != choice:
#             f.write(line)
#
# print("Random Choice is:\n{}".format(choice))
