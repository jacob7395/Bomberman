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


def Map_Load(screen_Size):
    """Read the map file then returns the group for that."""
    x_Size = 42
    # Setup map path
    path = os.path.realpath(__file__)
    for i in range(0, 2):
        path = os.path.dirname(path)
    path_Maps = path + "/Map_Gen/" + "Map"
    # Generate the map file
    # map_Info[0] = size of each block by pixles where x*x
    # map_Info[1] = contains a tubple where [1][0] is #x blocks and [1][1] is #y blocks
    map_Info = Map_Gen(screen_Size, path_Maps, x_Size)
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

    x_Offset = (screen_Size[0] - (map_Info[0] * map_Info[1][0])) / 2
    y = 0
    x = x_Offset

    for line in lines:
        for character in line:
            if (character == 'w'):
                sprite = wall_Factory.New((x, y), True)
            elif(character == 'g'):
                sprite = grass_Factory.New((x, y), True)
            elif(character == 'p'):
                sprite = pillar_Factory.New((x, y), True)
            sprite.Scale_Imgs(map_Info[0])
            background_List.add(sprite)
            x += map_Info[0]
        x = x_Offset
        y += map_Info[0]
    # return the populated background_List
    return background_List


def Map_Gen(screen_Size=None, file_Path=None, x_Size=42):
    """
    Map_Gen crates a file called Map, this text file contains a map using characters as notation.

    It then populates Map with walles and pillers for the spesific screen screen_Size.
    It also returns a scale size for the blocks to fill the screen correclty.
    """
    # cheack a screen size has been sent
    if(screen_Size == None):
        return None
    # open the file with w to make/clear
    f = open(file_Path, "w")
    # The x map size controls the y map size on a 16:9 aspect ration
    map_Size = [x_Size]
    map_Size.append(int(map_Size[0] / 1.8260869565))

    # Makes sure the map can be generated and corrects squeres if unable
    for x in range(len(map_Size)):
        if((map_Size[x] - 5) % 2 == 1):
            map_Size[x] -= 1

    scale = int(screen_Size[0] / map_Size[0])

    Map_Maker(map_Size[0], map_Size[1], f)

    return [scale, map_Size]


def Map_Maker(x_End, y_End, f):
    """Generates a map that is x_End by y_End where n is the file to put the map in."""
    for n in range((x_End * y_End) - 1, -1, -1):
        current_Line = n / x_End + 1
        last_Line = (n + 1) / x_End + 1

        if(current_Line != last_Line and n < (x_End * y_End) - 2):
            f.write('\n')

        if(current_Line == y_End or current_Line == 1 or n % x_End == 0 or (n + 1) % x_End == 0):
            f.write('w')
        elif((n % x_End) % 2 == 0 and current_Line % 2 == 1):
            f.write('p')
        else:
            f.write('g')
