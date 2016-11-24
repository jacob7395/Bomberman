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
from Player import Player


class Sprite_Bomb(Player):
    """Test fucntion for sprite init."""

    def __init__(self, spawn_Area=(0, 0, 0, 0), fixed=False, sprite_Scale=None, fuse_Time=1):
        """Class init."""
        # bomb propertys
        self.current_Image_Name = "bomb"
        self.collition_Offset = 10
        self.scale = sprite_Scale
        self.index = 0
        self.change_Time = float(fuse_Time) / 3
        self.t_Old = time.clock()
        self.collition_Offset = 5
        self.acceleration = 1
        self.v_Start = (0, 0)
        # pick random grass tile
        grass = random.randint(0, 2)

        bomb = {}
        bomb["s_Res"] = (16, 16)
        bomb["s_Start"] = (12, 2)
        bomb["p_Path"] = path_Assets + "bomberman_Sprite_Sheet_v2.png"
        bomb["s_Scale"] = sprite_Scale
        bomb["s_Annimated_Len"] = 3
        bomb["s_Name"] = "bomb"

        asset_List = [bomb]

        # Call the parent class (Sprite) constructor
        super(Sprite_Bomb, self).__init__(spawn_Area, fixed, asset_List)
        # Chose the image initaly dispalyed
        self.Set_Image(self.current_Image_Name)
        self.init_Time = time.clock()
        self.blow_Time = self.init_Time + (float(fuse_Time))
        self.fuse_Time = float(fuse_Time)
        self.old_Tile = None

    def set_Owner(self, bomberman):
        self.bomberman = bomberman

    def update_Positions(self, dt, map_Object):
        move = self.check_Move((self.velocity_x * dt, self.velocity_y * dt), map_Object)
        move[1] = True
        if(move[0] == True):
            current_Tile = map_Object.tile_At([self.get_Sprite_Center()])[0]
            if(current_Tile["Position"] != self.old_Tile["Position"]):
                if(current_Tile["Bomb"] == False):
                    current_Tile["Bomb"] = True
                    current_Tile["Bomb_Object"] = self.old_Tile["Bomb_Object"]
                    current_Tile["Bomb_Owner"] = self.old_Tile["Bomb_Owner"]
                    self.old_Tile["Bomb"] = False
                    self.old_Tile["Bomb_Object"] = None
                    self.old_Tile["Bomb_Owner"] = None
                    self.old_Tile = current_Tile
                else:
                    move[1] = False
                    self.Velocity(0, 0)
            if(move[1] == True):
                self.Incroment_Position((self.velocity_x * dt, self.velocity_y * dt))
                self.Calc_Accleration()

    def update(self, map_Object):
        # initalize first tile
        if(self.old_Tile == None):
            self.old_Tile = map_Object.tile_At([self.get_Sprite_Center()])[0]
        t = time.clock()
        if(t > self.init_Time + self.change_Time):
            self.index += 1
            # if index is out of range loop animation
            if(self.index > len(self.images[self.current_Image_Name]) - 1):
                return True
            # reset timer
            self.init_Time = t
            # update the current image
            self.Set_Image(self.current_Image_Name)
        dt = t - self.t_Old
        if(dt * abs(self.velocity_x) > 1 or dt * abs(self.velocity_y) > 1):
            self.update_Positions(dt, map_Object)
            self.t_Old = t
            # update the current image
            self.Set_Image(self.current_Image_Name)
