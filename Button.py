# This file contains the Button class

import pygame

from config import *
from Setup import *


class Button():
    """Create a button to place on the screen."""

    def __init__(self, x, y, scale, text, text_color, alpha, image=""):

        # Load the image
        if image:
            img_width = image.get_width()
            img_height = image.get_height()
            self.image = pygame.transform.scale(image, (int(img_width*scale), int(img_height*scale)))
            self.image.set_colorkey((0,0,0))
            self.image.set_alpha(alpha)
            self.rect = self.image.get_rect( center = (x,y) )

        # Text
        self.font = pygame.font.Font(pygame.font.get_default_font(), int(60*scale))
        self.text = self.font.render(text,False, text_color)

        # Sound
        self.button_sound = pygame.mixer.Sound(button_sound_location)
        self.button_sound.set_volume(.5)

        # Create a rect attribute based on the image. If no image, then based on the text
        if image:
            self.text_rect = self.text.get_rect(
                            center = (  self.rect.x + self.image.get_width()/2,
                                        self.rect.y + self.image.get_height()/2)
                                        )
        else:
            self.text_rect = self.text.get_rect( center = (x,y))
            self.rect = self.text_rect

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
