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
        # map string to be retuned
        map_String = ""
        # run through each tile row by row then add the tile the the string
        for y in range(len(self.map_Grid[0])):
            for x in range(len(self.map_Grid) - 1):
                map_String += self.map_Grid[x][y]["Tile"]
            # return charater need to be added after each row
            map_String += '\n'
        return map_String

    def tile_At(self, position):
        """Find what tiles are at the passed position/positions"""
        # check position has been passed
        if(position == None):
            return None
        # a list used to store each tile
        l = []
        # run through each tile
        for pos in position:
            # try to get the desired tile if it fails add 0,0 normaly a wall
            try:
                # the tile is found by deviding the x,y posiotn by the scale of the map
                l.append(self.map_Grid[int(pos[0]) // self.scale][int(pos[1]) // self.scale])
            except:
                l.append(self.map_Grid[0][0])
        return l

    def pos_To_Location(self, position):
        # check position has been passed
        if(position == None):
            return None
        # print("Pos = {}".format(position))
        # a list used to store each tile
        l = []
        # run through each tile
        for pos in position:
            # try to get the desired tile if it fails add 0,0 normaly a wall
            try:
                # the tile is found by deviding the x,y posiotn by the scale of the map
                l.append([int(pos[0]) // self.scale, int(pos[1]) // self.scale])
            except:
                l.append([0, 0])
        # print("list = {}".format(l))
        return l

    def get_Movable(self, tiles):
        """checks if the passed tiles are movable then return is any are not"""
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

    def get_Tiles(self, tile_Character):
        # List for tiles to be stored in
        tiels = []
        # check the passed value is valid
        if(type(tile_Character) != str):
            return None
        # run through every tile in the map
        for row in self.map_Grid:
            for tile in row:
                # check if the tile is a desite tile then add to list
                # if a retun character is passed to the function all tils will be retuned
                if(tile["Tile"] == tile_Character or tile_Character == '\n'):
                    tiels.append(tile)

        return tiels
