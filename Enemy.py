# This file contains the Enemy class

import pygame
import random

from Calculations import (
                    elastic_momentum,
                    momentum,
                    find_force,
                    radar_coord_conversion
                    )
from config import *
from math import fabs
from pygame.locals import RLEACCEL
from ThrustSprite import ThrustSprite

class Enemy(pygame.sprite.Sprite):
    """This is the enemy sprite"""
    def __init__(self, mass, x_size, y_size):
        super(Enemy,self).__init__()

        # Mass, Position and Velocity parameters initialized
        self.mass = mass
        self.velocity = [1,-2]
        self.size = [x_size, y_size]
        self.id = 1000

        # Create pygame Surface
        self.surface = pygame.image.load("Graphics/GreenBlob.png")
        self.surface = pygame.transform.scale(self.surface, self.size)
        self.surface.set_colorkey((0,0,0), RLEACCEL)
        self.rect = self.surface.get_rect( center = (1000,1000) )

        # Thrust sound and group
        self.thrust_sound = pygame.mixer.Sound(thrust_sound_location)
        self.thrust_sound.set_volume(.5)
        self.thrust_group = pygame.sprite.Group()
        self.percent_ejection = ENEMY_PERCENT_EJECTION

        # Only allow the enemy to thrust at a certain frequency
        self.thrust_count = pygame.USEREVENT + 1
        pygame.time.set_timer(self.thrust_count, 3)

        # Collision Sound
        self.collision_sound = pygame.mixer.Sound(gulp_sound_location)
        self.collision_sound.set_volume(.15)

        # Create radar point parameters
        self.radar_point_position = [0,0]
        self.radar_point_color = 'Yellow'
        self.radar_point_size = 2

    def thrust(self, direction):

        # Create a new thrust sprite and add it to the group
        ejected = ThrustSprite(self.rect.centerx,self.rect.centery,self.mass,direction)
        self.thrust_group.add(ejected)

        # Update the mass
        self.mass *= 1-self.percent_ejection

        # Play a sound
        self.thrust_sound.play()

        # Calculate and return the amount of force
        return self.mass*self.percent_ejection*thrust_acc

    def display(self, screen, screen_col, screen_row, win_width, win_height):

        # Blit the enemy to the screen
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

        # Blit the thrust group to the screen
        for sprite in self.thrust_group:
            sprite.display(
                            screen,
                            screen_col,
                            screen_row,
                            win_width,
                            win_height)

    def collision(self, rock, grey_collision_flag):

        # If it's a brown rock, then kill the space rock and add the rock's mass to the enemy mass
        if rock.id < 200:
            print( "your enemy just ate ",rock.mass,"kg" )
            self.mass += rock.mass
            self.velocity = [momentum(self.mass,self.velocity[0], rock.mass, rock.velocity[0])/2,
                            momentum(self.mass,self.velocity[1], rock.mass, rock.velocity[1])/2]
            self.collision_sound.play()
            rock.kill()

            return 1
        # If it's a grey rock, update the enemy and rock velocities
        else:

            if grey_collision_flag:
                # Elastic collision
                final_x_velocities = elastic_momentum(self.mass, self.velocity[0], rock.mass, rock.velocity[0])
                final_y_velocities = elastic_momentum(self.mass, self.velocity[1], rock.mass, rock.velocity[1])
                self.velocity[0] = BOUNCE_SLOW_PERCENT*final_x_velocities[0]
                self.velocity[1] = BOUNCE_SLOW_PERCENT*final_y_velocities[0]
                rock.velocity[0] = BOUNCE_SLOW_PERCENT*final_x_velocities[1]
                rock.velocity[1] = BOUNCE_SLOW_PERCENT*final_y_velocities[1]

            return 0

    def sense(self, all_sprites):
        """ Alows the enemy to move in the optimal direction"""

        horizontal = 0
        vertical = 0
        # Give a thrust in the direction of the most rocks
        for rock in all_sprites:
            # rock is to the right of the enemy
            if rock.rect.centerx - self.rect.centerx > 0:
                horizontal += 1
            else:
                horizontal -= 1
            # rock is below the enemy
            if rock.rect.centery - self.rect.centery > 0:
                vertical += 1
            else:
                vertical -= 1

        # Return true for most rocks to the right, and false for most rocks to the left
        # And return true for most rocks below, and false for most rocks above
        return [horizontal > 0, vertical > 0]

    # Move the sprite based on AI logic
    def update(self, all_sprites, key_down_flag, pressed_keys, screen, screen_col, screen_row, win_width, win_height, map_rect, radar_rect):

        x_thrust = 0
        y_thrust = 0

        # Check if any thrust is needed
        for event in pygame.event.get():
            if event.type == self.thrust_count:
                sense = self.sense(all_sprites)
                print(sense)
                print("v=", self.velocity)
                # Check the horizontal for rock majority to the right
                if sense[0]:
                    if self.velocity[0] <= 1.5:
                        x_thrust = self.thrust('right')
                # Otherwise rock majority is to the left
                else:
                    if self.velocity[0] >= -1.5:
                        x_thrust = -self.thrust('left')

                if sense[1]:
                    # Check the vertical for rock majority below
                    if self.velocity[1] <= 1.5:
                        y_thrust = self.thrust('down')
                # Otherwise rock majority is above
                else:
                    if self.velocity[1] >= -1.5:
                        y_thrust = -self.thrust('up')

        # Calculate force on object
        force = find_force(all_sprites, self.rect[0], self.rect[1], self.mass, self.id)

        # Update acceleration
        acceleration_x = (force[0]+x_thrust)/(self.mass*framerate*framerate)
        acceleration_y = (force[1]+y_thrust)/(self.mass*framerate*framerate)

        # Update object's velocity
        self.velocity[0] += acceleration_x
        self.velocity[1] += acceleration_y

        # Find the displacement in position
        self.rect.move_ip(self.velocity[0],self.velocity[1])

        # Update the radar point
        self.radar_point_position = radar_coord_conversion(
                                                            self.rect.left,
                                                            self.rect.top,
                                                            RADAR_REDUCTION,
                                                            radar_rect,
                                                            map_rect)

        # Update thrust group
        self.thrust_group.update(
                                screen,
                                screen_col,
                                screen_row,
                                win_width,
                                win_height)


        self.display(screen, screen_col, screen_row, win_width, win_height)
