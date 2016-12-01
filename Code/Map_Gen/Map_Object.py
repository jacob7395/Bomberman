import pygame
import os
from os import path


class o_Map:

    def __init__(self, grid, size=16, grid_Start_Position=0):
        # read in tile info
        self.read_Tile_Props()
        # define the map grid where [x][y] hold properts for that tile
        self.map_Grid = [""] * len(grid[0])
        self.scale = size
        self.map_String = ""
        self.bush_List = []
        for row in grid:
            self.map_String += row

        for x in range(len(self.map_Grid)):
            self.map_Grid[x] = []
        y = 0
        for row in grid:
            x = 0
            for character in row:
                if(character == '\n'):
                    break
                # fill the map grid with the respective properties
                self.map_Grid[x].append({"Tile": character, "Position": (size * x, size * y), "Movable": self.tile_Dic[character], "C_Aare": (size, size), "Bomb": False, "Bomb_Object": None})
                if(character == 'b'):
                    self.bush_List.append(self.map_Grid[x])
                x += 1
            y += 1

    def __str__(self):
        map_String = ""
        for y in range(len(self.map_Grid[0]) - 1):
            for x in range(len(self.map_Grid) - 1):
                map_String += self.map_Grid[x][y]["Tile"]
            map_String += '\n'
        return map_String

    def tile_At(self, position):
        # check position has been passed
        if(position == None):
            return None
        l = []
        for pos in position:
            try:
                l.append(self.map_Grid[int(pos[0]) // self.scale][int(pos[1]) // self.scale])
            except:
                l.append(self.map_Grid[0][0])
        return l

    def get_Movable(self, tiles):
        for tile in tiles:
            if(tile["Movable"] == False):
                return False
        return True

    def read_Tile_Props(self):
        # Setup tile path
        path = os.path.realpath(__file__)
        for i in range(0, 2):
            path = os.path.dirname(path)
        path_Time_Prop = path + "/Map_Gen/" + "Tiles"
        # Read each line of the tile info
        with open(path_Time_Prop, "r") as f:
            tile = f.readlines()
            f.close
        # remove end character
        # split the string at the = character
        # add each list to the dictonery
        self.tile_Dic = {}
        for x in range(len(tile)):
            tile[x] = tile[x].replace("\n", "")
            tile[x] = tile[x].split("=")
            self.tile_Dic.update({tile[x][0]: bool(int(tile[x][1]))})
