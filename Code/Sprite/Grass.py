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


class Sprite_Grass(Sprite_Two_Dimensions):
    """Test fucntion for sprite init."""

    def __init__(self, spawn_Area=(0, 0, 0, 0), fixed=False, sprite_Scale=None):
        """Class init."""
        # pick random grass tile
        grass = random.randint(0, 2)

        grass_One = {}
        grass_One["s_Res"] = (16, 16)
        grass_One["s_Start"] = (1, 0)
        grass_One["p_Path"] = path_Assets + "bomberman_Sprite_Sheet.png"
        grass_One["s_Scale"] = sprite_Scale

        grass_Two = {}
        grass_Two["s_Res"] = (16, 16)
        grass_Two["s_Start"] = (0, 0)
        grass_Two["p_Path"] = path_Assets + "bomberman_Sprite_Sheet.png"
        grass_Two["s_Scale"] = sprite_Scale

        grass_Three = {}
        grass_Three["s_Res"] = (16, 16)
        grass_Three["s_Start"] = (2, 0)
        grass_Three["p_Path"] = path_Assets + "bomberman_Sprite_Sheet.png"
        grass_Three["s_Scale"] = sprite_Scale

        asset_List = [grass_One, grass_Two, grass_Three]
        asset_List = [asset_List[grass]]

        # Call the parent class (Sprite) constructor
        super(Sprite_Grass, self).__init__(spawn_Area, fixed, asset_List)
        # Chose the image initaly dispalyed
        self.Set_Image(0)
        # CUSTOM CODE
