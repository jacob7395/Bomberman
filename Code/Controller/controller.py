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
        self.states = {'RIGHT': 0, 'LEFT': 0, 'UP': 0, 'DOWN': 0}
        self.key_Change = None

    def EventManager(self):
        pygame.event.pump()
        # update the button states for lynix
        if(self.system == "Darwin"):
            self.states = {'A': self.player.get_button(11)}

            movmentStates = {'UP': self.player.get_button(0),
                             'DOWN': self.player.get_button(1),
                             'LEFT': self.player.get_button(2),
                             'RIGHT': self.player.get_button(3)}  # return true or false of buttons
        # update button state for windows
        elif(self.system == "Windows"):
            # get the a button state
            self.states.update({'A': self.player.get_button(0)})
            # load the hat values
            hat_Values = self.player.get_hat(0)
            # holds the current states
            movmentStates = {'RIGHT': 0, 'LEFT': 0, 'UP': 0, 'DOWN': 0}
            # rad the had values
            if(hat_Values[0] == 1):
                movmentStates.update({'RIGHT': 1, 'LEFT': 0})
            elif(hat_Values[0] == -1):
                movmentStates.update({'RIGHT': 0, 'LEFT': 1})

            if(hat_Values[1] == 1):
                movmentStates.update({'UP': 1, 'DOWN': 0})
            elif(hat_Values[1] == -1):
                movmentStates.update({'UP': 0, 'DOWN': 1})
        # cheack for change in states
        for key in movmentStates.keys():
            # if there is a chnge in states set it to the last key change
            if(self.states[key] != movmentStates[key] and movmentStates[key] == 1):
                self.last_Key_Change = key
                self.bomberman.stop_running()
        # finaly update the movment states
        self.states.update(movmentStates)

        self.bomberman_Update()

    def bomberman_Update(self):
        # update bomberman direction
        number_Of_Directions_Pressed = 0
        # for each direction
        for directon in self.directions:
            # check if the direction is pressed if so add to count
            number_Of_Directions_Pressed += self.states[directon]
            # check if the button state is true and if the bomberman ia running
            if(self.states[directon] == True and self.bomberman.running == False):
                # if set the direction to the lates keychange
                if(self.key_Change != None):
                    self.bomberman.current_Image_Name = self.last_Key_Change
                    # then reset the key_Change
                    self.key_Change = None
                else:
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
