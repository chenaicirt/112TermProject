import os
import sys
import pygame
import TermProject
from pygame.locals import *

import TextWidget

TEXT_WIDGET_CLICK = pygame.locals.USEREVENT + 1

# http://www.learningpython.com/2006/12/13/textwidget-a-simple-text-class-for-pygame/
class instructions ():

    def __init__(self, width=850, height=650):

        pygame.init()
        # create the screen

        self.screen = pygame.display.set_mode((width, height), 0)
        self.background = pygame.Surface(self.screen.get_size(), SWSURFACE)
        self.background = self.background.convert()

        self.background.fill((229, 239, 255))

        self.img = pygame.image.load("Instructions.png")
        self.rect = self.img.get_rect()
        self.screen.blit(self.img,(10,10))
        pygame.display.flip()


        self.screen.blit(self.background, (0, 0))
        self.main_loop()



    def main_loop(self):

      
            pygame.display.update()
            self.timer = pygame.time.Clock()

            # Text Widget list
            self.text_widgets = []
            # Create our Text WIdget

            go_back = TextWidget.TextWidget("Go Back",
                                            (0, 0, 0), 40)
            go_back.rect.center = (650,600)
            go_back.on_mouse_click = self.goBack
            self.text_widgets.append(go_back)
            
            while True:
                # Tick of the timer
                #self.timer.tick()
                self.event_loop()
                self.draw()


    def goBack(self, event):
        self.background.fill((229, 239, 255))
        TermProject.splashScreen().main_loop()


    def event_loop(self):

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


    def draw(self):
        rects = []
        rects.append(self.timer_update())
        self.screen.blit (self.img, self.rect)
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

