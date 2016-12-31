import os
import sys
import pygame
import playCatan
import Player
import random
from pygame.locals import *

import TextWidget

TEXT_WIDGET_CLICK = pygame.locals.USEREVENT + 1

# http://www.learningpython.com/2006/12/13/textwidget-a-simple-text-class-for-pygame/
class build ():

    def __init__(self, curGame, curPlayer, width=850, height=650):
        self.curPlayer = curPlayer
        self.catanGame = curGame
        self.continueBuildScreen = True
        self.messageText = ""
        pygame.init()

        self.devCards = []
        self.drawDevCard = False
        for i in range(14):
            self.devCards += ["knight"]
        for i in range(4):
            self.devCards += ["VP"]


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

            # Text Widget list
            self.text_widgets = []
            # Create our Text WIdget

            build_road = TextWidget.TextWidget("Build Road",
                                               (0, 0, 0), 60)
            build_road.rect.center = self.screen.get_rect().center
            build_road.rect.top = 100
            build_road.on_mouse_click = self.buildRoad
            self.text_widgets.append(build_road)

            build_settlement = TextWidget.TextWidget("Build Settlement",
                                                     (0, 0, 0), 60)
            build_settlement.rect.center = self.screen.get_rect().center
            build_settlement.rect.top = build_road.rect.bottom + 30
            build_settlement.on_mouse_click = self.buildSettlement
            self.text_widgets.append(build_settlement)

            build_city = TextWidget.TextWidget("Build City",
                                               (0, 0, 0), 60)
            build_city.rect.center = self.screen.get_rect().center
            build_city.rect.top = build_settlement.rect.bottom + 30
            build_city.on_mouse_click = self.buildCity
            self.text_widgets.append(build_city)


            get_development = TextWidget.TextWidget("Get Development Card",
                                                    (0, 0, 0), 60)
            get_development.rect.center = self.screen.get_rect().center
            get_development.on_mouse_click = self.getDevCard
            get_development.rect.top = build_city.rect.bottom + 30
            self.text_widgets.append(get_development)

            go_back = TextWidget.TextWidget("Go Back",
                                            (0, 0, 0), 60)
            go_back.rect.center = self.screen.get_rect().center
            go_back.rect.top = get_development.rect.bottom + 30
            go_back.on_mouse_click = self.goBack
            self.text_widgets.append(go_back)

            while self.continueBuildScreen:
                # Tick of the timer
                #self.timer.tick()
                self.event_loop()
                self.draw()


    # not going to check if can build settlement yet 
    def buildRoad(self, event):
        # has the resources to build the road
        if (self.curPlayer.canPlaceRoad()):
            self.background.fill((255, 255, 255))
            self.continueBuildScreen = False
            self.catanGame.gobuildRoad()

        #self.messageText = "You Don't Have The Resources to Build This"

    def buildSettlement(self, event):

        # has the resources to build a settlement
        if (self.curPlayer.canBuildSettlement()):
            self.background.fill((255, 255, 255))
            self.continueBuildScreen = False
            self.catanGame.goBackToBuildSettlement()

        #self.messageText = "You Don't Have The Resources to Build This"

    def getDevCard(self, event):
        if (self.curPlayer.canGetDevCard()):
            self.background.fill((229, 239, 255))
            randIndex = random.randint(1, len(self.devCards) - 1)
            newDevCard = self.devCards [randIndex]

            self.curPlayer.updateDevResource()
            
            if (newDevCard == "VP"):
                self.curPlayer.incVP()
            else:
                self.curPlayer.addDevCard(newDevCard)
                devImg = pygame.image.load(newDevCard + ".png")
                self.background.blit(devImg, (650, 500))


        self.messageText = "You Don't Have The Resources to Build This"

    def buildCity(self, event):
        # has the resources to build a city
        if (self.curPlayer.canBuildCity()):
            self.background.fill((255, 255, 255))
            self.continueBuildScreen = False
            self.catanGame.buildCity()
        self.messageText = "You Don't Have The Resources to Build This"

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
                elif (event.type == pygame.K_SPACE):
                    if (self.drawDevCard == True):
                        self.catanGame.main_loop()
                elif (event.type == TextWidget.TEXT_WIDGET_CLICK):
                    print (event.text_widget)
                self.draw()
        else:
            return

    def goBack(self, event):
        self.background.fill((255, 255, 255))
        self.continueBuildScreen = False
        self.catanGame.comeBackFromScreen()

    def draw(self):
        rects = []

        font = pygame.font.Font(None, 36)
        label = font.render(self.messageText, 1, (10, 10, 10))
        self.screen.blit(label, (300, 600))
        rects += [(label.get_rect())]

        rects.append(self.timer_update())
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

