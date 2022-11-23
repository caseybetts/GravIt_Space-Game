# This contains a class for thrust sprites, the mass ejected from the blob
import pygame

from config import *
from math import log

pygame.init()

class ThrustSprite(pygame.sprite.Sprite):
    """ThrustSprite is a little pixel of mass ejected from the player."""

    def __init__(self, x_pos, y_pos, mass, direction, color):
        super(ThrustSprite, self).__init__()
        self.speed = 30
        self.direction = direction
        self.count = 0

        size = 0
        if mass > PLAYER_START_MASS:
            size = 1
        elif mass > PLAYER_START_MASS*1.4:
            size = 5
        if mass > PLAYER_START_MASS*1.8:
            size = 10
        if mass > PLAYER_START_MASS*2.6:
            size = 20

        self.surface = pygame.Surface((size,size))
        self.surface.fill((color))
        self.rect = self.surface.get_rect( center = (x_pos,y_pos))

    def display(self, screen, screen_col, screen_row, win_width, win_height):

        # Blit the thrust sprite to the screen
        screen.blit(self.surface,[
                        self.rect.left + (-screen_col*win_width),
                        self.rect.top + (-screen_row*win_height)])

    def update(self, screen, screen_col, screen_row, win_width, win_height):

        if self.direction == 'left':
            self.rect.move_ip(self.speed,0)
        if self.direction == 'right':
            self.rect.move_ip(-self.speed,0)
        if self.direction == 'up':
            self.rect.move_ip(0,self.speed)
        if self.direction == 'down':
            self.rect.move_ip(0,-self.speed)

        # Remove sprite when it gets too far away
        if self.count > 10:
            self.kill()
        self.count+=1

        self.display(screen, screen_col, screen_row, win_width, win_height)
