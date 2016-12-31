import os
import sys
import pygame
import playCatan
import Instructions
from pygame.locals import *

import TextWidget
TEXT_WIDGET_CLICK = pygame.locals.USEREVENT + 1

#Pictures
# city http://clipartix.com/wp-content/uploads/2016/07/Castle-clip-art-at-vector-clip-art-image.png
#hexagons https://d13yacurqjgara.cloudfront.net/users/50008/screenshots/1828250/catanicons.jpg
#knight http://clipartix.com/wp-content/uploads/2016/06/Free-knight-clipart-the-cliparts-2.png

# http://www.learningpython.com/2006/12/13/textwidget-a-simple-text-class-for-pygame/
class splashScreen ():

    def __init__(self, width=850, height=650):
        pygame.init()
        # create the screen
        self.playingGame = False
        self.screen = pygame.display.set_mode((width, height), 0)
        self.background = pygame.Surface(self.screen.get_size(), SWSURFACE)
        self.background = self.background.convert()

            # Just fill with a solid colour
        self.background.fill((229, 239, 255))


        self.screen.blit(self.background, (0, 0))



    def main_loop(self):

        pygame.display.update()
        self.timer = pygame.time.Clock()

        # Text Widget list
        self.text_widgets = []
        # Create our Text WIdget

        self.title = TextWidget.TextWidget("Settlers of Catan",
                                           (0, 0, 0), 70)
        self.title.rect.center = self.screen.get_rect().center
        self.title.rect.top = 100
        self.text_widgets.append(self.title)


        self.new_game_text = TextWidget.TextWidget("New Game",
                                                   (0, 0, 0), 60)
        self.new_game_text.rect.center = self.screen.get_rect().center
        self.new_game_text.rect.top = 200
        self.text_widgets.append(self.new_game_text)
        self.new_game_text.on_mouse_click = self.playGame

        self.website_text = TextWidget.TextWidget("Instructions",
                                                  (0, 0, 0), 60)
        self.website_text.rect.center = self.screen.get_rect().center
        self.website_text.rect.top = self.new_game_text.rect.bottom + 30
        self.website_text.on_mouse_click = self.switchtoInstructions
        self.text_widgets.append(self.website_text)

        # Different font for the last one, and let's make it increase
        # more
        self.exit_text = TextWidget.TextWidget("Exit", (0, 0, 0), 60, 40,
                                               pygame.font.match_font("sans",
                                               False, True))
        self.exit_text.rect.center = self.screen.get_rect().center
        self.exit_text.rect.top = self.website_text.rect.bottom + 30
        # override the on_mouse_click event
        self.exit_text.on_mouse_click = self.on_exit_clicked
        self.text_widgets.append(self.exit_text)

        while 1:
            # Tick of the timer
            #self.timer.tick()
            self.event_loop()
            self.draw()

    def playGame(self, event):
        self.background.fill((229, 239, 255))
        self.playingGame = True 
        playCatan.playCatan()

    def switchtoInstructions (self,event):
        Instructions.instructions()


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


if __name__ == "__main__":
    text = splashScreen()
    text.main_loop()
