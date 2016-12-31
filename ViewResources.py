import os
import sys
import pygame
import playCatan
import Player
from pygame.locals import *

import TextWidget

TEXT_WIDGET_CLICK = pygame.locals.USEREVENT + 1

# http://www.learningpython.com/2006/12/13/textwidget-a-simple-text-class-for-pygame/
class resource ():

    def __init__(self, curGame, curPlayer, width=850, height=650):
        self.curPlayer=curPlayer
        self.catanGame=curGame
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

            # Text Widget list
            self.text_widgets = []
            # Create our Text WIdget

            go_back = TextWidget.TextWidget("Go Back",
                                            (0, 0, 0), 60)
            go_back.rect.center = (425,450)
            go_back.on_mouse_click = self.goBack
            self.text_widgets.append(go_back)
            
            while self.continueBuildScreen:
                # Tick of the timer
                #self.timer.tick()
                self.event_loop()
                self.draw()


    def goBack(self, event):
        self.background.fill((229, 239, 255))
        self.continueBuildScreen=False
        self.catanGame.comeBackFromScreen()


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

        text = "Brick: %d" %(self.curPlayer.resources["B"])
        font = pygame.font.Font(None, 36)
        label = font.render(text, 1, (10, 10, 10))
        self.screen.blit (label, (375,100))
        rects += [(label.get_rect())]

        text = "Wood: %d" % self.curPlayer.resources["L"]
        font = pygame.font.Font(None, 36)
        label = font.render(text, 1, (10, 10, 10))
        self.screen.blit (label, (375,150))
        rects += [(label.get_rect())]

        text = "Wheat: %d" % self.curPlayer.resources["G"]
        font = pygame.font.Font(None, 36)
        label = font.render(text, 1, (10, 10, 10))
        self.screen.blit (label, (375,200))
        rects += [(label.get_rect())]

        text = "Sheep: %d" % self.curPlayer.resources["W"]
        font = pygame.font.Font(None, 36)
        label = font.render(text, 1, (10, 10, 10))
        self.screen.blit (label, (375,250))
        rects += [(label.get_rect())]

        text = "Ore: %d" % self.curPlayer.resources["O"]
        font = pygame.font.Font(None, 36)
        label = font.render(text, 1, (10, 10, 10))
        self.screen.blit (label, (375,300))
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

