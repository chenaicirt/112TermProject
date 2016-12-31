import random


class allHexagons (object):
    # 112 is the number of the desert 
    theNumbers = [5, 2, 6, 3, 8, 10, 9, 12, 11, 4, 8, 10, 9, 4, 5, 6, 3, 11,112]
    # D is dessert, O is ore, G is grain, W is wool, B is brick, L is lumber 
    theTerrain = ["O", "O", "O", "G", "G", "G", "G", "W", "W", "W", "W",
                  "B", "B", "B", "L", "L", "L", "L", "D"]

    def __init__(self):
        self.allHex = []
        self.vertices = []

        while (len(allHexagons.theNumbers) != 0):

            high = len(allHexagons.theTerrain) - 1
            number = allHexagons.theNumbers.pop(random.randint(0, high))
            if (number == 112):
                terrain = "D"
                allHexagons.theTerrain.remove("D")
            else:
                index = random.randint(0, high)
                while (allHexagons.theTerrain[index] == "D"):
                    index = random.randint(0, high)
                terrain = allHexagons.theTerrain.pop(index)

            self.allHex += [hexagon(number, terrain)]

    def __str__(self):

        toReturn = ""
        for a in self.allHex:
            toReturn += str(a)
            toReturn += " "

        return toReturn


    def getHexagons(self):
        return self.allHex

# a individual hexagon which contains a number and terrain
class hexagon (object):

    def __init__(self, number, terrain):
        self.number = number
        self.terrain = terrain

    def __str__(self):
        return ("Number: %d Terain %s \n" %
                (self.number, self.terrain))

    def getTerrain(self):
        return self.terrain

    def getNumber(self):
        return self.number


# will be 3x3 
class Board (object):
    def __init__(self, numHexes):
        aHexes = allHexagons().getHexagons()

        self.board = Board.createBoard(numHexes)  # creates jagged board
        self.allHexes = dict()  # maps board to hexagon attributes

        # loops through the board
        for row in range(len(self.board)):
            for hex in self.board[row]:
                if (len(aHexes) != 0):
                    high = len(aHexes) - 1
                    toRemoveIndex = random.randint(0, high)
                    self.allHexes[hex] = aHexes[toRemoveIndex]
                    aHexes.pop(toRemoveIndex)
                else:
                    self.allHexes[hex] = hexagon(112, "D")

    def getallHexes(self):
        return self.allHexes

    def getHexTuples (self):
        return self.board

    def __str__(self):
        toReturn = ""
        for tup in self.allHexes:
            toReturn += (str(tup) + ":")
            toReturn += (str(self.allHexes[tup]))

        return toReturn


    # given tuple, we can return the neighboring hexagons 
    def getNeighbors(self, locHex):

        toReturn = []
        centerX, centerY = locHex[0], locHex[1]

        offset = centerX
        y = centerY - 1
        upperRange = centerX + 2

        while(y != (centerY + 2)):
            for x in range(offset, upperRange):
                if ((x, y) in self.allHexes):
                    toReturn += [(x, y)]
            if (y < centerY):
                offset -= 1
            else:
                upperRange -= 1
            y += 1

        return toReturn

    @staticmethod
    def createBoard(length):
        board = []
        offset = 0
        y = -2
        upperRange = length

        while (y != length):
            row = []
            for x in range(offset, upperRange):
                row += [(x, y)]
            if (y < 0):
                offset -= 1
            if (y >= 0):
                upperRange -= 1
            y += 1
            board += [row]
        return board