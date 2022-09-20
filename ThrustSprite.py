# This contains a class for thrust sprites, the mass ejected from the blob
import pygame
from math import log

pygame.init()

class ThrustSprite(pygame.sprite.Sprite):
    """ThrustSprite is a little pixel of mass ejected from the player."""

    def __init__(self, x_pos, y_pos, mass, direction):
        super(ThrustSprite, self).__init__()
        self.speed = 20
        self.direction = direction
        self.count = 0

        size = 0
        if mass > 100000:
            size = 1
        if mass > 5000000:
            size = 5
        if mass > 20000000:
            size = 10
        if mass > 50000000:
            size = 20

        self.surface = pygame.Surface((size,size))
        self.surface.fill(('Green'))
        self.rect = self.surface.get_rect( center = (x_pos,y_pos))

    def update(self):

        if self.direction == 'left':
            self.rect.move_ip(-self.speed,0)
        if self.direction == 'right':
            self.rect.move_ip(self.speed,0)
        if self.direction == 'up':
            self.rect.move_ip(0,-self.speed)
        if self.direction == 'down':
            self.rect.move_ip(0,self.speed)

        # Remove sprite when it gets too far away
        if self.count > 10:
            self.kill()
        self.count+=1
