# -----------------------------------------------
# Load functions and calsses form remote locations
import random
import os
import time

import pygame
from pygame import draw, display, rect, mouse
from pygame.sprite import groupcollide
# -----------------------------------------------
# section for Pygame initalization
# Define some colors
BLACK = (0,   0,   0)
WHITE = (255, 255, 255)
GREEN = (0, 255,   0)
RED = (255,   0,   0)
# default pygame init functions
pygame.init()
# Set the width and height of the screen [width, height]
screen_Size = (1280, 720)
screen = display.set_mode(screen_Size)
scree_Fullscreen = True
# Define spawn Area
spawn_Area = (-100, -50, 0, screen_Size[1])
# Set game window
pygame.display.set_caption("Bomberman")
# loop until the user clicks the close button.
done = False
# used to manage how fast the screen updates
clock = pygame.time.Clock()
# pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP])
# -------- Main Program Loop -----------
while not done:
    # --- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    # --- Game logic should go here
    # Calculate collitions with Bman
    screen.fill(BLACK)
    # --- Drawing code should go here

    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
    # --- Limit to 60 frames per second
    clock.tick(60)
    print ("fps:" + str(clock.get_fps()))

# Close the window and quit.
pygame.quit()
