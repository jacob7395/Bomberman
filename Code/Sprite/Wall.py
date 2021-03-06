# Example of a sprite using Sprite_Two_Dimensions as a perant

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
import sys
sys.path.insert(0, path_JacobLib)
# import from MyLib
from Sprite_Two_D import Sprite_Two_Dimensions
from Error_Report import Report_Error
from Class_Factory import Class_Factory


class Sprite_Wall(Sprite_Two_Dimensions):
    """Test fucntion for sprite init."""

    def __init__(self, spawn_Area=(0, 0, 0, 0), fixed=False, sprite_Scale=None):
        """Class init."""
        wall = {}
        wall["s_Res"] = (16, 16)
        wall["s_Start"] = (11, 5)
        wall["p_Path"] = path_Assets + "bomberman_Sprite_Sheet.png"
        wall["s_Scale"] = sprite_Scale

        asset_List = [wall]
        # Call the parent class (Sprite) constructor
        super(Sprite_Wall, self).__init__(spawn_Area, fixed, asset_List)
        # Chose the image initaly dispalyed
        self.Set_Image(0)
        # CUSTOM CODE
