import sys, Tile, pygame
pygame.init();

from SpriteSheet import SpriteSheet

class Map:
    
    TILES_DATA_FILE = "Data/Tiles.txt"
    MAP_DATA_FILE = "Data/Map.txt"

    def __init__(self, mapWidth=0, mapHeight=0, screenWidth=0, screenHeight = 0) :
        self.spriteSheet = SpriteSheet("Sprites/SpriteSheet.png")  
        self.tileWidth = (screenWidth / mapWidth)
        self.tileHeight = (screenHeight / mapHeight)
        self.tiles = [ [Tile.Tile([self.tileWidth, self.tileHeight], [i, j] ,"Null", True) for i in range(mapHeight) ] for j in range(mapWidth)]
        self.getTileInformation();
        self.getMapData()
        self.mapWidth = mapWidth;
        self.mapHeight = mapHeight;
        self.screenWidth = screenWidth;
        self.screenHeight = screenHeight;                  

    def getTileInformation(self) :
        self.mapTiles = list();
        with open(self.TILES_DATA_FILE, 'r') as f:
            next(f)     
            for row in f :
                values = list();
                for col in row.split() :
                    values.append(col);
                self.mapTiles.append(values);
        # Need to add some error handling here later
            
    def getMapData(self) :    
            with open(self.MAP_DATA_FILE, 'r') as file:
                 for i, row in enumerate(file) :
                    for j, col in enumerate(row.strip()):
                        imageRect = self.spriteSheet.GetImage(int(self.mapTiles[int(col)][3]), int(self.mapTiles[int(col)][4]), 16, 16)
                        self.tiles[i][j] = Tile.Tile(self.calculateDimensions(i, j), [i, j], imageRect, True);
        # Need to add some error handling here later

    def updateGameWindow(self, screenWidth=0, screenHeight=0) :
        self.screenWidth = screenWidth;
        self.screenHeight = screenHeight;
        self.tileWidth = int(screenWidth / self.mapWidth);
        self.tileHeight = int(screenHeight / self.mapHeight);
        for i, row in enumerate(self.tiles) :
            for j, col in enumerate(row) :
                col.updateTile(self.tileWidth, self.tileHeight);
                							    			    	       
    def renderMap(self, gameDisplay) :
        for i, row in enumerate(self.tiles) :
            for j, col in enumerate(row) :
                Image = pygame.transform.scale(self.tiles[i][j].getBG(), (self.tileWidth, self.tileHeight))
                gameDisplay.blit(Image, self.tiles[i][j].get_Rect())
                
    def calculateDimensions(self, x, y) :
        return [(x * self.tileWidth), (y *  self.tileHeight)];                
