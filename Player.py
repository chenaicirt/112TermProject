# max settlements you can have is 5
class Player (object):
    def __init__(self, color):
        self.settlementLocs = []  # locations of settlements
        self.roadLocs = []  # road locations, tuples
        self.numVP = 0  # number of victory points
        self.color = color
        self.rolled = False
        self.firstMoves = True
        self.possibleResources = dict()  # dicenum maps to resources list owned
        self.resources = dict()  # resources map to the number of resources
        self.resources["B"] = 5
        self.resources["L"] = 5
        self.resources["G"] = 5
        self.resources["W"] = 5
        self.resources["O"] = 5
        self.devCards = []


    def incVP(self):
        self.numVP += 1

    def getVictoryPoints (self):
        return self.numVP

    def addDevCard(self, devCard):
        self.devCards += [devCard]

    def getDevCards(self):
        return self.devCards

    def removeDevCard(self,index):
        self.devCards.pop(index)

    def checkResource(self, resource, num):
        return self.resources[resource] >= num

    def addFutureSources(self, num, resource):
        theNewList = self.possibleResources.get(num, [])
        theNewList += [resource]
        self.possibleResources[num] = theNewList


    def increaseResourceFromNum(self, num):
        if (num in self.possibleResources):
            for terrain in self.possibleResources[num]:
                if (terrain in self.possibleResources[num]):
                    self.resources[terrain] += 1

    def increaseResource(self, resource):
        if (resource in self.resources):
            self.resources[resource] += 1
    # checks if player has the resources to build settlement
    def canBuildSettlement(self):

        if (self.resources["B"] >= 1 and self.resources["L"] >= 1 and
                self.resources["G"] >= 1 and self.resources["W"] >= 1):
            return True

        return False

    def roll(self):
        self.rolled = True

    def unRoll(self):
        self.rolled = False

    def curRoll (self): 
        return self.rolled


    def getColor(self):
        return self.color

    def canBuildCity(self):
        if (self.resources["G"] >= 2 and self.resources["O"] >= 3):
            return True

        return False
    def updateResourceCity(self):
        self.resources["G"] -= 2
        self.resources["O"] -= 3

    def canGetDevCard(self):
        if (self.resources["W"] >= 1 and self.resources["G"] >= 1 and
                self.resources["O"] >= 1):
            return True
        return False

    def updateDevResource(self):
        self.resources["W"] -= 1
        self.resources["G"] -= 1
        self.resources["O"] -= 1


    def placeSettlement(self, rect, firstTurns):
        if (not firstTurns):
            self.resources["B"] -= 1
            self.resources["L"] -= 1
            self.resources["G"] -= 1
            self.resources["W"] -= 1

        self.incVP()
        self.settlementLocs += [rect]

    def placeRoad(self, points, firstTurns):
        if (not firstTurns):
            self.resources["B"] -= 1
            self.resources["L"] -= 1

        self.roadLocs += [points]

    def removeResource(self, resource, quantity):
        self.resources[resource] -= quantity

    def addResource(self, resource, quantity):
        self.resources[resource] += quantity

    def canPlaceRoad (self):
        if (self.resources["B"] >= 1 and self.resources["L"] >= 1):
            return True

        return False

    def canRemoveResource (self, resource, quantity): 
        if (self.resources[resource] >= quantity):
            return True
        else:
            return False

    def getRoadLocs(self):
        return self.roadLocs

    def getSettlementLocs(self):
        return self.settlementLocs