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
    # gets the current path for a AI

    def isSeeking(self):
        return self.hasPath
    # clear woking varibles

    def reset(self):
        self.hasPath = False
        self.isRunning = False
        self.currentMoveRun = 0
        self.currentMoveRun = 0
    # setup the internal map varible

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

    # check if there is a bomb within 2 tiles of the current location
    def check_Safty(self, map_Object, position, distance=2):
        # all the posible direction that need checking
        directions = [[0, 1], [0, -1], [1, 0], [-1, 0]]
        # for each direction go the distence passed and cheick if there is a bomb
        for direction in directions:
            # for the range of the passed distance incorpment position
            # then check if there is a bomb there
            for x in range(distance + 1):
                # make a copy of the passed position
                pos = position[:]
                pos[0] = pos[0] + direction[0] * x
                pos[1] = pos[1] + direction[1] * x
                # try to check the tile if it is out of the map brak the loop
                try:
                    tile = map_Object.map_Grid[pos[0]][pos[1]]
                    if(tile["Bomb"] == True):
                        return False
                    elif(tile["Tile"] == 'w'):
                        break
                except:
                    break
        return True

    # uses recursion to find all the safe locations within the gievn distance(desired_Distance)
    def check_For_Path(self, map_Object, position, possible_Paths, bomberman, direction=[0, 0], depth=0, path=[], desired_Distance=5):
        # all posible directions
        directions = [[0, 1], [0, -1], [1, 0], [-1, 0]]
        desired_Distance -= 1
        pos = position[:]
        # incroment the positon in the disred direction
        pos[0] += direction[0]
        pos[1] += direction[1]
        # make a copy of the path object then add the current position to the new path
        newPath = path[:]
        newPath.append(pos)
        # invert the direction giving the direction of the previos tile
        for i in range(len(direction)):
            direction[i] *= -1
        # if direction is not [0,0] remove it from the list of possible directions
        # this stops the function from checking the location the function was called from
        if(direction != [0, 0]):
            directions.remove(direction)
        # a list to store all movible locations
        movable = []
        for move in directions:
            # for each direction incroment the positon
            newPos = pos[:]
            newPos[0] = newPos[0] + move[0]
            newPos[1] = newPos[1] + move[1]
            # check the new position is a mobable tile and there isn't a bomb
            try:
                if(map_Object.map_Grid[newPos[0]][newPos[1]]["Movable"] and map_Object.map_Grid[newPos[0]][newPos[1]]["Bomb"] == False):
                    # if the position is movable add it to the list
                    movable.append(move)

            except IndexError:
                pass

        # if the desired_Distance has not been met call the function for all posible moved
        if(desired_Distance != 0):
            depth += 1
            for move in movable:
                self.check_For_Path(map_Object, pos, possible_Paths, bomberman, move, depth, newPath, desired_Distance)

        # if the found paths last location is safe add it to the list of possible_Paths
        if(self.check_Safty(map_Object, newPath[-1])):
            possible_Paths.append(newPath)

    def find_Safe_Space(self, map_Object, bomberman):
        # gets the tiles posion on the map object for the mans location
        pos = (map_Object.pos_To_Location([bomberman.get_Sprite_Center()]))[0]
        # make a list to store possible paths
        possible_Paths = []
        # use the resusive function to find all possible paths within a set range
        self.check_For_Path(map_Object, pos, possible_Paths, bomberman)
        # if three is a possbile path choice a random one then set it to the bots path
        if(len(possible_Paths) > 0):
            self.path = random.choice(possible_Paths)
            self.path.append(False)

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
        # get a list of all men without me in it
        man_Positions = []
        for not_Me in self.man_List:
            if(not_Me.ID != man.ID):
                # get the postion of each man then append it to the dic
                pos = (map_Object.pos_To_Location([not_Me.get_Sprite_Center()]))[0]
                man_Positions.append(pos)
        # get the positon of the current man
        pos = (map_Object.pos_To_Location([bomberman.get_Sprite_Center()]))[0]
        # for eahch man check if they are within 2 tiles of this bomberman
        # if so the funciton return ture else it retuns false
        for there_Pos in man_Positions:
            dif_X = abs(pos[0] - there_Pos[0])
            dif_Y = abs(pos[1] - there_Pos[1])
            if(pos[1] == there_Pos[1] and dif_X < 2 or pos[0] == there_Pos[0] and dif_Y < 2):
                return True
        return False

    def update(self, display, map_Object, bomberman):
        if self.path is not None:
            currentPosition = self.moving_Pos
            if(currentPosition == self.path[0]):
                self.back_Path.append(self.path.pop(0))

            if(type(self.path[0]) == bool):
                if(self.path[0] == True):
                    self.path = None
                    return str("BOOM")
                else:
                    self.path = None
                    return None

            targetPosition = self.path[0]

            man_In_Range = self.check_For_Men(bomberman, map_Object)
            if(man_In_Range == True):
                if(random.randint(0, 100) > 50):
                    self.path = None
                    return str("BOOM")
                else:
                    self.find_Safe_Space(map_Object, bomberman)

            if(self.check_Safty(map_Object, self.moving_Pos) == False and self.path[-1] == True):
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
                self.path = None
        else:
            man_In_Range = self.check_For_Men(bomberman, map_Object)
            if(self.check_Safty(map_Object, self.moving_Pos) == False):
                self.find_Safe_Space(map_Object, bomberman)
            elif(bomberman.bombs_Out <= 0):
                self.findMan(bomberman, map_Object)
            elif(man_In_Range == True):
                if(random.randrange(0, 100) >= 75):
                    self.path = None
                    return str("BOOM")
                else:
                    self.find_Safe_Space(map_Object, bomberman)
