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


class Sprite_Explotion(Player):

    def __init__(self,
                 spawn_Area=(0, 0, 0, 0),
                 asset_List,
                 fixed=False,
                 sprite_Scale=None,
                 map_Object=None,
                 direction=None,
                 bomb=None,
                 explotion_Grown=False,
                 explotion_Size=None,
                 explotion_Base=None,
                 explotion_Groth_Rate=None
                 ):
        """Class init."""
        # bomb propertys
        self.current_Image_Name = None
        self.collition_Offset = 2
        self.scale = sprite_Scale
        self.bomb = bomb
        # explotion props
        self.explotion_Grown = explotion_Grown
        self.explotion_Size = explotion_Size
        self.explotion_Groth_Rate = explotion_Groth_Rate
        self.explotion_Change_Time = time.clock() + self.explotion_Groth_Rate
        self.bushes_to_Destroyed = []

        # Call the parent class (Sprite) constructor
        super(Sprite_Explotion_Arm, self).__init__(spawn_Area, fixed, asset_List, sprite_Scale)


class Sprite_Explotion_Arm(Sprite_Explotion):

    def __init__(self,
                 spawn_Area=(0, 0, 0, 0),
                 fixed=False,
                 sprite_Scale=None,
                 map_Object=None,
                 direction=None,
                 bomb=None,
                 explotion_Base=None,
                 explotion_Groth_Rate=None,
                 explotion_Size=None):
        """Class init."""
        self.scale = sprite_Scale
        self.bomb = bomb
        # explotion props
        self.explotion_Base = explotion_Base
        self.explotion_Grown = False
        self.explotion_Size = explotion_Size
        self.explotion_Groth_Rate = explotion_Groth_Rate
        self.explotion_Change_Time = time.clock() + self.explotion_Groth_Rate
        self.direction = direction
        self.bushes_to_Destroyed = []
        # determin what direction the explotion is traveling and if an end is needed
        if(direction[0] != 0):
            if(self.explotion_Size == 0):
                if(self.direction == (1, 0)):
                    self.current_Image_Name = "explotion_Vertical_End_Fliped"
                else:
                    self.current_Image_Name = "explotion_Vertical_End"
            else:
                self.current_Image_Name = "explotion_Vertical"
        elif(direction[1] != 0):
            if(self.explotion_Size == 0):
                if(self.direction == (0, -1)):
                    self.current_Image_Name = "explotion_Horizontal_End_Fliped"
                else:
                    self.current_Image_Name = "explotion_Horizontal_End"
            else:
                self.current_Image_Name = "explotion_Horizontal"

        explotion_Vertical = {}
        explotion_Vertical["s_Res"] = (16, 16)
        explotion_Vertical["s_Start"] = (1, 5)
        explotion_Vertical["p_Path"] = path_Assets + "bomberman_Sprite_Sheet_v2.png"
        explotion_Vertical["s_Scale"] = sprite_Scale
        explotion_Vertical["s_Annimated_Len"] = 1
        explotion_Vertical["s_Name"] = "explotion_Vertical"

        explotion_Vertical_End = {}
        explotion_Vertical_End["s_Res"] = (16, 16)
        explotion_Vertical_End["s_Start"] = (0, 5)
        explotion_Vertical_End["p_Path"] = path_Assets + "bomberman_Sprite_Sheet_v2.png"
        explotion_Vertical_End["s_Scale"] = sprite_Scale
        explotion_Vertical_End["s_Annimated_Len"] = 1
        explotion_Vertical_End["s_Name"] = "explotion_Vertical_End"

        explotion_Vertical_End_Filp = {}
        explotion_Vertical_End_Filp["s_Res"] = (16, 16)
        explotion_Vertical_End_Filp["s_Start"] = (0, 5)
        explotion_Vertical_End_Filp["p_Path"] = path_Assets + "bomberman_Sprite_Sheet_v2.png"
        explotion_Vertical_End_Filp["s_Scale"] = sprite_Scale
        explotion_Vertical_End_Filp["s_Annimated_Len"] = 1
        explotion_Vertical_End_Filp["s_Flip"] = (True, False)
        explotion_Vertical_End_Filp["s_Name"] = "explotion_Vertical_End_Fliped"

        explotion_Horizontal = {}
        explotion_Horizontal["s_Res"] = (16, 16)
        explotion_Horizontal["s_Start"] = (15, 1)
        explotion_Horizontal["p_Path"] = path_Assets + "bomberman_Sprite_Sheet_v2.png"
        explotion_Horizontal["s_Scale"] = sprite_Scale
        explotion_Horizontal["s_Annimated_Len"] = 1
        explotion_Horizontal["s_Name"] = "explotion_Horizontal"

        explotion_Horizontal_End = {}
        explotion_Horizontal_End["s_Res"] = (16, 16)
        explotion_Horizontal_End["s_Start"] = (15, 2)
        explotion_Horizontal_End["p_Path"] = path_Assets + "bomberman_Sprite_Sheet_v2.png"
        explotion_Horizontal_End["s_Scale"] = sprite_Scale
        explotion_Horizontal_End["s_Annimated_Len"] = 1
        explotion_Horizontal_End["s_Name"] = "explotion_Horizontal_End"

        explotion_Horizontal_End_Fliped = {}
        explotion_Horizontal_End_Fliped["s_Res"] = (16, 16)
        explotion_Horizontal_End_Fliped["s_Start"] = (15, 2)
        explotion_Horizontal_End_Fliped["p_Path"] = path_Assets + "bomberman_Sprite_Sheet_v2.png"
        explotion_Horizontal_End_Fliped["s_Scale"] = sprite_Scale
        explotion_Horizontal_End_Fliped["s_Annimated_Len"] = 1
        explotion_Horizontal_End_Fliped["s_Flip"] = (False, True)
        explotion_Horizontal_End_Fliped["s_Name"] = "explotion_Horizontal_End_Fliped"

        asset_List = [explotion_Vertical, explotion_Vertical_End, explotion_Vertical_End_Filp, explotion_Horizontal, explotion_Horizontal_End, explotion_Horizontal_End_Fliped]
        # Call the parent class (Sprite) constructor
        super(Sprite_Explotion_Arm, self).__init__(spawn_Area, fixed, asset_List, sprite_Scale)
        # Chose the image initaly dispalyed
        self.Set_Image(self.current_Image_Name)
        # Check what bushes the explotions collide with
        tile = map_Object.tile_At([self.get_Sprite_Center()])[0]
        if(tile["Tile"] == 'b'):
            tile["Movable"] = True
            tile["Tile"] = 'g'
            self.bushes_to_Destroyed.append(tile["Position"])

    def update(self, map_Object):
        t = time.clock()
        if(t > self.explotion_Change_Time and self.explotion_Grown == False):
            # check groth reate
            if(self.explotion_Size != 0):
                self.explotion_Size -= 1
                if(self.explotion_Grown == False):
                    self.explotion_Grown = True
                    pos = self.get_Sprite_Center()
                    tiles = self.check_Neighbor_Tiles(map_Object)
                    for tile in tiles:
                        if(tile[0]["Tile"] != 'w' and tile[1] == self.direction):
                            arm_Pos = (pos[0] + (tile[1][0] * self.scale) - self.scale / 2, pos[1] + (tile[1][1] * self.scale) - self.scale / 2)
                            explotion_Arm = self.explotion_Base.explotion_Arm_Factory.New(arm_Pos, False, self.scale, map_Object, tile[1], self.bomb, self.explotion_Base, self.explotion_Groth_Rate, self.explotion_Size)
                            self.bomb.explotion_List.add(explotion_Arm)
                            self.explotion_Base.explotion_Arm_List.add(explotion_Arm)


