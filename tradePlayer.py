import os
import sys
import pygame
import playCatan
import Player
from pygame.locals import *

import TextWidget

TEXT_WIDGET_CLICK = pygame.locals.USEREVENT + 1

class tradePlayer ():

    def __init__(self, curGame, curNum, players, info, width=850, height=650):
        self.curNum = curNum
        self.catanGame = curGame
        self.players = players
        self.curPlayer = self.players[self.curNum % 4]
        self.info = info
        self.goThru = 0
        self.messageText = ""
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

        pygame.display.update()
        self.timer = pygame.time.Clock()

        # Text Widget list
        self.text_widgets = []
        # Create our Text WIdget

        yes = TextWidget.TextWidget("Yes",
                                    (0, 0, 0), 30)
        yes.rect.center = (300, 250)
        yes.on_mouse_click = self.yes
        self.text_widgets.append(yes)

        no = TextWidget.TextWidget("No",
                                    (0, 0, 0), 30)
        no.rect.center = (350, 250)
        no.on_mouse_click = self.no
        self.text_widgets.append(no)

        while True:
            # Tick of the timer
            #self.timer.tick()
            self.event_loop()
            self.draw()

    # you go back to the main screen and subtract and add accordingly
    def yes(self, event):
        self.continueBuildScreen = False
        self.background.fill((255, 255, 255))

        index = self.goThru

        if (self.players[index].checkResource(self.info[0], self.info[1])):
            self.catanGame.tradeEverything(self.curNum, self.goThru, self.info)
        else:
            self.messageText = "You Can't Trade, click No"
    # you continue the player
    def no (self, event):
        self.goThru += 1
        if (self.goThru == self.curNum):
            self.goThru += 1

        if (self.goThru == 4):
            continueBuildScreen = False
            self.catanGame.main_loop()
            self.background.fill((255, 255, 255))

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

        if (self.goThru == self.curNum):
            self.goThru += 1

        text = "Player %d" % (self.goThru + 1)
        font = pygame.font.Font(None, 36)
        label = font.render(text, 1, (10, 10, 10))
        self.screen.blit(label, (275, 100))
        rects += [(label.get_rect())]
        offertext = "Do You want %d %s for %d %s ?" % (self.info[3], self.info[2],
                                                        self.info[1], self.info[0])
        
        font = pygame.font.Font(None, 36)
        offer = font.render(offertext, 1, (10, 10, 10))
        self.screen.blit(offer, (275, 150))
        rects += [(offer.get_rect())]

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

