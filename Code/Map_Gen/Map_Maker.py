import pygame
import os
from os import path

import random
from random import randrange

from Map_Object import o_Map
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
from Bush import Sprite_Bush
from Spawn import Sprite_Spawn
from Brick import Sprite_Brick


def Map_Load(screen_Size, x_Size=42):
    """Read the map file then returns the group for that."""
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
    wall_Factory = Class_Factory("Wall", Sprite_Wall)
    grass_Factory = Class_Factory("Grass", Sprite_Grass)
    pillar_Factory = Class_Factory("Pillar", Sprite_Pillar)
    bush_Factory = Class_Factory("Bush", Sprite_Bush)
    spawn_Factory = Class_Factory("Spawn", Sprite_Spawn)
    brick_Factory = Class_Factory("Brick", Sprite_Brick)
    # make a list for the baground this will be retuned
    background_List = pygame.sprite.Group()
    bush_List = pygame.sprite.Group()
    wall_List = pygame.sprite.Group()
    # Read each line of the map
    with open(path_Maps, "r") as f:
        map_String = f.readlines()
        f.close

    x_Offset = (screen_Size[0] - (map_Info[0] * map_Info[1][0])) / 2
    y = 0
    x = x_Offset

    for row in map_String:
        for character in row:
            if (character == 'w'):
                sprite = wall_Factory.New((x, y), True, map_Info[0])
            elif(character == 'g'):
                sprite = grass_Factory.New((x, y), True, map_Info[0])
            elif(character == 'p'):
                sprite = pillar_Factory.New((x, y), True, map_Info[0])
            elif(character == 'b'):
                sprite1 = grass_Factory.New((x, y), True, map_Info[0])
                sprite2 = bush_Factory.New((x, y), True, map_Info[0])
            elif(character == 's'):
                sprite = spawn_Factory.New((x, y), True, map_Info[0])
            elif(character == 'i'):
                sprite = brick_Factory.New((x, y), True, map_Info[0])
            # fix bush and grass collision
            if(character == 'b'):
                sprite1.Scale_Imgs(map_Info[0])
                sprite2.Scale_Imgs(map_Info[0])
                background_List.add(sprite1)
                bush_List.add(sprite2)
            elif(sprite.class_Name == "Wall"):
                sprite.Scale_Imgs(map_Info[0])
                wall_List.add(sprite)
            else:
                sprite.Scale_Imgs(map_Info[0])
                background_List.add(sprite)
            x += map_Info[0]
        x = x_Offset
        y += map_Info[0]

    map_Object = o_Map(map_String, map_Info[0], x_Offset)
    # return the populated background_List
    return [background_List, bush_List, wall_List, map_Info[0], map_Object]


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


def Assembe_Map(map):
    """Convert a list of string into a single string."""
    assembled_Map = ""
    for y in map:
        for x in y:
            if(x != ''):
                assembled_Map += x
        assembled_Map += "\n"
    return assembled_Map


def Map_Maker(x_End, y_End, f):
    """Generate a map that is x_End by y_End where n is the file to put the map in."""
    m = ""

    mp = []
    # fill the map row by row
    # first run addes walls busehs and grass
    y = 0
    while(y < y_End):
        x = 0
        line = []
        while(x < x_End):
            if((y == 0 or y == y_End - 1 or x == 0 or x == x_End - 1) or (y % 2 == 0 and x % 2 == 0)):
                line.append("w")
            else:
                if(random.randint(0, 100) <= 90):
                    line.append("g")
                else:
                    line.append("b")
            x += 1
        mp.append(line)
        x = 0
        y += 1
    # Second run adds spawns
    y = 0
    while(y < y_End):
        x = 0
        line = []
        while(x < x_End):
            if((x == 1 and y == 1) or (x == 1 and y == y_End - 2) or (x == x_End - 2 and y == 1) or (x == x_End - 2 and y == y_End - 2)):
                mp[y][x] = 's'
                if(mp[y][x + 1] != 'w'):
                    mp[y][x + 1] = 'i'
                if(mp[y + 1][x] != 'w'):
                    mp[y + 1][x] = 'i'
                if(mp[y - 1][x] != 'w'):
                    mp[y - 1][x] = 'i'
                if(mp[y][x - 1] != 'w'):
                    mp[y][x - 1] = 'i'
            x += 1
        y += 1

    f.write(Assembe_Map(mp))

# screen_Size = (1280, 720)
# background_List = Map_Load(screen_Size)