class Sprite_Explotion_Base(Player):
    """Test fucntion for sprite init."""

    def __init__(self, spawn_Area=(0, 0, 0, 0), fixed=False, sprite_Scale=None, map_Object=None, explotion_Size=2, bomb=None):
        """Class init."""
        # bomb propertys
        self.current_Image_Name = "explotion"
        self.collition_Offset = 2
        self.scale = sprite_Scale
        self.bomb = bomb
        # explotion varibles
        self.explotion_Arm_List = pygame.sprite.Group()
        self.explotion_Arm_Factory = Class_Factory("Explotion_Arm", Sprite_Explotion_Arm)
        self.explotion_Grown = True
        self.explotion_Growing = True
        self.explotion_Size = explotion_Size
        self.explotion_Groth_Rate = 0.01
        self.explotion_Timeout = 0.25
        self.explotion_Change_Time = time.clock() + self.explotion_Groth_Rate
        self.bushes_to_Destroyed = []

        explotion = {}
        explotion["s_Res"] = (16, 16)
        explotion["s_Start"] = (2, 5)
        explotion["p_Path"] = path_Assets + "bomberman_Sprite_Sheet_v2.png"
        explotion["s_Scale"] = sprite_Scale
        explotion["s_Annimated_Len"] = 1
        explotion["s_Name"] = "explotion"

        asset_List = [explotion]

        # Call the parent class (Sprite) constructor
        super(Sprite_Explotion_Base, self).__init__(spawn_Area, fixed, asset_List, sprite_Scale)
        # Chose the image initaly dispalyed
        self.Set_Image(self.current_Image_Name)

    def set_Owner(self, bomb):
        self.bomb = bomb

    def update(self, map_Object):
        t = time.clock()
        if(t > self.explotion_Change_Time):
            # reset explotion time
            self.explotion_Change_Time = time.clock() + self.explotion_Groth_Rate

            if(self.explotion_Size != 0):
                self.explotion_Size -= 1
            elif(self.explotion_Growing == True):
                self.explotion_Change_Time = time.clock() + self.explotion_Timeout
                self.explotion_Growing = False
            else:
                return True

            if(self.explotion_Grown == True):
                self.explotion_Grown = False
                pos = self.get_Sprite_Center()
                tiles = self.check_Neighbor_Tiles(map_Object)
                for tile in tiles:
                    if(tile[0]["Tile"] != 'w'):
                        arm_Pos = (pos[0] + (tile[1][0] * self.scale) - self.scale / 2, pos[1] + (tile[1][1] * self.scale) - self.scale / 2)
                        explotion_Arm = self.explotion_Arm_Factory.New(arm_Pos, False, self.scale, map_Object, tile[1], self.bomb, self, self.explotion_Groth_Rate, self.explotion_Size)
                        self.bomb.explotion_List.add(explotion_Arm)
                        self.explotion_Arm_List.add(explotion_Arm)

        for explotion_Arm in self.explotion_Arm_List:
            explotion_Arm.update(map_Object)
