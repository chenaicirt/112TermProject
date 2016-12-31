import os
import sys
import pygame
import catanBoard
import Player
import build
import ViewResources
import random
import DevelopmentCard
import TermProject
import promptTrade
from pygame.locals import *

import TextWidget
TEXT_WIDGET_CLICK = pygame.locals.USEREVENT + 1

mouseClicked = False


class playCatan():

    def __init__(self, width=850, height=650):
        pygame.init()
        self.diceimg = None
        self.diceimge2 = None
        self.screen = pygame.display.set_mode((width, height), 0)
        self.background = pygame.Surface(self.screen.get_size(), SWSURFACE)
        self.background = self.background.convert()
        self.background.fill((229, 239, 255))
        self.screen.blit(self.background, (0, 0))
        self.displayHexes()
        self.curPlayer = 0
        self.players = []
        self.turns = 0  # keep track of the first few turns
        self.firstTurns = True
        self.buildingRoad = False
        self.buildingCity = False

        self.moveRobber = False
        self.robberImg = pygame.image.load("robber.png")

        centers = [(168, 58), (224, 87), (284, 59), (341, 88), (399, 59),
                   (449, 88), (453, 149), (511, 182), (512, 243), (566, 274),
                   (571, 335), (513, 370), (513, 370), (513, 432), (460, 465),
                   (460, 529), (407, 559), (349, 528), (295,558), (235, 526),
                   (178,559),
                   (122,526), (120,469), (65,432), (61,37), (4,336), (6,281), (60,244), (57,183), (113, 149),
                   (118,189), (168,179), (224,148), (287, 179), (345, 148),(401,176), (115,271), (172,249),
                   (227,271), (286, 244), (344,275),(404, 244), (457, 272),(117,336), (173, 368), (229, 339),
                   (290, 370), (346, 336), (406, 367), (462,340), (176, 432), (235, 465), (293,434), (350,464),
                   (406,433)]

        self.allPointRects = []
        self.roadPoints = []
        self.settlementImgs = []
        self.settlementRects = []
        self.roadLocs = []
        self.roadColor = []

        for point in centers:
            x, y = point[0], point[1]
            self.allPointRects += [Rect((x - 20, y - 20), (40, 40))]

        self.setNames = ["red", "blue", "orange", "purple"]
        self.colors = [(255, 75, 56), (0, 0, 255), (255, 215, 0), (238, 130, 238)]
        for i in range(4):
            self.players += [Player.Player(self.setNames[i])]

        text = ("Player %d's turn") % (self.curPlayer + 1)
        font = pygame.font.Font(None, 36)
        self.playerText = font.render(text, 1,self.colors[self.curPlayer % 4])
        text = "Victory Points: %d" %self.players [self.curPlayer % 4].getVictoryPoints()
        self.VPText = font.render (text, 1, self.colors[self.curPlayer % 4])
        self.buildingSettlement = True
        self.messageText = "Please Build Settlement"

        pygame.display.update()
        self.timer = pygame.time.Clock()
        self.text_widgets = []

        text = "Roll Dice"
        dice = TextWidget.TextWidget(text, (0, 0, 0), 30)
        dice.rect.top = 150
        dice.rect.left = 600
        dice.on_mouse_click = self.rollDice
        self.text_widgets.append(dice)

        text = "View Resouces"
        resources = TextWidget.TextWidget(text, (0, 0, 0), 30)
        resources.rect.top = 200
        resources.rect.left = 600
        resources.on_mouse_click = self.switchResources
        self.text_widgets.append(resources)

        text = "Build"
        build = TextWidget.TextWidget(text, (0, 0, 0), 30)
        build.rect.top = 250
        build.rect.left = 600
        build.on_mouse_click = self.switchBuild
        self.text_widgets.append(build)

        text = "Trade"
        trade = TextWidget.TextWidget(text, (0, 0, 0), 30)
        trade.rect.top = 300
        trade.rect.left = 600
        trade.on_mouse_click = self.switchTrade
        self.text_widgets.append(trade)

        text = "Development Card"
        devCard = TextWidget.TextWidget(text, (0, 0, 0), 30)
        devCard.rect.top = 350
        devCard.rect.left = 600
        devCard.on_mouse_click = self.switchDevCard
        self.text_widgets.append(devCard)

        text = "End Turn"
        endturn = TextWidget.TextWidget(text, (0, 0, 0), 30)
        endturn.rect.top = 400
        endturn.rect.left = 600
        endturn.on_mouse_click = self.endTurn
        self.text_widgets.append(endturn)
        self.main_loop()

    def useKnightCard (self):
        self.messageText = "Please Move Robber"
        self.moveRobber = True
        self.players[self.curPlayer % 4].removeDevCard(0)
        self.main_loop()

    def rollDice(self, event):
        if (not self.firstTurns):
            if (not self.players[self.curPlayer % 4].curRoll()):
                num = random.randint(1, 6)
                picName = "dice%d" % num
                self.diceimg = pygame.image.load(picName + ".png")

                num2 = random.randint(1, 6)
                picName2 = "dice%d" % num2
                self.diceimg2 = pygame.image.load(picName2 + ".png")

                self.players[(self.curPlayer % 4)].roll()

                self.updateResources(num + num2)

                if ((num + num2) == 7):
                    self.messageText = "Robber Activated! Please Move the Robber"
                    self.moveRobber = True

        else:
            self.messageText = "You Can't Roll Yet!"

    def updateResources(self, num):
        count = 0
        curHex = self.rectToHexagons[tuple(self.robberRect)][0]
        hexrect = pygame.Rect(tuple(self.robberRect))

        for player in self.players:
            player.increaseResourceFromNum(num)
            count += 1
            for settlement in player.getSettlementLocs():
                if (hexrect.colliderect(settlement) and curHex.getNumber() == num):
                    player.removeResource(curHex.getTerrain(), 1)


    def comeBackFromScreen(self):
        self.messageText = ""
        self.main_loop()

    #function to transition from build.py
    def goBackToBuildSettlement(self):
        self.buildingSettlement = True
        self.draw()
        self.main_loop()

    def placeSettlement (self, color, rect):
        settlementimg = pygame.image.load(color + ".png")
        self.settlementRects += [rect]
        self.settlementImgs += [settlementimg]

    def goBuildSettlement(self):
        curPlayer = self.curPlayer % 4
        actualPlayer = self.players[curPlayer]

        for rect in self.allPointRects:
            if(rect.collidepoint(pygame.mouse.get_pos())):
                self.placeSettlement(self.setNames[curPlayer], rect)
                self.messageText = ""
                actualPlayer.placeSettlement(rect, self.firstTurns)
                # adds all nighboring hexes
                for hextup in self.rectToHexagons:
                    hexrect = pygame.Rect(hextup)
                    if(hexrect.colliderect(rect)):
                        curHex = self.rectToHexagons[hextup][0]
                        terrain = curHex.getTerrain()
                        num = curHex.getNumber()
                        actualPlayer.addFutureSources(num, terrain)
                        if (self.firstTurns):
                            player = self.players[curPlayer]
                            player.increaseResource(terrain)

                self.buildingSettlement = False

                if (self.firstTurns):
                    self.messageText = "Please Build a Road too"
                    self.buildingRoad = True

    def goBuildCity(self):
        curPlayer = self.curPlayer % 4
        actualPlayer = self.players[curPlayer]
        color = self.colors[curPlayer]
        for settlement in actualPlayer.getSettlementLocs():
                if(settlement.collidepoint(pygame.mouse.get_pos())):
                    pygame.draw.rect(self.background, color, settlement, 5)

        actualPlayer.updateResourceCity()
        actualPlayer.incVP()
        self.buildingCity = False

    def buildCity(self):
        self.buildingCity = True
        self.draw()
        self.main_loop()

    #function to transition from build.py 
    def gobuildRoad(self):
        self.buildingRoad = True
        self.roadPoints = []
        self.draw()
        self.main_loop()

    def tradeEverything(self, curNum, goThru, info):
        self.players[curNum].addResource(info[0], info[1])
        self.players[curNum].removeResource(info[2], info[3])

        self.players[goThru].addResource(info[2], info[3])
        self.players[goThru].removeResource(info[0], info[1])

        self.main_loop()

    # goes to viewResources screen
    def switchResources(self, event):
        ViewResources.resource(self, self.players[self.curPlayer % 4])
        self.background.fill((229, 239, 255))

    def switchTrade(self, event):
        promptTrade.promptTradeScreen(self, self.curPlayer % 4, self.players)
        self.background.fill((229, 239, 255))

    #displays development cards
    def switchDevCard(self, event):
        DevelopmentCard.DevelopmentCard(self, self.players[self.curPlayer % 4])
        self.background.fill((229, 239, 255))

    # goes to build screen
    def switchBuild(self, event):
        if (self.players[self.curPlayer % 4].curRoll()):
            build.build(self, self.players[self.curPlayer % 4])
            self.background.fill((229, 239, 255))
        else:
            if (self.firstTurns):
                self.messageText = "You Can't Build Yet, End Your Turn"
            else:
                self.messageText = "Please Roll The Dice First"

    def displayDice(self):
        if (not self.firstTurns):
            if (self.diceimg is not None and self.diceimg2 is not None):
                diceRect = self.diceimg.get_rect()
                diceRect = diceRect.move(550, 500)
                self.screen.blit(self.diceimg, diceRect)

                diceRect2 = self.diceimg2.get_rect()
                diceRect2 = diceRect2.move(660, 500)
                self.screen.blit(self.diceimg2, diceRect2)

    # loads in all the images, only called once
    def displayHexes(self):
        aCatanBoard = catanBoard.Board(3)
        findHex = aCatanBoard.getallHexes()
        self.rectToHexagons = dict()
        self.hexImg = []
        self.numImg = []
        self.hexRects = []
        hexes = aCatanBoard.getHexTuples()

        index = 0
        for row in range(len(hexes)):
            for col in range(len(hexes[row])):
                tup = hexes[row][col]

                x, y = tup[0], tup[1]  # hexagon numbers
                picName = findHex[tup].getTerrain()
                numName = str(findHex[tup].getNumber())

                img = pygame.image.load(picName + ".png")
                rect = img.get_rect()
                numimg = pygame.image.load(numName + ".png")
                locX, locY = ((x + 1) * 115), ((y + 2.5) * 115)

                if (y != -2):
                    locY -= (20) * index
                    locX += (60) * index



                rect = rect.move((locX), (locY))
                if (picName == "D"):
                    self.robberLoc = (locX, locY)
                    self.robberRect = (rect)
                self.screen.blit(img, (locX, locY))
                self.screen.blit(numimg, (locX, locY))
                self.hexImg += [img]
                self.numImg += [numimg]
                self.hexRects += [(locX, locY)]
                self.rectToHexagons[tuple(rect)] = (findHex[tup], tup)
                pygame.display.flip()

            index += 1
    # to actually draw hexes
    def drawHexesAgain(self):
        for i in range(len(self.hexRects)):
            self.screen.blit(self.hexImg[i], self.hexRects[i])
            self.screen.blit(self.numImg[i], self.hexRects[i])

    def drawSettlementsAgain (self):
        for i in range (len(self.settlementImgs)):
            settlementImgRect = self.settlementRects[i]
            settlementImgRect = settlementImgRect.move(10,10)
            self.screen.blit(self.settlementImgs[i], settlementImgRect)

    # updates player text
    def endTurn(self, event):
        if (self.players[self.curPlayer % 4].curRoll() or self.firstTurns):
            self.turns += 1

            if (self.turns < 4 or self.turns > 8):
                self.curPlayer += 1
            elif (self.turns > 4 and self.turns < 8):
                self.curPlayer -= 1

            text = ("Player %d's turn") % ((self.curPlayer % 4) + 1)
            font = pygame.font.Font(None, 36)
            self.playerText = font.render(text, 1, self.colors[self.curPlayer % 4])
            text = "Victory Points: %d" %self.players[self.curPlayer % 4].getVictoryPoints()
            self.VPText = font.render(text, 1, self.colors[self.curPlayer % 4])
            if (self.turns < 8):
                self.buildingSettlement = True
                self.messageText = "Please Build Settlement"
            else:
                self.firstTurns = False
        else:
            self.messageText = "Please Roll First"

        if (self.players[self.curPlayer % 4].getVictoryPoints() == 10):
            self.background.fill((229, 239, 255))
            TermProject.splashScreen()


    def drawRobber(self): 
        self.screen.blit(self.robberImg, self.robberLoc)

    def draw(self):
        rects = []
        rects.append(self.timer_update())

        font = pygame.font.Font(None, 36)
        label = font.render(self.messageText, 1, (10, 10, 10))
        self.screen.blit(label, (300, 600))
        rects += [(label.get_rect())]

        self.screen.blit(self.playerText, (575, 100))

        self.screen.blit(self.VPText, (0, 0))
        rects += [self.VPText.get_rect()]
        rects += [self.playerText.get_rect()]


        self.drawHexesAgain()
        self.drawRoadAgain()
        self.drawSettlementsAgain()
        self.displayDice()

        for text in self.text_widgets:
            rect = text.draw(self.screen)
            rects.append(rect)
        self.drawRobber()
        pygame.display.update(rects)

    def timer_update(self):
        """Update the Timer
        returns - pygame.rect - The rect that the timer
        needs to be redrawn, or None on error"""

        rect_return = None

        if (pygame.font):
            # timer_string = "%.2f" % self.timer.get_fps()
            # basic font
            font = pygame.font.Font(None, 36)
            message = font.render("", 1, (147, 1, 16))
            rect_return = message.get_rect(left=0)
            rect_return.width += 25
            self.screen.blit(self.background, rect_return)
            self.screen.blit(message, rect_return)

        return rect_return

    def drawRoadAgain(self):
        for i in range(len(self.roadLocs)):
            pygame.draw.line(self.screen, self.roadColor[i],
                             self.roadLocs[i][0], self.roadLocs[i][1],
                             5)

    def buildRoad(self):
        curPlayer = self.curPlayer % 4
        playerLoc = self.players[curPlayer].getSettlementLocs()
        if (len(self.roadPoints) >= 3):
            atLeastOnePoint = False
            for rect in playerLoc:
                if (rect.collidepoint(self.roadPoints[1])):
                    atLeastOnePoint = True
                if (rect.collidepoint(self.roadPoints[2])):
                    atLeastOnePoint = True
            if (atLeastOnePoint is False and self.firstTurns):
                self.messageText = "You cannot place a road there"
                self.roadPoints = []
                self.buildingRoad = self.firstTurns
            else:
                pygame.draw.line(self.background,
                                 self.colors[curPlayer],
                                 self.roadPoints[1],
                                 self.roadPoints[2],
                                 20)
                endPoints = (self.roadPoints[1], self.roadPoints[2])
                self.roadLocs += [endPoints]
                self.roadColor += [self.colors[curPlayer]]
                self.players[curPlayer].placeRoad(endPoints, self.firstTurns)
                self.messageText = "You built a road!"
                self.roadPoints = []
                self.buildingRoad = False
        else:
            # all possible settlement locs on board
            for rect in self.allPointRects:
                if(rect.collidepoint(pygame.mouse.get_pos())):
                    self.roadPoints += [rect.center]
  


    def main_loop(self):
        while 1:
            # Tick of the timer
            # self.timer.tick()
            self.event_loop()
            self.draw()

    def event_loop(self):
        curPlayer = self.curPlayer % 4
        actualPlayer = self.players[curPlayer]
        for event in pygame.event.get():

            if (event.type == pygame.QUIT):
                pygame.quit()
                sys.exit()

            elif (event.type == pygame.MOUSEMOTION):
                for text in self.text_widgets:
                    text.highlight = text.rect.collidepoint(event.pos)
                    text.update_surface()

            elif(event.type == pygame.MOUSEBUTTONDOWN):
                if (self.buildingSettlement):
                    self.goBuildSettlement()

                if (self.buildingCity):
                    self.goBuildCity()

                if(self.buildingRoad):
                    self.buildRoad()

                if (self.moveRobber):
                    for tup in self.rectToHexagons:
                        rect = pygame.Rect(tup)
                        if(rect.collidepoint(pygame.mouse.get_pos())):
                            self.robberLoc = (rect.topleft)
                            self.robberRect = tup
                    self.messageText = "Robber Placed!"
                    self.moveRobber = False

                else:
                    for text in self.text_widgets:
                        text.on_mouse_button_down(event)


            elif (event.type == pygame.MOUSEBUTTONUP):
                for text in self.text_widgets:
                    text.on_mouse_button_up(event)
            elif (event.type == TextWidget.TEXT_WIDGET_CLICK):
                print (event.text_widget)

if __name__ == "__main__":
    game = playCatan()
    game.main_loop()
