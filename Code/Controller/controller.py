import time
import pygame
import platform
from pygame import joystick


class controller_Object:

    def __init__(self, bomberman=None, controller_ID=None):
        self.system = platform.system()
        self.bomberman = bomberman
        self.controller_ID = controller_ID
        self.player = joystick.Joystick(self.controller_ID)
        self.player.init()
        self.bomb_Spawned = False
        self.pressed = {}
        self.directions = ["UP", "DOWN", "LEFT", "RIGHT"]
        self.press_Count = 0

    def EventManager(self):
        pygame.event.pump()
        # update the button states
        if(self.system == "Darwin"):
            self.states = {
                'A': self.player.get_button(11),
                'UP': self.player.get_button(0),
                'DOWN': self.player.get_button(1),
                'LEFT': self.player.get_button(2),
                'RIGHT': self.player.get_button(3)}  # return true or false of buttons
        elif(self.system == "Windows"):
            self.states = {
                'A': self.player.get_button(0)}
            hat_Values = self.player.get_hat(0)

            self.states.update({'RIGHT': 0, 'LEFT': 0, 'UP': 0, 'DOWN': 0})

            if(hat_Values[0] == 1):
                self.states.update({'RIGHT': 1, 'LEFT': 0})
            elif(hat_Values[0] == -1):
                self.states.update({'RIGHT': 0, 'LEFT': 1})

            if(hat_Values[1] == 1):
                self.states.update({'UP': 1, 'DOWN': 0})
            elif(hat_Values[1] == -1):
                self.states.update({'UP': 0, 'DOWN': 1})

        for directon in self.directions:
            if(self.states[directon] == True):
                self.pressed.update({directon: self.press_Count})
                self.press_Count = len(self.pressed)
            else:
                try:
                    self.pressed.remove(directon)
                    self.press_Count -= 1
                except:
                    pass
        self.bomberman_Update()

    def bomberman_Update(self):
        # update bomberman direction
        number_Of_Directions_Pressed = 0
        for directon in self.directions:
            number_Of_Directions_Pressed += self.states[directon]
            if(self.states[directon] == True and self.bomberman.running == False):
                self.bomberman.current_Image_Name = directon
                self.bomberman.begin_running()
                number_Of_Directions_Pressed += 1
        if(self.states["A"] == True and self.bomb_Spawned == False):
            self.bomb_Spawned = True
            self.bomberman.spawn_B = True
        elif(self.states["A"] == False and self.bomb_Spawned == True):
            self.bomb_Spawned = False
        if(number_Of_Directions_Pressed == 0 and self.bomberman.running == True):
            self.bomberman.stop_running()
