# This file contains the SpaceRock class
# from pygame import (
#                     image,
#                     transform,
#                     sprite
# )
import pygame
from Calculations import find_force
from config import *
from pygame.locals import RLEACCEL


# Create a class for the space rocks extending pygame sprite class
class SpaceRock(pygame.sprite.Sprite):
    def __init__(self,mass,position_x,position_y,velocity_x,velocity_y,id):
        super(SpaceRock,self).__init__()

        # Mass, Position and Velocity parameters initialized
        self.mass = mass
        self.velocity = [velocity_x, velocity_y]
        self.id = id

        # Choose metor size based on mass
        if mass == min(MASSES):
            image = "Graphics/meteorBrown_tiny1.png"
            size = (10,10)
        elif mass == max(MASSES):
            image = "Graphics/meteorBrown_med3.png"
            size = (40,40)
        else:
            image = "Graphics/meteorBrown_big2.png"
            size = (20,20)
        # Create pygame Surface
        self.surface = pygame.image.load(image)
        self.surface = pygame.transform.scale(self.surface, size)
        self.surface.set_colorkey((0,0,0), RLEACCEL)
        self.rect = self.surface.get_rect( center = (position_x,position_y) )

    def change_size(self):
        """ Change the size of the space rock based on it's mass"""
        if self.mass > 2*big_rock:
            self.surface = pygame.transform.scale(self.surface, (80,80))
            self.surface.set_colorkey((0,0,0), RLEACCEL)
        if self.mass > 4*big_rock:
            self.surface = pygame.transform.scale(self.surface, (120,120))
            self.surface.set_colorkey((0,0,0), RLEACCEL)

    def update(self, all_sprites, map_rect):

        # Calculate force on object
        force = find_force(all_sprites, self.rect[0], self.rect[1], self.mass, self.id)

        # Give the rocks a little force to keep them from clustering at the edges
        if self.rect[0] < 0:
            force[0]+= helper_force
        elif self.rect[0] > 1000:
            force[0]-= helper_force

        if self.rect[1] < 0:
            force[1]+= helper_force
        elif self.rect[1] > 1000:
            force[1]-= helper_force

        # Update acceleration
        acceleration_x = force[0]/(self.mass*framerate*framerate)
        acceleration_y = force[1]/(self.mass*framerate*framerate)
        # Update object's velocity
        self.velocity[0] += acceleration_x
        self.velocity[1] += acceleration_y

        # Update the rectangle coordinates
        self.rect.move_ip(self.velocity[0],self.velocity[1])

        # Remove space rock if it gets too far away
        if self.rect.left < map_rect.left or self.rect.right > map_rect.right:
            self.kill()
        if self.rect.top < map_rect.top or self.rect.bottom > map_rect.bottom:
            self.kill()
