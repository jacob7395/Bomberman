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

        for assets in asset_List:
            # check all asses propertys exist
            l = ["s_Res", "s_Start", "s_End", "p_Path", "s_Scale", "s_Flip"]
            for tag in l:
                if(Dic_Search(tag, assets) == False):
                    assets[tag] = None
            # Load Assets in provides list
            self.Load_Image(assets["p_Path"], assets["s_Res"], assets["s_Scale"], assets["s_Start"], assets["s_End"], assets["s_Flip"])

    def Position(self, *pos):
        """Function to return and set position if passes a value."""
        if(type(pos) == tuple and len(pos) == 2 and type(pos[0]) == int):
            # chescks the value senf is a tuble and tue tuple has only 2 values witht first value being an int
            # this makes sure only the first tupe of format (x,y) is used
            self.position_x, self.position_y = pos[0], pos[1]

        return (self.position_x, self.position_y)

    def Velocity(self, *vel):
        """Function to return and set velocity if passes a value."""
        if(type(vel) == tuple and len(vel) == 2 and type(vel[0]) == int):
            # chescks the value senf is a tuble and tue tuple has only 2 values witht first value being an int
            # this makes sure only the first tupe of format (x,y) is used
            self.velocity_x, self.velocity_y = vel[0], vel[1]

        return (self.velocity_x, self.velocity_y)

    def Acceleration(self, *acc):
        """Function to return and set acceleration if passes a value."""
        if(type(acc) == tuple and len(acc) == 2 and type(acc[0]) == int):
            # chescks the value senf is a tuble and tue tuple has only 2 values witht first value being an int
            # this makes sure only the first tupe of format (x,y) is used
            self.acceleration_x, self.acceleration_y = acc[0], acc[1]

        return (self.acceleration_x, self.acceleration_y)

    def Locational_Data(self):
        """Returnes values for Position,Velocity,Acceleration in a tuple."""
        return (self.Position(), self.Velocity(), self.Acceleration())

    def Load_Image(self, file_Path, resolution, sprite_Scale, sprite_Start, sprite_End, sprite_Flip):
        try:
            # Attempt to load sprite sheet
            self.sheet = pygame.image.load(file_Path)
        except pygame.error:
            Report_Error("%s is an invalid file path" % (file_Path))
            return None

        if(sprite_End == None):
            range_x = 1
            range_y = 1
        else:
            range_x = sprite_End[0] - sprite_Start[0] + 1
            range_y = sprite_End[1] - sprite_Start[1] + 1

        rectange = resolution[0] * sprite_Start[0], resolution[1] * sprite_Start[1], resolution[0] * range_x, resolution[1] * range_y

        rect = pygame.Rect(rectange)
        image = pygame.Surface(rect.size)
        image.blit(self.sheet, (0, 0), rect)
        # Scale the image if the sacle property exitst
        if(sprite_Scale != None):
            image = pygame.transform.scale(image, (int(resolution[0] * sprite_Scale), int(resolution[1] * sprite_Scale)))
        # Flip the sprite if the property exitst
        if(sprite_Flip != None):
            image = pygame.transform.flip(image, sprite_Flip[0], sprite_Flip[1])

        self.images.append(image)

    def Set_Image(self, img_Num):
        if(len(self.images) >= img_Num):
            self.img_Num = img_Num
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

    def Scale_Imgs(self, scale):
        """Scale all the images by the value passed."""
        for x in range(len(self.images)):
            self.images[x] = pygame.transform.scale(self.images[x], (scale, scale))
        if(self.img_Num != None):
            self.Set_Image(self.img_Num)

    def Detect_Collitions(Collitions_Sprite_Group, Own_Sprite_Group):
        pass
