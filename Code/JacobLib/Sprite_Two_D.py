# import pygames
import random
import os
import pygame
from pygame import draw, display, rect, sprite

from Dic import Dic_Search
from Error_Report import Report_Error


class Sprite_Two_Dimensions(pygame.sprite.Sprite):
    "Base sprite class form which all custom sprite inherit"

    def __init__(self, spawn_Area=(0, 0, 0, 0), fixed=False):
        # Call the parent class (Sprite) constructor
        super(Sprite_Two_Dimensions, self).__init__()
        # set default values if None is passed
        # Area where sprites can spawn
        if(spawn_Area == None):
            self.spawn_Area = (0, 0, 0, 0)
        else:
            self.spawn_Area = spawn_Area

        # sets if the sprite can be moved
        if(fixed == None):
            self.fixed = False
        else:
            self.fixed = fixed

        self.position_x = 0
        self.position_y = 0
        self.velocity_x = 0
        self.velocity_y = 0
        self.acceleration_x = 0
        self.acceleration_y = 0
        # Stores all loaded images
        self.images = []
        self.image = None
        self.rect = None

    def Position(self, *pos):
        if(type(pos) == tuple and len(pos) == 2 and type(pos[0]) == int):
            # chescks the value senf is a tuble and tue tuple has only 2 values witht first value being an int
            # this makes sure only the first tupe of format (x,y) is used
            self.position_x, self.position_y = pos[0], pos[1]

        return (self.position_x, self.position_y)

    def Velocity(self, *vel):
        if(type(vel) == tuple and len(vel) == 2 and type(vel[0]) == int):
            # chescks the value senf is a tuble and tue tuple has only 2 values witht first value being an int
            # this makes sure only the first tupe of format (x,y) is used
            self.velocity_x, self.velocity_y = vel[0], vel[1]

        return (self.velocity_x, self.velocity_y)

    def Acceleration(self, *acc):
        if(type(acc) == tuple and len(acc) == 2 and type(acc[0]) == int):
            # chescks the value senf is a tuble and tue tuple has only 2 values witht first value being an int
            # this makes sure only the first tupe of format (x,y) is used
            self.acceleration_x, self.acceleration_y = acc[0], acc[1]

        return (self.acceleration_x, self.acceleration_y)

    def Locational_Data(self):
        return (self.Position(), self.Velocity(), self.Acceleration())

    def Load_Image(self, file_Path=None, scale=None, x_Res=None):
        if(file_Path == None):
            Report_Error("No file path given for %s" % (__name__))
            return

        try:
            # load image then resize te image
            img = pygame.image.load(os.path.join(file_Path))
        except pygame.error:
            Report_Error("%s is an invalid file path" % (file_Path))
            return None

        rect = img.get_rect()
        # check x_res
        if(x_Res):
            scale = self.rect[2] / self.x_res + scale
        elif(type(scale) == tuple):
            scale = random.randrange(scale[0], scale[1])
        elif(scale == None or scale[0] == 0 or scale[1]):
            Report_Error("No valid scale for 2D Sprite")
            return None

        # resize the image then get new size
        try:
            image = pygame.transform.scale(img, (rect[2] / scale, rect[3] / scale))
        except ZeroDivisionError:
            Report_Error("Scale was equal to 0 for 2D sprite")
            return

        self.images.append(image)

    def Set_Image(self, img_Num):
        if(len(self.images) >= img_Num):
            self.image = self.images[img_Num]
            self.rect = self.image.get_rect()
            self.rect[0], self.rect[1] = self.position_x, self.position_y
        else:
            Report_Error("%s is not an image in Sprite.images" % (img_Num))

    def Set_Spawn(self):
        try:
            self.position_x = random.randrange(self.spawn_Area[0], self.spawn_Area[1])
            self.position_y = random.randrange(self.spawn_Area[2], self.spawn_Area[3])
            self.rect[0], self.rect[1] = self.position_x, self.position_y
        except ValueError:
            Report_Error("%s is am invalid spawn value" % (str(self.spawn_Area)))

    def Detect_Collitions(Collitions_Sprite_Group, Own_Sprite_Group):
        pass
