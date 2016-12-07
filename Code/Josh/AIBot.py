import pygame
import Dijkstra
import random
import time


class AIBot:

    def __init__(self, y, x):
        self.pathFinding = Dijkstra.Dijkstra(x, y)
        self.runAwayPath = None
        self.reset()
        self.moving_Pos = None
        self.back_Path = []

    def isSeeking(self):
        return self.hasPath

    def reset(self):
        self.hasPath = False
        self.isRunning = False
        self.currentMoveRun = 0
        self.currentMoveRun = 0

    def findMan(self, me_Man, man_List, map):
        man = me_Man
        # get a list of all men withouth me in it
        man_List_Not_Me = []
        for not_Me in man_List:
            if(not_Me.ID != man.ID):
                man_List_Not_Me.append(not_Me)
        target = random.choice(man_List_Not_Me)
        # gets the tiles posion on the map object for the mans location
        pos = (map.pos_To_Location([man.get_Sprite_Center()]))[0]
        tagert_Pos = (map.pos_To_Location([target.get_Sprite_Center()]))[0]
        # get path with dicstra
        path = self.pathFinding.getPath(pos, tagert_Pos, map.map_Grid)
        self.path = path

    def setList(self, lst):
        self.map = lst
        for i, row in enumerate(lst):
            for j, tile in enumerate(row):
                if tile['Tile'] == 'w':
                    position = tile.get("Position")
                    newPos = (position[0] / 34, position[1] / 34)
                    self.pathFinding.makeMoveable(newPos[0], newPos[1], tile.get("Movable"))
                elif tile['Tile'] == 'b':
                    position = tile.get("Position")
                    newPos = (position[0] / 34, position[1] / 34)

    def inRange(self, posX, posY, width, height):
        if posX > 0 and posX < width and posY > 0 and posY < height:
            return True
        else:
            return False

    def runAway(self, position, notAllowedX):
        print("Run away now!")
        for i, row in enumerate(self.map):
            for j, tile in enumerate(row):
                if(tile['Tile'] == 'w') and self.inRange(i - 1, j - 1, len(row), len(tile)):
                    position = tile.get("Position")
                    curPos = (position[0] / 34, position[1] / 34)
                    while True:
                        rand = random.randrange(0, 3)
                        if rand == 0:
                            newPos = [curPos[0], curPos[1] - 1]
                            runAwayPath = self.pathFinding.getPathSecond(curPos, newPos, self.map)
                            print(runAwayPath)
                            if runAwayPath is not None:
                                self.runAwayPath = runAwayPath
                                self.isRunning = True
                                print(self.runAwayPath)
                                return runAwayPath
                        elif rand == 1:
                            newPos = [curPos[0] + 1, curPos[1]]
                            runAwayPath = self.pathFinding.getPathSecond(curPos, newPos, self.map)
                            if runAwayPath is not None:
                                self.runAwayPath = runAwayPath
                                self.isRunning = True
                                print(self.runAwayPath)
                                return runAwayPath
                        elif rand == 2:
                            newPos = [curPos[0], curPos[1] + 1]
                            runAwayPath = self.pathFinding.getPathSecond(curPos, newPos, self.map)
                            if runAwayPath is not None:
                                self.runAwayPath = runAwayPath
                                self.isRunning = True
                                print(self.runAwayPath)
                                return runAwayPath

                        elif rand == 3:
                            newPos = [curPos[0] - 1, curPos[1]]
                            runAwayPath = self.pathFinding.getPathSecond(curPos, newPos, self.map)
                            if runAwayPath is not None:
                                self.runAwayPath = runAwayPath
                                self.isRunning = True
                                print(self.runAwayPath)
                                return runAwayPath
                        else:
                            print("None")
        return str("None")

    def setlastPosition(self, position):
        self.lastPosition = position

    def getlastPosition(self):
        return self.lastPosition

    def update(self, display, map_Object, bomberman):
        if self.path is not None:
            if(bomberman.ID == 1):
                print(self.path)
            currentPosition = self.moving_Pos
            if(currentPosition == self.path[0]):
                self.back_Path.append(self.path.pop(0))

            if(type(self.path[0]) == bool):
                if(self.path[0] == True):
                    self.path = []
                    for x in range(0, 2):
                        self.path.append(self.back_Path[x])
                    self.path.append(False)
                    return str("BOOM")
                else:
                    return None

            targetPosition = self.path[0]

            # print("Target = {}, Position = {}".format(self.path, currentPosition))
            if currentPosition[1] > targetPosition[1]:
                return str("UP")
            elif currentPosition[0] < targetPosition[0]:
                return str("RIGHT")
            elif currentPosition[1] < targetPosition[1]:
                return str("DOWN")
            elif currentPosition[0] > targetPosition[0]:
                return str("LEFT")
            else:
                return None
                # if targetPosition is not currentPosition:
                #
                #     target = pygame.Rect(targetPosition[0] * 34, targetPosition[1] * 34, 34, 34)
                #     finalPosition = self.path[-1]

                #     currentPosition = (currentPosition[0] * 34, currentPosition[1] * 34)
                #     curPos = (currentPosition[0] * 34, currentPosition[1] * 34)                #
                #     if target.contains(rec1):
                #         print("Collide")
                #         if self.currentMove + 1 < int(len(self.path)):
                #             self.currentMove += 1
                #             print("Increment")
                #
                #     pos = (finalPosition[0] * 34, finalPosition[1] * 34)
                #     if rec1.collidepoint(pos):
                #         self.runAway(self.path[-1], self.path[-1][0])
                #         return str("BOOM")
                #
                #     if currentPosition[1] > targetPosition[1]:
                #         return str("UP")
                #     elif currentPosition[0] < targetPosition[0]:
                #         return str("RIGHT")
                #     elif currentPosition[1] < targetPosition[1]:
                #         return str("DOWN")
                #     elif currentPosition[0] > targetPosition[0]:
                #         return str("LEFT")
                #     else:
                #         return str("None")
            if self.isRunning == True:
                targetPosition = [self.runAwayPath[-1][0] * 34, self.runAwayPath[-1][1] * 34]
                if self.runAwayPath is not None:
                    finalPosition = self.runAwayPath[-1]
                    rec1 = pygame.Rect((currentPosition[0]) * 34, currentPosition[1] * 34, 34, 34)
                    rec2 = pygame.Rect((finalPosition[0]) * 34, finalPosition[1] * 34, 34, 34)
                    currentPosition = (currentPosition[0] * 34, currentPosition[1] * 34)
                    pos = (finalPosition[0] * 34, finalPosition[1] * 34)
                    if rec1.collidepoint(pos):
                        return str("NewTarget")
                    if currentPosition[1] > targetPosition[1]:
                        return str("UP")
                    elif currentPosition[0] < targetPosition[0]:
                        return str("RIGHT")
                    elif currentPosition[1] < targetPosition[1]:
                        return str("DOWN")
                    elif currentPosition[0] > targetPosition[0]:
                        return str("LEFT")
                    else:
                        return str("None")
                    return str("None")
