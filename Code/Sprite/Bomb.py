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


class Sprite_Bomb(Sprite_Two_Dimensions):
    """Test fucntion for sprite init."""

    def __init__(self, spawn_Area=(0, 0, 0, 0), fixed=False, sprite_Scale=None, fuse_Time=1):
        """Class init."""
        # pick random grass tile
        grass = random.randint(0, 2)

        bomb_One = {}
        bomb_One["s_Res"] = (16, 16)
        bomb_One["s_Start"] = (12, 2)
        bomb_One["p_Path"] = path_Assets + "bomberman_Sprite_Sheet.png"
        bomb_One["s_Scale"] = sprite_Scale

        bomb_Two = {}
        bomb_Two["s_Res"] = (16, 16)
        bomb_Two["s_Start"] = (12, 3)
        bomb_Two["p_Path"] = path_Assets + "bomberman_Sprite_Sheet.png"
        bomb_Two["s_Scale"] = sprite_Scale

        bomb_Three = {}
        bomb_Three["s_Res"] = (16, 16)
        bomb_Three["s_Start"] = (12, 4)
        bomb_Three["p_Path"] = path_Assets + "bomberman_Sprite_Sheet.png"
        bomb_Three["s_Scale"] = sprite_Scale

        asset_List = [bomb_One, bomb_Two, bomb_Three]

        # Call the parent class (Sprite) constructor
        super(Sprite_Bomb, self).__init__(spawn_Area, fixed, asset_List)
        # Chose the image initaly dispalyed
        self.Set_Image(0)
        self.init_Time = time.clock()
        self.blow_Time = self.init_Time + (float(fuse_Time))
        self.fuse_Time = float(fuse_Time)

    def update(self):
        t = time.clock()
        if(t > self.blow_Time):
            return True
        elif(self.blow_Time - t < self.fuse_Time / 3):
            self.Set_Image(2)
        elif(self.blow_Time - t < self.fuse_Time * (2.0 / 3)):
            self.Set_Image(1)
