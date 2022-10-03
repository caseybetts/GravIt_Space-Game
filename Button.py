# This file contains the Button class

import pygame

from config import *
from Setup import *


class Button():
    """Created a button to place on the screen."""

    def __init__(self, x, y, scale, image, text):
        img_width = image.get_width()
        img_height = image.get_height()

        self.image = pygame.transform.scale(image, (int(img_width*scale), int(img_height*scale)))
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect( center = (x,y) )

        # Text
        self.font = pygame.font.Font(pygame.font.get_default_font(), int(60*scale))
        self.text = self.font.render(text,False, 'Black')
        self.text_rect = self.text.get_rect(
                            center = (  self.rect.x + self.image.get_width()/2,
                                        self.rect.y + self.image.get_height()/2)
                                        )
        self.clicked = False

    def check_mouse(self):

        action = False

        # Get mouse position
        pos = pygame.mouse.get_pos()

        # Check for mouse over and clicked condition
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True

            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

        return action



def real_button_action():
    print('real_button_action')
    rocks = setup.make_random_rocks(number_of_rocks)
