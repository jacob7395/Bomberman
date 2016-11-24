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
# load bomb asset
sys.path.insert(0, path_Assets)
from Bomb import Sprite_Bomb


class Sprite_Bomberman(Player):
    """Test fucntion for sprite init."""

    def __init__(self, spawn_Area=(0, 0, 0, 0), fixed=False, sprite_Scale=None, sprite_Man=0):
        """Class init."""

        self.index = 0
        self.run = False
        self.current_Image_Name = "man_Down"
        self.speed = 200
        self.animation_Rate = 65
        self.t = 0
        self.oldt = 0
        self.scale = sprite_Scale
        self.collition_Offset = 10
        # make bomb group and factry init
        self.bomb_List = pygame.sprite.Group()
        self.bomb_Factory = Class_Factory("Bomb", Sprite_Bomb)
        self.spawn_B = False
        self.bomb_Movable = False
        self.bomb_Kick_Power = 200
        self.bomb_Slow_Rate = 2
        self.bomb_Count = 5
        self.bomb_Start_Replenishment = False
        self.bomb_Next_Replenishment = 0
        self.bomb_Replenish_Rate = 5

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
        self.Set_Image(self.current_Image_Name)

    def begin_Run(self):
        self.init_Time = time.clock()
        self.change_Time = float(0.1) / (self.speed / self.animation_Rate)
        self.run = True
        self.oldt = time.clock()

    def stop_Run(self):
        self.run = False
        self.index = 0
        self.Set_Image(self.current_Image_Name)

    def update_Positions(self, dt, map_Object):
        on_Bomb = self.check_Bomb(map_Object, self.get_Collision_Coners())
        if(on_Bomb == False and self.bomb_Movable == True):
            self.bomb_Movable = False

        move = self.check_Move((self.velocity_x * dt, self.velocity_y * dt), map_Object)
        if(move[0] == True and (move[1] == False or self.bomb_Movable == True)):
            self.Incroment_Position((self.velocity_x * dt, self.velocity_y * dt))
        else:
            if(type(move[1]) != bool):
                if(move[1][1].bomberman.ID == self.ID):
                    move[1][1].acceleration = self.bomb_Kick_Power / self.bomb_Slow_Rate
                    if(self.current_Image_Name == "man_Down"):
                        move[1][1].Velocity(0, self.bomb_Kick_Power)
                        move[1][1].Acceleration(0, -move[1][1].acceleration)
                    elif(self.current_Image_Name == "man_Left"):
                        move[1][1].Velocity(-self.bomb_Kick_Power, 0)
                        move[1][1].Acceleration(move[1][1].acceleration, 0)
                    elif(self.current_Image_Name == "man_Up"):
                        move[1][1].Velocity(0, -self.bomb_Kick_Power)
                        move[1][1].Acceleration(0, move[1][1].acceleration)
                    elif(self.current_Image_Name == "man_Right"):
                        move[1][1].Velocity(self.bomb_Kick_Power, 0)
                        move[1][1].Acceleration(-move[1][1].acceleration, 0)
                    move[1][1].t_Old = time.clock()
            self.stop_Run()

    def spawn_Bomb(self, map_Object):
        if(self.bomb_Count > 0 and map_Object.tile_At([self.get_Sprite_Center()])[0]["Bomb"] == False):
            pos = self.get_Sprite_Center()
            bomb = self.bomb_Factory.New(map_Object.tile_At([pos])[0]["Position"], False, self.scale, 2.5)
            bomb.Alphe_Con()
            bomb.set_Owner(self)
            self.bomb_List.add(bomb)
            # add bomb to map
            map_O = map_Object.tile_At([pos])
            map_O[0]["Bomb"] = True
            map_O[0]["Bomb_Owner"] = self
            map_O[0]["Bomb_Object"] = bomb
            self.bomb_Movable = True
            self.bomb_Count -= 1
            self.bomb_Next_Replenishment = time.clock() + self.bomb_Replenish_Rate
            self.bomb_Start_Replenishment = True

    def update(self, map_Object):
        t = time.clock()
        dt = t - self.oldt
        if(self.run == True):
            # update run animations
            self.incroment_Animation_Index(t)
            # if the movment is grater then 1 pixle update movments
            if(1 * self.speed * dt > 1):
                if(self.current_Image_Name == "man_Down"):
                    self.Velocity(0, self.speed)
                elif(self.current_Image_Name == "man_Left"):
                    self.Velocity(-self.speed, 0)
                elif(self.current_Image_Name == "man_Up"):
                    self.Velocity(0, -self.speed)
                elif(self.current_Image_Name == "man_Right"):
                    self.Velocity(self.speed, 0)
                self.update_Positions(dt, map_Object)
                # reset the time applied to delta t
                self.oldt = t
        # update bombs
        if(self.spawn_B == True):
            self.spawn_Bomb(map_Object)
            self.spawn_B = False
        # Replenish bomb_List
        if (t > self.bomb_Next_Replenishment and self.bomb_Start_Replenishment == True):
            self.bomb_Count += 1
            self.bomb_Start_Replenishment = False
        return self.bomb_List
