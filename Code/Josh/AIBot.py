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

    def setlastPosition(self, position):
        self.lastPosition = position

    def getlastPosition(self):
        return self.lastPosition

    def check_Safty(self, map_Object, position, distance=2):
        directions = [[0, 1], [0, -1], [1, 0], [-1, 0]]
        for direction in directions:
            pos = position[:]
            for x in range(distance + 1):
                pos[0] = pos[0] + direction[0] * x
                pos[1] = pos[1] + direction[1] * x
                try:
                    tile = map_Object.map_Grid[pos[0]][pos[1]]
                    if(tile["Bomb"] == True):
                        return False
                    elif(tile["Tile"] == 'w'):
                        break
                except:
                    pass
        return True

    def check_For_Path(self, map_Object, position, possible_Paths, bomberman, direction=[0, 0], depth=0, path=[], desired_Distance=5):
        directions = [[0, 1], [0, -1], [1, 0], [-1, 0]]
        desired_Distance -= 1
        pos = position[:]

        # print("Old Position = {}, Came_From = {}".format(position, direction))

        pos[0] += direction[0]
        pos[1] += direction[1]

        newPath = path[:]
        newPath.append(pos)

        for i in range(len(direction)):
            direction[i] *= -1
        if(direction != [0, 0]):
            directions.remove(direction)

        # print("New Position = {}, Directions = {},current depth = {}, Current Path = {}".format(pos, directions, desired_Distance, newPath))
        movable = []
        for move in directions:
            newPos = pos[:]
            newPos[0] = newPos[0] + move[0]
            newPos[1] = newPos[1] + move[1]
            # print("move = {}, New positon = {}".format(move, newPos))
            try:
                if(map_Object.map_Grid[newPos[0]][newPos[1]]["Movable"] and map_Object.map_Grid[newPos[0]][newPos[1]]["Bomb"] == False):
                    movable.append(move)
                    # print(map_Object.map_Grid[newPos[0]][newPos[1]])
            except IndexError:
                pass

        if(desired_Distance != 0):
            # print("Moves = {}".format(directions))
            depth += 1
            for move in movable:
                self.check_For_Path(map_Object, pos, possible_Paths, bomberman, move, depth, newPath, desired_Distance)

        if(self.check_Safty(map_Object, newPath[-1]) and depth >= 2):
            # print("{} is Safe path is {}, depth is {}".format(newPath[-1], newPath, depth))
            possible_Paths.append(newPath)

    def find_Safe_Space(self, map_Object, bomberman):
        if(bomberman.ID != 1):
            # return
            pass

        # print("Finding")
        # gets the tiles posion on the map object for the mans location
        pos = (map_Object.pos_To_Location([bomberman.get_Sprite_Center()]))[0]

        possible_Paths = []
        self.check_For_Path(map_Object, pos, possible_Paths, bomberman)
        if(len(possible_Paths) > 0):
            self.path = random.choice(possible_Paths)
            self.path.append(False)
        # print(pos)
        # print(self.path)

    def findMan(self, me_Man, map, man_List=None):
        if(man_List != None):
            self.man_List = man_List
        man = me_Man
        # get a list of all men withouth me in it
        man_List_Not_Me = []
        for not_Me in self.man_List:
            if(not_Me.ID != man.ID):
                man_List_Not_Me.append(not_Me)
        target = random.choice(man_List_Not_Me)
        # gets the tiles posion on the map object for the mans location
        pos = (map.pos_To_Location([man.get_Sprite_Center()]))[0]
        tagert_Pos = (map.pos_To_Location([target.get_Sprite_Center()]))[0]
        # get path with dicstra
        path = self.pathFinding.getPath(pos, tagert_Pos, map.map_Grid)
        self.path = path

    def check_For_Men(self, bomberman, map_Object):
        man = bomberman
        # get a list of all men withouth me in it
        man_Positions = []
        for not_Me in self.man_List:
            if(not_Me.ID != man.ID):
                pos = (map_Object.pos_To_Location([not_Me.get_Sprite_Center()]))[0]
                man_Positions.append(pos)

        pos = (map_Object.pos_To_Location([bomberman.get_Sprite_Center()]))[0]

        for there_Pos in man_Positions:
            dif_X = abs(pos[0] - there_Pos[0])
            dif_Y = abs(pos[1] - there_Pos[1])
            if(pos[1] == there_Pos[1] and dif_X < 2 or pos[0] == there_Pos[0] and dif_Y < 2):
                return True

    def update(self, display, map_Object, bomberman):
        if self.path is not None:
            currentPosition = self.moving_Pos
            if(currentPosition == self.path[0]):
                self.back_Path.append(self.path.pop(0))

            man_In_Range = self.check_For_Men(bomberman, map_Object)
            man_In_Range = False

            if(type(self.path[0]) == bool or man_In_Range == True):
                if(self.path[0] == True or man_In_Range == True):
                    self.path = None
                    return str("BOOM")
                else:
                    self.path = None
                    return None

            targetPosition = self.path[0]

            if(self.check_Safty(map_Object, self.moving_Pos) == False):
                self.find_Safe_Space(map_Object, bomberman)

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
        else:
            if(self.check_Safty(map_Object, self.moving_Pos) == False):
                self.find_Safe_Space(map_Object, bomberman)
            elif(bomberman.bombs_Out == 0):
                self.findMan(bomberman, map_Object)
