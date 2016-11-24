import pygame
import constants

class SpriteSheet(object):
 
    def __init__(self, file_name):
        self.sprite_sheet = pygame.image.load(file_name).convert()
		
    def GetImage(self, x, y, width, height):
        image = pygame.Surface([width, height]).convert()
   #     pygame.Surface.convert_alpha(image);
        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
        return image

		
		
