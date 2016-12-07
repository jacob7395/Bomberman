import pygame

class Button:
    
    def __init__(self, x, y, width, height, buttoncolour, text, textcolour):
        self.buttonColour = buttoncolour
        self.textColour = textcolour
        self.text = text
        self.height = height
        self.width = width
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, width, height)
        self.gameFont = pygame.font.SysFont(None, 45)
        self.textPos = [self.x + (self.width / 2.5), self.y + (self.height / 4)]
        
    def updateSize(self, x, y, width, height, text) :
        self.rect = pygame.Rect(x, y, width, height)
    
    def get_Rect(self) :
        return self.rect

    def textAlignmentLeft(self) :
        self.textPos = self.textPos = [self.x, self.y + (self.height / 4)]

    def update(self, display) :
       # print("test")
        pygame.draw.rect(display, self.buttonColour, self.rect);
        text = self.gameFont.render(self.text, True, self.textColour);
        display.blit(text, self.textPos, None);
