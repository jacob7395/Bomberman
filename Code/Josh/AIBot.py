import pygame, Dijkstra

class AIBot :

    def __init__(self,y,x):
        self.pathFinding = Dijkstra.Dijkstra(x, y)
        self.hasPath = False;

    def isSeeking(self) :
        return self.hasPath
        
    def getPath(self,currentPosition, map) :
        if self.hasPath == False :
            for i, row in enumerate(map):
                for j, tile in enumerate(row):
                    if(tile['Tile'] == 'b') :
                        position = tile.get("Position")
                        curPos = (position[0] / 34, position[1] / 34)
                        self.path = self.pathFinding.getPath([currentPosition[0], currentPosition[1]], [curPos[0],curPos[1]]);
                        if self.path is not None :
                                self.movements = int(len(self.path))
                                self.currentMove = 0
                                self.isSeeking = True
                                self.hasPath = True
                                return self.path
            return None
            
    def setList(self, lst) :
        self.map = list;
        for rows in lst:
            for tile in rows:
                if(tile['Tile'] == 'w'):
                    position = tile.get("Position")
                    newPos = (position[0] / 34, position[1] / 34)
                    self.pathFinding.makeMoveable(newPos[0], newPos[1],tile.get("Movable"))


    def runAway(self) :
        print("Run away now!")
                
    def update(self, currentPosition) :
        if self.path is not None :
            targetPosition = self.path[self.currentMove]
            if targetPosition is not currentPosition :
                minus = [targetPosition[0] - currentPosition[0],  targetPosition[1] - currentPosition[1]];
                if minus[1] < 0 :
                    return "UP"
                elif minus[0] > 0:
                    return "RIGHT"
                elif minus[1] > 0 :
                    return "DOWN"
                elif minus[1] < 0 :
                  return "LEFT"                    
                elif self.currentMove + 1 < int(len(self.path)) :
                    self.currentMove += 1
                else :              
                    print("Making bomb")
                    return "BOMB"
                    
            
        
        
