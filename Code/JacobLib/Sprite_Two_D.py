# import pygames
import random
import os
import pygame
from pygame import draw, display, rect, sprite

from Dic import Dic_Search
from Error_Report import Report_Error


class Sprite_Two_Dimensions(pygame.sprite.Sprite):
    """Base sprite class form which all custom sprite inherit."""

    def __init__(self, spawn_Area=(0, 0), fixed=False, asset_List=[]):
        """Init Function."""
        # Call the parent class (Sprite) constructor
        super(Sprite_Two_Dimensions, self).__init__()
        # set default values if None is passed
        # Area where sprites can spawn
        if(spawn_Area == None):
            self.spawn_Area = (0, 0)
        else:
            self.spawn_Area = spawn_Area

        # sets if the sprite can be moved
        if(fixed == None):
            self.fixed = False
        else:
            self.fixed = fixed

        self.position_x = spawn_Area[0]
        self.position_y = spawn_Area[1]
        self.velocity_x = 0
        self.velocity_y = 0
        self.acceleration_x = 0
        self.acceleration_y = 0
        # Stores all loaded images
        self.images = []
        self.image = None
        self.rect = None
        # load asset as instructed by the given dictunery
        for assets in asset_List:
            # check all asses propertys exist
            l = ["s_Res", "s_Start", "s_End", "p_Path",
                 "s_Scale", "s_Flip", "s_Annimated_Len",
                 "s_Name"]
            for tag in l:
                if(Dic_Search(tag, assets) == False):
                    assets[tag] = None
            if(assets["s_Name"] != None and type(self.images) != dict):
                self.images = {}

            if(assets["s_Annimated_Len"] == None):
                # Load Assets in provides list
                self.Load_Image(assets["p_Path"], assets["s_Res"], assets["s_Scale"], assets[
                                "s_Start"], assets["s_End"], assets["s_Flip"], assets["s_Name"])
            else:
                self.images.update({assets["s_Name"]: []})
                for x in range(0, assets["s_Annimated_Len"]):
                    self.Load_Image(assets["p_Path"], assets["s_Res"], assets["s_Scale"], assets[
                                    "s_Start"], assets["s_End"], assets["s_Flip"], assets["s_Name"], x)

    def Position(self, *pos):
        """Function to return and set position if passes a value."""
        if(type(pos) == tuple and len(pos) == 2 and type(pos[0]) == int):
            # chescks the value senf is a tuble and tue tuple has only 2 values witht first value being an int
            # this makes sure only the first tupe of format (x,y) is used
            self.position_x, self.position_y = pos[0], pos[1]

        return (self.position_x, self.position_y)

    def Incroment_Position(self, pos):
        """Function that incroments the position by passes valuse."""
        if(type(pos) == tuple and len(pos) == 2):
            # chescks the value senf is a tuble and tue tuple has only 2 values witht first value being an int
            # this makes sure only the first tupe of format (x,y) is used
            self.position_x += pos[0]
            self.position_y += pos[1]

    def Velocity(self, *vel):
        """Function to return and set velocity if passes a value."""
        if(type(vel) == tuple and len(vel) == 2):
            # chescks the value senf is a tuble and tue tuple has only 2 values witht first value being an int
            # this makes sure only the first tupe of format (x,y) is used
            self.velocity_x, self.velocity_y = vel[0], vel[1]
        self.v_Start = (self.velocity_x, self.velocity_y)
        return (self.velocity_x, self.velocity_y)

    def Acceleration(self, *acc):
        """Function to return and set acceleration if passes a value."""
        if(type(acc) == tuple and len(acc) == 2):
            # chescks the value senf is a tuble and tue tuple has only 2 values witht first value being an int
            # this makes sure only the first tupe of format (x,y) is used
            self.acceleration_x, self.acceleration_y = acc[0], acc[1]

        return (self.acceleration_x, self.acceleration_y)

    def Locational_Data(self):
        """Returnes values for Position,Velocity,Acceleration in a tuple."""
        return (self.Position(), self.Velocity(), self.Acceleration())

    def Load_Image(self, file_Path, resolution, sprite_Scale, sprite_Start, sprite_End, sprite_Flip, name, img_Num=0):
        """loads images as instructed by the propertys passed"""
        # Check the passed sprite sheet is valid
        try:
            # Attempt to load sprite sheet
            self.sheet = pygame.image.load(file_Path)
        except pygame.error:
            Report_Error("%s is an invalid file path" % (file_Path))
            return None
        # Check the size of the wanted sprite
        if(sprite_End == None):
            range_x = 1
            range_y = 1
        else:
            # if there is a sprite end set the wanted x,y range
            range_x = sprite_End[0] - sprite_Start[0] + 1
            range_y = sprite_End[1] - sprite_Start[1] + 1
        # make the rectange for the
        rectange = resolution[0] * sprite_Start[0] + resolution[0] * img_Num, resolution[
            1] * sprite_Start[1], resolution[0] * range_x, resolution[1] * range_y

        rect = pygame.Rect(rectange)
        image = pygame.Surface(rect.size)
        image.blit(self.sheet, (0, 0), rect)
        # Scale the image if the sacle property exitst
        if(sprite_Scale != None):
            image = pygame.transform.scale(image, (sprite_Scale, sprite_Scale))
        # Flip the sprite if the property exitst
        if(sprite_Flip != None):
            image = pygame.transform.flip(
                image, sprite_Flip[0], sprite_Flip[1])

        if(name == None):
            self.images.append(image)
        else:
            self.images[name].append(image)

    def Set_Image(self, img_Num):
        if(type(img_Num) == str):
            self.img_Name = img_Num
            self.image = self.images[img_Num][self.index]
            self.rect = self.image.get_rect()
            self.rect[0], self.rect[1] = self.position_x, self.position_y
        elif(len(self.images) >= img_Num):
            self.img_Num = img_Num
            self.image = self.images[img_Num]
            self.rect = self.image.get_rect()
            self.rect[0], self.rect[1] = self.position_x, self.position_y
        else:
            Report_Error("%s is not an image in Sprite.images" % (img_Num))
        self.Alphe_Con()

    def Set_Spawn(self):
        try:
            self.position_x = random.randrange(
                self.spawn_Area[0], self.spawn_Area[1])
            self.position_y = random.randrange(
                self.spawn_Area[2], self.spawn_Area[3])
            self.rect[0], self.rect[1] = self.position_x, self.position_y
        except ValueError:
            Report_Error("%s is an invalid spawn value" %
                         (str(self.spawn_Area)))

    def Scale_Imgs(self, scale):
        """Scale all the images by the value passed."""
        for x in range(len(self.images)):
            self.images[x] = pygame.transform.scale(
                self.images[x], (scale, scale))
        if(self.img_Num != None):
            self.Set_Image(self.img_Num)

    def Alphe_Con(self, color_Key=(0, 0, 0)):
        if(type(self.images) != dict):
            for image in self.images:
                image.set_colorkey(color_Key, pygame.RLEACCEL)

        if(self.image):
            self.image.set_colorkey(color_Key, pygame.RLEACCEL)

    def get_Collision_Coners(self):
        pos = self.Position()
        cornors = []
        cornors.append((pos[0] + self.collition_Offset,
                        pos[1] + self.collition_Offset))
        cornors.append((pos[0] + self.collition_Offset,
                        pos[1] + (self.scale - self.collition_Offset)))
        cornors.append(
            (pos[0] + (self.scale - self.collition_Offset), pos[1] + self.collition_Offset))
        cornors.append((pos[0] + (self.scale - self.collition_Offset),
                        pos[1] + (self.scale - self.collition_Offset)))
        return cornors

    def get_Sprite_Center(self):
        corners = self.get_Collision_Coners()
        pos_One = corners[0]
        pos_Two = corners[3]
        return ((pos_One[0] + pos_Two[0]) / 2, (pos_One[1] + pos_Two[1]) / 2)

    def incroment_Animation_Index(self, t):
        if(t > self.init_Time + self.change_Time):
            self.index += 1
            # if index is out of range loop animation
            if(self.index > len(self.images[self.current_Image_Name]) - 1):
                self.index = 0
            # reset timer
            self.init_Time = t
            # update the current image
            self.Set_Image(self.current_Image_Name)
