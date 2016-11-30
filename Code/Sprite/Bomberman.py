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


class Sprite_Bomberman(Sprite_Two_Dimensions):
    """Test fucntion for sprite init."""

    def __init__(self, spawn_Area=(0, 0, 0, 0), fixed=False, sprite_Scale=None, sprite_Man=0):
        """Class init."""

        self.index = 0
        self.run = False
        self.current_Direction = "man_Down"
        self.speed = 10

        man_Down = {}
        man_Down["s_Res"] = (16, 16)
        man_Down["s_Start"] = (0, sprite_Man + 1)
        man_Down["p_Path"] = path_Assets + "bomberman_Sprite_Sheet_v2.png"
        man_Down["s_Scale"] = sprite_Scale
        man_Down["s_Annimated_Len"] = 3
        man_Down["s_Name"] = "man_Down"

        man_Right = {}
        man_Right["s_Res"] = (16, 16)
        man_Right["s_Start"] = (3, sprite_Man + 1)
        man_Right["p_Path"] = path_Assets + "bomberman_Sprite_Sheet_v2.png"
        man_Right["s_Scale"] = sprite_Scale
        man_Right["s_Annimated_Len"] = 3
        man_Right["s_Name"] = "man_Right"

        man_Left = {}
        man_Left["s_Res"] = (16, 16)
        man_Left["s_Start"] = (3, sprite_Man + 1)
        man_Left["p_Path"] = path_Assets + "bomberman_Sprite_Sheet_v2.png"
        man_Left["s_Scale"] = sprite_Scale
        man_Left["s_Annimated_Len"] = 3
        man_Left["s_Name"] = "man_Left"
        man_Left["s_Flip"] = (True, False)

        man_Up = {}
        man_Up["s_Res"] = (16, 16)
        man_Up["s_Start"] = (7, sprite_Man + 1)
        man_Up["p_Path"] = path_Assets + "bomberman_Sprite_Sheet_v2.png"
        man_Up["s_Scale"] = sprite_Scale
        man_Up["s_Annimated_Len"] = 2
        man_Up["s_Name"] = "man_Up"

        asset_List = [man_Down, man_Right, man_Left, man_Up]

        # Call the parent class (Sprite) constructor
        super(Sprite_Bomberman, self).__init__(spawn_Area, fixed, asset_List)
        # Chose the image initaly dispalyed
        self.Set_Image(self.current_Direction)

    def begin_Run(self):
        self.init_Time = time.clock()
        self.change_Time = float(0.1) / (self.speed / 2)
        self.run = True

    def stop_Run(self):
        self.run = False
        self.index = 0
        self.Set_Image(self.current_Direction)

    def steb_Back(self):
        if(self.current_Direction == "man_Down"):
            self.Incroment_Position(0, -1 * self.speed)
        elif(self.current_Direction == "man_Left"):
            self.Incroment_Position(1 * self.speed, 0)
        elif(self.current_Direction == "man_Up"):
            self.Incroment_Position(0, 1 * self.speed)
        elif(self.current_Direction == "man_Right"):
            self.Incroment_Position(-1 * self.speed, 0)

    def update(self):
        if(self.run == True):
            t = time.clock()
            self.position_Old = self.Position()
            if(t > self.init_Time + self.change_Time):
                self.index += 1
                if(self.index > len(self.images[self.current_Direction]) - 1):
                    self.index = 0
                self.init_Time = t
                self.Set_Image(self.current_Direction)
            if(self.current_Direction == "man_Down"):
                self.Incroment_Position(0, 1 * self.speed)
            elif(self.current_Direction == "man_Left"):
                self.Incroment_Position(-1 * self.speed, 0)
            elif(self.current_Direction == "man_Up"):
                self.Incroment_Position(0, -1 * self.speed)
            elif(self.current_Direction == "man_Right"):
                self.Incroment_Position(1 * self.speed, 0)
