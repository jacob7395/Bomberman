import sys, pygame, Map
from pygame.locals import *
pygame.init()

gameWidth = 1024;
gameHeight = 768;
gameDisplay = pygame.display.set_mode((gameWidth, gameHeight),HWSURFACE|DOUBLEBUF|RESIZABLE)
pygame.display.set_caption('Bomberman')
isGameRunning = True;
gameFont = pygame.font.SysFont(None, 25)
FPSColour = (0, 255, 0)
clock = pygame.time.Clock()

map = Map.Map(20, 15, gameWidth, gameHeight)

while isGameRunning:
    for event in pygame.event.get():
        if event.type == pygame.QUIT :  
            isGameRunning = False;
            break
        if event.type==VIDEORESIZE:
            gameDisplay=pygame.display.set_mode(event.dict['size'],HWSURFACE|DOUBLEBUF|RESIZABLE)
            displayInfo = pygame.display.Info()
            gameWidth = displayInfo.current_w
            gameHeight = displayInfo.current_h
            map.updateGameWindow(gameWidth, gameHeight);
            
    map.renderMap(gameDisplay); 
    clock.tick()
    fpsText = gameFont.render("FPS: " + str(int(clock.get_fps())), True, FPSColour); 
    gameDisplay.blit(fpsText, [10, 10], None);
    
  #  pygame.display.flip()
    pygame.display.update();
    # Little difference between the two
    
pygame.quit()

    



