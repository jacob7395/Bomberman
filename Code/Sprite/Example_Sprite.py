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


class Sprite_Example(Sprite_Two_Dimensions):
    """Test fucntion for sprite init."""

    def __init__(self, spawn_Area=(0, 0, 0, 0), fixed=False):
        """Class init."""
        asset_One = {}
        asset_One["s_Res"] = (16, 16)
        asset_One["s_Start"] = (0, 5)
        asset_One["s_End"] = (3, 5)
        asset_One["p_Path"] = path_Assets + "bomberman_Sprite_Sheet.png"
        asset_One["s_Scale"] = 5

        asset_Two = {}
        asset_Two["s_Res"] = (16, 16)
        asset_Two["s_Start"] = (3, 3)
        asset_Two["s_End"] = None
        asset_Two["p_Path"] = path_Assets + "bomberman_Sprite_Sheet.png"
        asset_Two["s_Scale"] = 5
        asset_Two["s_Flip"] = (False, True)

        asset_List = [asset_One, asset_Two]
        # Call the parent class (Sprite) constructor
        super(Sprite_Example, self).__init__(spawn_Area, fixed, asset_List)
        # Chose the image initaly dispalyed
        self.Set_Image(1)
        # CUSTOM CODE

test = Sprite_Example((50, 60, 50, 60), False)
