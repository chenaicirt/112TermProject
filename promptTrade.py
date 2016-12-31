# 14 Soldiers/Knights (I’ll call them Knights from now on)
# 5 Victory Points
# 2 Road Building Cards
# 2 Monopoly Cards
# 2 Year of Plenty Cards

import os
import sys
import pygame
import playCatan
import Player
import tradePlayer

from pygame.locals import *

import TextWidget

TEXT_WIDGET_CLICK = pygame.locals.USEREVENT + 1

# http://www.learningpython.com/2006/12/13/textwidget-a-simple-text-class-for-pygame/
class promptTradeScreen ():

    def __init__(self, curGame, curNum, players, width=850, height=650):
        self.curNum = curNum
        self.catanGame = curGame
        self.players = players
        self.curPlayer = self.players[self.curNum]
        self.desiredResource = ""
        self.undesiredResource = ""
        self.messageText = ""
        self.desiredQuantity = 0
        self.undesiredQuantity = 0

        self.continueBuildScreen = True
        pygame.init()

        # create the screen
        self.screen = pygame.display.set_mode((width, height), 0)
        self.background = pygame.Surface(self.screen.get_size(), SWSURFACE)
        self.background = self.background.convert()

        self.background.fill((229, 239, 255))

        self.screen.blit(self.background, (0, 0))
        self.main_loop()



    def main_loop(self):

        if (self.continueBuildScreen):

            pygame.display.update()
            self.timer = pygame.time.Clock()

        # self.resources["G"] = 0
        # self.resources["O"] = 0

            # Text Widget list
            self.text_widgets = []

            wantSheep = TextWidget.TextWidget("Sheep",
                                              (0, 0, 0), 30)
            wantSheep.rect.center = (100, 150)
            wantSheep.on_mouse_click = self.wantSheep
            self.text_widgets.append(wantSheep)

            wantBrick = TextWidget.TextWidget("Brick",
                                              (0, 0, 0), 30)
            wantBrick.rect.center = (100, 200)
            wantBrick.on_mouse_click = self.wantBrick
            self.text_widgets.append(wantBrick)

            wantWood = TextWidget.TextWidget("Wood",
                                             (0, 0, 0), 30)
            wantWood.rect.center = (100, 250)
            wantWood.on_mouse_click = self.wantWood
            self.text_widgets.append(wantWood)

            wantWheat = TextWidget.TextWidget("Wheat",
                                              (0, 0, 0), 30)
            wantWheat.rect.center = (100, 300)
            wantWheat.on_mouse_click = self.wantWheat
            self.text_widgets.append(wantWheat)

            wantOre = TextWidget.TextWidget("Ore",
                                            (0, 0, 0), 30)
            wantOre.rect.center = (100, 350)
            wantOre.on_mouse_click = self.wantOre
            self.text_widgets.append(wantOre)


            wantOne = TextWidget.TextWidget("1",
                                            (0, 0, 0), 30)
            wantOne.rect.center = (200, 150)
            wantOne.on_mouse_click = self.wantOne
            self.text_widgets.append(wantOne)

            wantTwo = TextWidget.TextWidget("2",
                                            (0, 0, 0), 30)
            wantTwo.rect.center = (200, 200)
            wantTwo.on_mouse_click = self.wantTwo
            self.text_widgets.append(wantTwo)

            wantThree = TextWidget.TextWidget("3",
                                              (0, 0, 0), 30)
            wantThree.rect.center = (200, 250)
            wantThree.on_mouse_click = self.wantThree
            self.text_widgets.append(wantThree)

            wantFour = TextWidget.TextWidget("4",
                                             (0, 0, 0), 30)
            wantFour.rect.center = (200, 300)
            wantFour.on_mouse_click = self.wantFour
            self.text_widgets.append(wantFour)

            wantFive = TextWidget.TextWidget("5",
                                             (0, 0, 0), 30)
            wantFive.rect.center = (200, 350)
            wantFive.on_mouse_click = self.wantFive
            self.text_widgets.append(wantFive)



            tradeSheep = TextWidget.TextWidget("Sheep",
                                               (0, 0, 0), 30)
            tradeSheep.rect.center = (450, 150)
            tradeSheep.on_mouse_click = self.tradeSheep
            self.text_widgets.append(tradeSheep)

            tradeBrick = TextWidget.TextWidget("Brick",
                                               (0, 0, 0), 30)
            tradeBrick.rect.center = (450, 200)
            tradeBrick.on_mouse_click = self.tradeBrick
            self.text_widgets.append(tradeBrick)

            tradeWood = TextWidget.TextWidget("Wood",
                                              (0, 0, 0), 30)
            tradeWood.rect.center = (450, 250)
            tradeWood.on_mouse_click = self.tradeWood
            self.text_widgets.append(tradeWood)

            tradeWheat = TextWidget.TextWidget("Wheat",
                                               (0, 0, 0), 30)
            tradeWheat.rect.center = (450, 300)
            tradeWheat.on_mouse_click = self.tradeWheat
            self.text_widgets.append(tradeWheat)

            tradeOre = TextWidget.TextWidget("Ore",
                                             (0, 0, 0), 30)
            tradeOre.rect.center = (450, 350)
            tradeOre.on_mouse_click = self.tradeOre
            self.text_widgets.append(tradeOre)


            tradeOne = TextWidget.TextWidget("1",
                                             (0, 0, 0), 30)
            tradeOne.rect.center = (550, 150)
            tradeOne.on_mouse_click = self.tradeOne
            self.text_widgets.append(tradeOne)

            tradeTwo = TextWidget.TextWidget("2",
                                             (0, 0, 0), 30)
            tradeTwo.rect.center = (550, 200)
            tradeTwo.on_mouse_click = self.tradeTwo
            self.text_widgets.append(tradeTwo)

            tradeThree = TextWidget.TextWidget("3",
                                               (0, 0, 0), 30)
            tradeThree.rect.center = (550, 250)
            tradeThree.on_mouse_click = self.tradeThree
            self.text_widgets.append(tradeThree)

            tradeFour = TextWidget.TextWidget("4",
                                              (0, 0, 0), 30)
            tradeFour.rect.center = (550, 300)
            tradeFour.on_mouse_click = self.tradeFour
            self.text_widgets.append(tradeFour)

            tradeFive = TextWidget.TextWidget("5",
                                              (0, 0, 0), 30)
            tradeFive.rect.center = (550, 350)
            tradeFive.on_mouse_click = self.tradeFive
            self.text_widgets.append(tradeFive)


            go_back = TextWidget.TextWidget("Go Back",
                                            (0, 0, 0), 30)
            go_back.rect.center = (100, 450)
            go_back.on_mouse_click = self.goBack
            self.text_widgets.append(go_back)

            trade = TextWidget.TextWidget("Trade",
                                            (0, 0, 0), 30)
            trade.rect.center = (550, 450)
            trade.on_mouse_click = self.trade
            self.text_widgets.append(trade)


            while self.continueBuildScreen:
                # Tick of the timer
                #self.timer.tick()
                self.event_loop()
                self.draw()

    def wantOne(self, event):
        self.desiredQuantity = 1

    def wantTwo(self, event):
        self.desiredQuantity = 2

    def wantThree(self, event):
        self.desiredQuantity = 3

    def wantFour(self, event):
        self.desiredQuantity = 4

    def wantFive(self, event):
        self.desiredQuantity = 5

    def tradeOne(self, event):
        self.undesiredQuantity = 1

    def tradeTwo(self, event):
        self.undesiredQuantity = 2

    def tradeThree(self, event):
        self.undesiredQuantity = 3

    def tradeFour(self, event):
        self.undesiredQuantity = 4

    def tradeFive(self, event):
        self.undesiredQuantity = 5


    def wantSheep(self, event):
        self.desiredResource = "W"

    def wantBrick(self, event):
        self.desiredResource = "B"

    def wantWood(self, event):
        self.desiredResource = "L"

    def wantWheat(self, event):
        self.desiredResource = "G"

    def wantOre(self, event):
        self.desiredResource = "O"

    def tradeSheep(self, event):
        self.undesiredResource = "W"

    def tradeBrick(self, event):
        self.undesiredResource = "B"

    def tradeWood(self, event):
        self.undesiredResource = "L"

    def tradeWheat(self, event):
        self.undesiredResource = "G"

    def tradeOre(self, event):
        self.undesiredResource = "O"

    def goBack(self, event):
        self.background.fill((229, 239, 255))
        self.continueBuildScreen = False
        self.catanGame.comeBackFromScreen()

    def trade (self, event):
        info = (self.desiredResource, self.desiredQuantity, self.undesiredResource, self.undesiredQuantity)
        
        if (self.curPlayer.checkResource(info[2],info[3])):
            tradePlayer.tradePlayer(self.catanGame,self.curNum, self.players, info)
        else:
            self.messageText = "You Don't have those resources"

    def event_loop(self):

        if (self.continueBuildScreen):
            for event in pygame.event.get():
                if (event.type == pygame.QUIT):
                    pygame.quit()
                    sys.exit()
                elif (event.type == pygame.MOUSEMOTION):
                    for text in self.text_widgets:
                        text.highlight = text.rect.collidepoint(event.pos)
                elif (event.type == pygame.MOUSEBUTTONDOWN):
                    for text in self.text_widgets:
                        text.on_mouse_button_down(event)
                elif (event.type == pygame.MOUSEBUTTONUP):
                    for text in self.text_widgets:
                        text.on_mouse_button_up(event)
                elif (event.type == TextWidget.TEXT_WIDGET_CLICK):
                    print (event.text_widget)
                self.draw()
        else:
            return


    def draw(self):
        rects = []
        rects.append(self.timer_update())

        text = "What Do You Want" 
        font = pygame.font.Font(None, 36)
        label = font.render(text, 1, (10, 10, 10))
        self.screen.blit (label, (50,100))
        rects += [(label.get_rect())]

        text = "What Are You Willing to Give up?" 
        font = pygame.font.Font(None, 36)
        label = font.render(text, 1, (10, 10, 10))
        self.screen.blit (label, (400,100))
        rects += [(label.get_rect())]

        font = pygame.font.Font(None, 36)
        label = font.render(self.messageText, 1, (10, 10, 10))
        self.screen.blit(label, (300, 600))
        rects += [(label.get_rect())]

        for text in self.text_widgets:
            rect = text.draw(self.screen)
            rects.append(rect)
        pygame.display.update(rects)


    def timer_update(self):
        """Update the Timer
        returns - pygame.rect - The rect that the timer
        needs to be redrawn, or None on error"""

        rect_return = None

        if (pygame.font):
            timer_string = "%.2f" % self.timer.get_fps()
            # basic font
            font = pygame.font.Font(None, 36)
            message = font.render(timer_string, 1, (147, 1, 16))
            if (message):
                rect_return = message.get_rect(left=0)
                rect_return.width += 25
                self.screen.blit(self.background, rect_return)
                #self.screen.blit(message, rect_return)

        return rect_return



    def on_exit_clicked(self, event):
        pygame.quit()
        sys.exit()

