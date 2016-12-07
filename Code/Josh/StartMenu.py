import pygame
import os
import sys
path = os.path.realpath(__file__)
for i in range(0, 1):
    path = os.path.dirname(path)
path_Josh = path + "/Josh"
sys.path.insert(0, path_Josh)
import button

class StartMenu :
    def __init__(self, file_location, screen_Size):
        self.state = 0
        self.addButton(screen_Size)
        self.background = pygame.image.load(file_location)
        self.background = pygame.transform.scale(self.background, (screen_Size[0], screen_Size[1]))


    def addButton(self, screen_Size) :
        self.playButton = button.Button(screen_Size[0] - ((screen_Size[0] / 4) * 2.9), screen_Size[1] - ((screen_Size[1] / 3) * 2), screen_Size[0] / 2, screen_Size[1] / 7, (0, 150, 0), "Play", (150, 150, 0))
        self.exitButton = button.Button(screen_Size[0] - ((screen_Size[0] / 4) * 2.9), screen_Size[1] - ((screen_Size[1] / 3) * 1.5), screen_Size[0] / 2, screen_Size[1] / 7, (150, 0, 0), "Exit", (150, 150, 0))
        self.player1 = button.Button(screen_Size[0] - ((screen_Size[0] / 4) * 2.9), screen_Size[1] - ((screen_Size[1] / 3) * 2.0), screen_Size[0] / 7, screen_Size[1] / 8, (0,150, 0), "Comp", (150,0,0))
        self.player1.textAlignmentLeft()
        self.player2 = button.Button(screen_Size[0] - ((screen_Size[0] / 4) * 1.9), screen_Size[1] - ((screen_Size[1] / 3) * 2.0), screen_Size[0] / 7, screen_Size[1] / 8, (0,150, 0), "Comp", (150,0,0))
        self.player2.textAlignmentLeft()
        self.player3 = button.Button(screen_Size[0] - ((screen_Size[0] / 4) * 2.9), screen_Size[1] - ((screen_Size[1] / 3) * 1.5), screen_Size[0] / 7, screen_Size[1] / 8, (0,150, 0), "Comp", (150,0,0))
        self.player3.textAlignmentLeft()
        self.player4 = button.Button(screen_Size[0] - ((screen_Size[0] / 4) * 1.9), screen_Size[1] - ((screen_Size[1] / 3) * 1.5), screen_Size[0] / 7, screen_Size[1] / 8, (0,150, 0), "Comp", (150,0,0))
        self.player4.textAlignmentLeft()
        self.confirmButton = button.Button(screen_Size[0] - ((screen_Size[0] / 4) * 3.1), screen_Size[1] - ((screen_Size[1] / 3) * 1), screen_Size[0] / 2, screen_Size[1] / 7, (0, 150, 0), "Play", (150, 150, 0))
        self.backButton = button.Button(screen_Size[0] - ((screen_Size[0] / 4) * 4.0), screen_Size[1] - ((screen_Size[1] / 3) * 0.4), screen_Size[0] / 7, screen_Size[1] / 8, (150, 0, 0), "Back", (150, 150, 0))
        self.backButton.textAlignmentLeft()
        self.controllerCount = [False, False, False, False]   
        self.player1_Controller = button.Button(screen_Size[0] - ((screen_Size[0] / 4) * 2.9), screen_Size[1] - ((screen_Size[1] / 3) * 2.0), screen_Size[0] / 7, screen_Size[1] / 8, (150,150, 150), "Player", (150,0,0))
        self.player1_Controller.textAlignmentLeft()
        self.player2_Controller = button.Button(screen_Size[0] - ((screen_Size[0] / 4) * 1.9), screen_Size[1] - ((screen_Size[1] / 3) * 2.0), screen_Size[0] / 7, screen_Size[1] / 8, (150,150, 150), "Player", (150,0,0))
        self.player2_Controller.textAlignmentLeft()
        self.player3_Controller = button.Button(screen_Size[0] - ((screen_Size[0] / 4) * 2.9), screen_Size[1] - ((screen_Size[1] / 3) * 1.5), screen_Size[0] / 7, screen_Size[1] / 8, (150,150, 150), "Player", (150,0,0))
        self.player3_Controller.textAlignmentLeft()
        self.player4_Controller = button.Button(screen_Size[0] - ((screen_Size[0] / 4) * 1.9), screen_Size[1] - ((screen_Size[1] / 3) * 1.5), screen_Size[0] / 7, screen_Size[1] / 8, (150,150, 150), "Player", (150,0,0))
        self.player4_Controller.textAlignmentLeft()


        
      #  print(screen_Size)
    def keyPress(self, pos) :
        if self.playButton.get_Rect().collidepoint(pos):
            return "playButton" 
        elif self.exitButton.get_Rect().collidepoint(pos):
            return "exitButton"
        elif self.confirmButton.get_Rect().collidepoint(pos) :
            return "confirmButton"
        elif self.backButton.get_Rect().collidepoint(pos) :
            return "backButton"
        else :
            return None

    def controllers(self, number) :
        self.controllerCount = [False, False, False, False]
        for i in range(0, number) :
            self.controllerCount[i] = True
                   

    def update(self, display) :
        display.blit(self.background, (0, 0))
        if self.state == 0 :     
            self.playButton.update(display)
            self.exitButton.update(display)
        elif self.state == 1:
            
            if self.controllerCount[0] == False :
                self.player1.update(display)
            else :
                self.player1_Controller.update(display)
                
            if self.controllerCount[1] == False :
                self.player2.update(display)
            else :
                self.player2_Controller.update(display)
                
            if self.controllerCount[2] == False :
                self.player3.update(display)   
            else :
                self.player3_Controller.update(display)
                
            if self.controllerCount[3] == False :
                self.player4.update(display)
            else :
                self.player4_Controller.update(display)
                
           # self.player2.update(display)
           # self.player3.update(display)
           # self.player4.update(display)
            self.confirmButton.update(display)
            self.backButton.update(display)

    
