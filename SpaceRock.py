# This file contains the SpaceRock class
# from pygame import (
#                     image,
#                     transform,
#                     sprite
# )
import pygame
from Calculations import (
                    find_force,
                    radar_coord_conversion
                    )
from config import *
from pygame.locals import RLEACCEL


# Create a class for the space rocks extending pygame sprite class
class SpaceRock(pygame.sprite.Sprite):
    def __init__(self, id, mass, color, position_x, position_y, velocity_x, velocity_y):
        super(SpaceRock,self).__init__()

        # Position and Velocity parameters initialized
        self.velocity = [velocity_x, velocity_y]
        self.id = id
        self.color = color

        # Choose meteor soze based on color
        if color == "Brown":

            # Choose meteor size based on mass
            if mass == 'SMALL_MASS':
                image = "Graphics/meteorBrown_tiny1.png"
                size = (10,10)
                self.mass = SMALL_MASS
            elif mass == 'MED_MASS':
                image = "Graphics/meteorBrown_med3.png"
                size = (20,20)
                self.mass = MED_MASS
            elif mass == 'BIG_MASS':
                image = "Graphics/meteorBrown_big2.png"
                size = (40,40)
                self.mass = BIG_MASS
            elif mass == 'HUGE_MASS':
                image = "Graphics/meteorBrown_big2.png"
                size = (55,55)
                self.mass = HUGE_MASS
        else:
            # Choose meteor size based on mass
            if mass == 'SMALL_MASS':
                image = "Graphics/meteorGrey_tiny2.png"
                size = (10,10)
                self.mass = SMALL_MASS
            elif mass == 'MED_MASS':
                image = "Graphics/meteorGrey_med2.png"
                size = (20,20)
                self.mass = MED_MASS
            elif mass == 'BIG_MASS':
                image = "Graphics/meteorGrey_big1.png"
                size = (40,40)
                self.mass = BIG_MASS
            elif mass == 'HUGE_MASS':
                image = "Graphics/meteorGrey_big1.png"
                size = (45,45)
                self.mass = HUGE_MASS

        # Create pygame Surface
        self.surface = pygame.image.load(image)
        self.surface = pygame.transform.scale(self.surface, size)
        self.surface.set_colorkey((0,0,0), RLEACCEL)
        self.rect = self.surface.get_rect( center = (position_x,position_y) )

        # Create radar point parameters
        self.radar_point_position = [0,0]
        self.radar_point_color = 'Red'

        self.radar_point_size = 2

    def change_size(self):
        """ Change the size of the space rock based on it's mass"""

        if self.mass > 2*BIG_MASS:
            self.surface = pygame.transform.scale(self.surface, (80,80))
            self.surface.set_colorkey((0,0,0), RLEACCEL)

        if self.mass > 6*BIG_MASS:
            self.surface = pygame.transform.scale(self.surface, (120,120))
            self.surface.set_colorkey((0,0,0), RLEACCEL)

    def display(self, screen, screen_col, screen_row, win_width, win_height):

        # Blit the space rock to the screen
        screen.blit(self.surface,[
                        self.rect.left + (-screen_col*win_width),
                        self.rect.top + (-screen_row*win_height)])

        # Blit the radar point to the screen
        pygame.draw.rect(
                        screen,
                        self.radar_point_color,
                        (self.radar_point_position[0],
                          self.radar_point_position[1],
                          self.radar_point_size,
                          self.radar_point_size))

    def update(self, all_sprites, map_rect, screen, screen_col, screen_row, win_width, win_height, radar_rect):

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
        if self.rect.left < (map_rect.left - win_width/2) or self.rect.right > (map_rect.right + win_width/2):
            self.kill()
        if self.rect.top < (map_rect.top - win_height*2) or self.rect.bottom > (map_rect.bottom + win_height/2):
            self.kill()

        # Update the radar point
        self.radar_point_position = radar_coord_conversion(
                                                            self.rect.left,
                                                            self.rect.top,
                                                            RADAR_REDUCTION,
                                                            radar_rect,
                                                            map_rect)

        # Blit the space rock to the screen
        self.display(screen, screen_col, screen_row, win_width, win_height)
