# Example of a sprite using Sprite_Two_Dimensions as a perant

import pygame
import datetime
import time
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
import sys
sys.path.insert(0, path_JacobLib)
# import from MyLib
from Sprite_Two_D import Sprite_Two_Dimensions
from Error_Report import Report_Error
from Class_Factory import Class_Factory


class Player(Sprite_Two_Dimensions):
    """Test fucntion for sprite init."""

    def __init__(self, spawn_Area=(0, 0), fixed=False, asset_List=[], sprite_Scale=16):
        """Class init."""
        # shared values
        self.t_Acc_Old = time.clock()
        self.index = 0
        # shared blank image
        blank = {}
        blank["s_Res"] = (16, 16)
        blank["s_Start"] = (6, 0)
        blank["p_Path"] = path_Assets + "bomberman_Sprite_Sheet_v2.png"
        blank["s_Scale"] = sprite_Scale
        blank["s_Annimated_Len"] = 1
        blank["s_Name"] = "blank"

        asset_List.append(blank)
        # Call the parent class (Sprite) constructor
        super(Player, self).__init__(spawn_Area, fixed, asset_List)

    def check_Neighbor_Tiles(self, map_Object):
        pos = self.get_Sprite_Center()
        tiles = []
        tiles.append([map_Object.tile_At([(pos[0] + self.scale, pos[1])])[0], (1, 0)])
        tiles.append([map_Object.tile_At([(pos[0] - self.scale, pos[1])])[0], (-1, 0)])
        tiles.append([map_Object.tile_At([(pos[0], pos[1] + self.scale)])[0], (0, 1)])
        tiles.append([map_Object.tile_At([(pos[0], pos[1] - self.scale)])[0], (0, -1)])
        return tiles

    def position_In_Collition(self, pos):
        cornors = self.get_Collision_Coners()
        if(cornors[0][0] < pos[0] and cornors[3][0] > pos[0] and cornors[0][1] < pos[1] and cornors[3][1] > pos[1]):
            return True
        return False

    def check_Move(self, move, map_Object):
        corners = self.get_Collision_Coners()
        new_Corners = []
        for corner in corners:
            new_Corners.append((corner[0] + move[0], corner[1] + move[1]))
        tile_At_Move = map_Object.tile_At(new_Corners)
        return [map_Object.get_Movable(tile_At_Move), self.check_Bomb(map_Object, new_Corners)]

    def check_Bomb(self, map_Object, position):
        for pos in position:
            map_Tile = map_Object.tile_At([pos])[0]
            if(map_Tile["Bomb"] == True):
                return (True, map_Tile["Bomb_Object"])
        return False

    def Calc_Accleration(self):
        t = time.clock()
        dt = t - self.t_Acc_Old
        if(self.velocity_x != 0):
            self.velocity_x += self.acceleration_x * dt
        if(self.velocity_y != 0):
            self.velocity_y += self.acceleration_y * dt
        # calculate a change in direction
        # when there has been a change in direction set the velocity to 0
        if(self.v_Start[0] > 0 or self.v_Start[1] > 0 and (self.v_Start[0] + self.v_Start[1] != 0)):
            if(self.v_Start[0] - self.velocity_x > self.v_Start[0]):
                self.velocity_x = 0
            if(self.v_Start[1] - self.velocity_y > self.v_Start[1]):
                self.velocity_y = 0
        elif(self.v_Start[0] + self.v_Start[1] != 0):
            if(self.v_Start[0] + self.velocity_x > self.v_Start[0]):
                self.velocity_x = 0
            if(self.v_Start[1] + self.velocity_y > self.v_Start[1]):
                self.velocity_y = 0

        self.t_Acc_Old = t
