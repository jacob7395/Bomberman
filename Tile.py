import pygame

class Tile :
    tile_ID = 0;
    is_Walkable = True;
    texture = "";
    x = 0;
    y = 0;
    data_File_Path = "Map.txt"

    def __init__ (self, tileDimensions, tileIndex, background, walkable) :
        self.is_Walkable = walkable;
        self.tileWidth = tileDimensions[0]
        self.tileHeight = tileDimensions[1]
        self.tileIndex = tileIndex;
        self.x = tileIndex[0] * self.tileWidth
        self.y = tileIndex[1] * self.tileHeight
        self.texture = background;

    def setBG(self, bg) :
        texture = bg;

    def getBG(self) :
        return self.texture;
    
    def setWalkable(self, walkable) :
        self.is_Walkable = walkable;
        
    def getWalkable(self) :
        return self.is_Walkable;   
    
    def get_Rect(self) :
        return [self.x, self.y, self.tileWidth , self.tileHeight]
    
    def get_Rect_X(self) :
        return self.x;
    
    def get_Rect_Y(self) :
        return self.y;

    def updateTile(self, tileWidth, tileHeight) :
        self.tileWidth = tileWidth;
        self.tileHeight = tileHeight;
        self.x = self.tileIndex[0] * self.tileWidth
        self.y = self.tileIndex[1] * self.tileHeight    
