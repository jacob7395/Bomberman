class Dijkstra:

    def __init__(self, x=0, y=0):

        self.validPosition = [[True for i in range(y)] for j in range(x)]
        self.width = x
        self.height = y
        self.initializeVariables()
# Need to optimize and add error handling if no available path/delete unused things

    def makeMoveable(self, x, y, state):
        self.validPosition[x][y] = state

    def initializeVariables(self):
        self.cost = [[100000 for i in range(self.height)] for j in range(self.width)]
        self.link = [[[-1, -1] for i in range(self.height)] for j in range(self.width)]
        self.inPath = [[False for i in range(self.height)] for j in range(self.width)]
        self.closed = [[False for i in range(self.height)] for j in range(self.width)]

    def getPath(self, playerPosition, botPosition, mapTiles):
        self.initializeVariables()
        self.cost[botPosition[0]][botPosition[1]] = 0
        findingPath = True
        self.foundPath = False
        steps = 0
        self.botPosition = botPosition
        self.dynamicTiles = mapTiles

        while (True):
            if steps > 100:
                return

            if self.closed[playerPosition[0]][playerPosition[1]] == True:
                self.foundPath = True
                break
            self.currentLowest = 100000000
            self.lowestI = 0
            self.lowestJ = 0
            steps += 1
            for i, row in enumerate(self.cost):
                for j, col in enumerate(row):
                    position = [i, j]
                    if (self.cost[i][j] < self.currentLowest and self.closed[i][j] == False and self.getClosed(position) == True and self.isValid(i, j)):
                        self.lowestI = i
                        self.lowestJ = j
                        self.currentLowest = self.cost[i][j]
            self.closed[self.lowestI][self.lowestJ] = True
            #print(mapTiles[self.lowestI] [self.lowestJ - 1])
            if self.isValid(self.lowestI, self.lowestJ - 1) == True and mapTiles[self.lowestI][self.lowestJ - 1].get("Tile") is not 'w' and mapTiles[self.lowestI][self.lowestJ - 1].get("Tile") is not 'b':
                if self.cost[self.lowestI][self.lowestJ] < self.cost[self.lowestI][self.lowestJ - 1]:
                    self.cost[self.lowestI][self.lowestJ - 1] = self.cost[self.lowestI][self.lowestJ] + 1
                    self.link[self.lowestI][self.lowestJ - 1] = [self.lowestI, self.lowestJ]

            if self.isValid(self.lowestI + 1, self.lowestJ) == True and mapTiles[self.lowestI + 1][self.lowestJ].get("Tile") is not 'w' and mapTiles[self.lowestI + 1][self.lowestJ].get("Tile") is not 'b':
                if self.cost[self.lowestI][self.lowestJ] < self.cost[self.lowestI + 1][self.lowestJ]:
                    self.cost[self.lowestI + 1][self.lowestJ] = self.cost[self.lowestI][self.lowestJ] + 1
                    self.link[self.lowestI + 1][self.lowestJ] = [self.lowestI, self.lowestJ]

            if self.isValid(self.lowestI, self.lowestJ + 1) == True and mapTiles[self.lowestI][self.lowestJ + 1].get("Tile") is not 'w' and mapTiles[self.lowestI][self.lowestJ + 1].get("Tile") is not 'b':
                if self.cost[self.lowestI][self.lowestJ] < self.cost[self.lowestI][self.lowestJ + 1]:
                    self.cost[self.lowestI][self.lowestJ + 1] = self.cost[self.lowestI][self.lowestJ] + 1
                    self.link[self.lowestI][self.lowestJ + 1] = [self.lowestI, self.lowestJ]

            if self.isValid(self.lowestI - 1, self.lowestJ) == True and mapTiles[self.lowestI - 1][self.lowestJ].get("Tile") is not 'w' and mapTiles[self.lowestI - 1][self.lowestJ].get("Tile") is not 'b':
                if self.cost[self.lowestI][self.lowestJ] < self.cost[self.lowestI - 1][self.lowestJ]:
                    self.cost[self.lowestI - 1][self.lowestJ] = self.cost[self.lowestI][self.lowestJ] + 1
                    self.link[self.lowestI - 1][self.lowestJ] = [self.lowestI, self.lowestJ]

        nextClosed = [playerPosition[0], playerPosition[1]]
        steps = list()
        stepCount = 0

        while self.foundPath == True:
            if stepCount > 1000:
                return
            self.inPath[nextClosed[0]][nextClosed[1]] = True
            steps.append([nextClosed[0], nextClosed[1]])
            nextClosed = self.link[nextClosed[0]][nextClosed[1]]
            stepCount += 1
            if nextClosed == botPosition:
                break
        steps.append(True)

        print("Got a Path")
        return steps

    def getPathSecond(self, playerPosition, botPosition, mapTiles):
        self.initializeVariables()
        self.cost[botPosition[0]][botPosition[1]] = 0
        findingPath = True
        self.foundPath = False
        steps = 0
        self.botPosition = botPosition
        self.dynamicTiles = mapTiles

        while (True):

            if steps > 100:
                return
            if self.closed[playerPosition[0]][playerPosition[1]] == True:
                self.foundPath = True
                break
            self.currentLowest = 100000000
            self.lowestI = 0
            self.lowestJ = 0
            steps += 1
            for i, row in enumerate(self.cost):
                for j, col in enumerate(row):
                    position = [i, j]
                    if (self.cost[i][j] < self.currentLowest and self.closed[i][j] == False and self.getClosed(position) == True) and mapTiles[i][j] is not 'w' and mapTiles[i][j] is not 'b':
                        self.lowestI = i
                        self.lowestJ = j
                        self.currentLowest = self.cost[i][j]
            self.closed[self.lowestI][self.lowestJ] = True

            if mapTiles[self.lowestI][self.lowestJ - 1] is not 'w' and mapTiles[self.lowestI][self.lowestJ - 1] is not 'b':
                if self.cost[self.lowestI][self.lowestJ] < self.cost[self.lowestI][self.lowestJ - 1]:
                    self.cost[self.lowestI][self.lowestJ - 1] = self.cost[self.lowestI][self.lowestJ] + 1
                    self.link[self.lowestI][self.lowestJ - 1] = [self.lowestI, self.lowestJ]

            if mapTiles[self.lowestI + 1][self.lowestJ] is not 'w' and mapTiles[self.lowestI + 1][self.lowestJ] is not 'b':
                if self.cost[self.lowestI][self.lowestJ] < self.cost[self.lowestI + 1][self.lowestJ]:
                    self.cost[self.lowestI + 1][self.lowestJ] = self.cost[self.lowestI][self.lowestJ] + 1
                    self.link[self.lowestI + 1][self.lowestJ] = [self.lowestI, self.lowestJ]

            if mapTiles[self.lowestI][self.lowestJ + 1] is not 'w' and mapTiles[self.lowestI][self.lowestJ + 1] is not 'b':
                if self.cost[self.lowestI][self.lowestJ] < self.cost[self.lowestI][self.lowestJ + 1]:
                    self.cost[self.lowestI][self.lowestJ + 1] = self.cost[self.lowestI][self.lowestJ] + 1
                    self.link[self.lowestI][self.lowestJ + 1] = [self.lowestI, self.lowestJ]

            if mapTiles[self.lowestI - 1][self.lowestJ] is not 'w' and mapTiles[self.lowestI - 1][self.lowestJ] is not 'b':
                if self.cost[self.lowestI][self.lowestJ] < self.cost[self.lowestI - 1][self.lowestJ]:
                    self.cost[self.lowestI - 1][self.lowestJ] = self.cost[self.lowestI][self.lowestJ] + 1
                    self.link[self.lowestI - 1][self.lowestJ] = [self.lowestI, self.lowestJ]

        nextClosed = [playerPosition[0], playerPosition[1]]
        steps = list()
        stepCount = 0

        while self.foundPath == True:
            if stepCount > 1000:
                return
            self.inPath[nextClosed[0]][nextClosed[1]] = True
            steps.append([nextClosed[0], nextClosed[1]])
            nextClosed = self.link[nextClosed[0]][nextClosed[1]]
            stepCount += 1
            if nextClosed == botPosition:
                break

        print("Got a Path")
        steps.append(botPosition)
        return steps

    def getClosed(self, pos):
        if self.closed[pos[0]][pos[1]] == True:
            return False
        else:
            return True

    def isValid(self, posX=-1, posY=-1):  # Temp isValid function

     #   if self.botPosition == [posX, posY] :
     #       return True
     #   elif self.dynamicTiles[posX][posY]['Tile'] == 'b' :
      #      return False

        if posX > 0 and posX < self.width and posY > 0 and posY < self.height:
           #     if self.validPosition[posX][posY] == True :
              #  return True;
          #  else :
              #  return False;
            return True
        else:
            return False
