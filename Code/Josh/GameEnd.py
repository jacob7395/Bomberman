import pygame
import os
import sys
path = os.path.realpath(__file__)
for i in range(0, 1):
    path = os.path.dirname(path)
path_Josh = path + "/Josh"
sys.path.insert(0, path_Josh)
import button


class GameEnd:

    def __init__(self, file_location, screen_Size):
        self.addButton(screen_Size)
        self.background = pygame.image.load(file_location)
        self.background = pygame.transform.scale(self.background, (screen_Size[0], screen_Size[1]))

    def addButton(self, screen_Size):
        self.mainMenuButton = button.Button(screen_Size[0] - ((screen_Size[0] / 4) * 2.5), screen_Size[1] - ((screen_Size[1] / 3) * 1), screen_Size[0] / 4, screen_Size[1] / 7, (0, 150, 0), "Main Menu", (150, 150, 0))
        self.mainMenuButton.textAlignmentLeft()

    def keyPress(self, pos):
        if self.mainMenuButton.get_Rect().collidepoint(pos):
            return "Restart"
        else:
            return None

    def update(self, display):
        display.blit(self.background, (0, 0))
        self.mainMenuButton.update(display)
