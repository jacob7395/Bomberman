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


class Sprite_Spawn(Sprite_Two_Dimensions):
    """Test fucntion for sprite init."""

    def __init__(self, spawn_Area=(0, 0, 0, 0), fixed=False):
        """Class init."""
        spawn = {}
        spawn["s_Res"] = (16, 16)
        spawn["s_Start"] = (14, 14)
        spawn["p_Path"] = path_Assets + "16bit_Ground_Sheet.gif"

        asset_List = [spawn]
        # Call the parent class (Sprite) constructor
        super(Sprite_Spawn, self).__init__(spawn_Area, fixed, asset_List)
        # Chose the image initaly dispalyed
        self.Set_Image(0)
        # CUSTOM CODE
