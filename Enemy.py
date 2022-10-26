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

    # Must pass in a mass (int), size (int), postion (2 element list), velocity (2 element list)
    def __init__(self, id, mass, size, position, velocity):
        super(Enemy,self).__init__()

        # Mass, Position and Velocity parameters initialized
        self.mass = mass
        self.velocity = velocity
        self.position = position
        self.id = id

        # Create pygame Surface
        self.surface = pygame.image.load(enemy_image_location)
        self.surface = pygame.transform.scale(self.surface, [size,size])
        self.surface.set_colorkey((0,0,0), RLEACCEL)
        self.rect = self.surface.get_rect( center = position )

        # Thrust parameters
        self.thrust_sound = pygame.mixer.Sound(thrust_sound_location)
        self.thrust_sound.set_volume(.5)
        self.thrust_group = pygame.sprite.Group()
        self.percent_ejection = ENEMY_PERCENT_EJECTION
        self.thrust_direction = ['left', 'up']
        self.thrust_mass_multiplyer = self.percent_ejection*thrust_acc

        # Only allow the enemy to thrust at a certain frequency
        self.thrust_count = pygame.USEREVENT + 2
        pygame.time.set_timer(self.thrust_count, 500)

        # Collision Sound
        self.collision_sound = pygame.mixer.Sound(gulp_sound_location)
        self.collision_sound.set_volume(.15)

        # Create radar point parameters
        self.radar_point_position = [0,0]
        self.radar_point_color = 'Yellow'
        self.radar_point_size = 2

        # Sensor parameters
        self.player_in_proximity_flag = False
        self.enemy_in_proximity_flag = False
        self.rock_quadrant_majority = [0, 0]

        # Collision parameters
        self.enemy_collision_flag = False
        self.player_collision_flag = False
        self.grey_rock_collision_flag = False

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

    def collision(self, type, sprite):

        # If the collision is with the player, update the rock velocities to bounce off
        if type == "Player":
            print("Collision with player. Flag=", self.player_collision_flag)
            if not self.player_collision_flag:
                print("Enemy bounced off player. Start Vs", self.velocity)
                # Elastic collision
                final_x_velocities = elastic_momentum(self.mass, self.velocity[0], sprite.mass, sprite.velocity[0])
                final_y_velocities = elastic_momentum(self.mass, self.velocity[1], sprite.mass, sprite.velocity[1])
                self.velocity[0] = BOUNCE_SLOW_PERCENT*final_x_velocities[0]
                self.velocity[1] = BOUNCE_SLOW_PERCENT*final_y_velocities[0]
                self.player_collision_flag = True
                print("Final Vs", self.velocity)

        # If it's a grey rock, update the enemy velocity to bounce off
        elif type == "Enemy":

            if not self.enemy_collision_flag:
                # Elastic collision
                final_x_velocities = elastic_momentum(self.mass, self.velocity[0], sprite.mass, sprite.velocity[0])
                final_y_velocities = elastic_momentum(self.mass, self.velocity[1], sprite.mass, sprite.velocity[1])
                self.velocity[0] = BOUNCE_SLOW_PERCENT*final_x_velocities[0]
                self.velocity[1] = BOUNCE_SLOW_PERCENT*final_y_velocities[0]
                self.enemy_collision_flag = True

        # If it's a grey rock, update the enemy velocity to bounce off
        elif type == "Grey":

            if not self.grey_rock_collision_flag:
                # Elastic collision
                final_x_velocities = elastic_momentum(self.mass, self.velocity[0], sprite.mass, sprite.velocity[0])
                final_y_velocities = elastic_momentum(self.mass, self.velocity[1], sprite.mass, sprite.velocity[1])
                self.velocity[0] = BOUNCE_SLOW_PERCENT*final_x_velocities[0]
                self.velocity[1] = BOUNCE_SLOW_PERCENT*final_y_velocities[0]
                self.grey_rock_collision_flag = True

        # If it's a brown rock, add the rock's mass to the enemy mass and kill the rock
        if type == "Brown":
            print( "your enemy just ate ",sprite.mass,"kg" )
            self.mass += sprite.mass
            self.velocity = [momentum(self.mass,self.velocity[0], sprite.mass, sprite.velocity[0])/2,
                            momentum(self.mass,self.velocity[1], sprite.mass, sprite.velocity[1])/2]
            self.collision_sound.play()
            sprite.kill()

    def sense(self, all_sprites):
        """ Alows the enemy to move in the optimal direction"""

        horizontal = 0
        vertical = 0

        for sprite in all_sprites:

            # Check if the player is in proximity
            if sprite.id == 0:
                # Calculate the distance to the player
                range_x = fabs(sprite.rect.centerx - self.rect.centerx)
                range_y = fabs(sprite.rect.centery - self.rect.centery)

                if self.player_in_proximity_flag:
                    if range_x > 1000 or range_y > 1000:
                        self.player_in_proximity_flag = False
                else:
                    if  range_x < 1000 and range_y < 1000:
                        self.player_in_proximity_flag = True

            # Check if another enemy is in proximity
            if sprite.id > 1000:
                # Calculate the distance to other enemies
                range_x = fabs(sprite.rect.centerx - self.rect.centerx)
                range_y = fabs(sprite.rect.centery - self.rect.centery)

                if range_x < 100 and range_y < 100:
                    self.enemy_in_proximity_flag = True

            # Determine which direction (left/right and up/down) there are the most rocks

            # rock is to the right of the enemy
            if self.rect.centerx - sprite.rect.centerx  < 0:
                horizontal += 1
            else:
                horizontal -= 1

            # rock is below the enemy
            if self.rect.centery - sprite.rect.centery  < 0:
                vertical += 1
            else:
                vertical -= 1

        # Positive numbers indicate a majority of the rocks to the right or below the enemy
        # Negative numbers indicate a majority of the rocks to the left or above the enemy
        self.rock_quadrant_majority = [horizontal, vertical]

    def think(self):
        """ This function decides if the sprite should thruse in any direction
            and will update the thrust variable accordingly"""

        speeding = False

        # Horizontal speed check; slow the enemy if it's going too fast
        if self.velocity[0] > ENEMY_TOP_SPEED:
            self.thrust_direction[0] = 'left'
            speeding = True
        elif self.velocity[0] < -ENEMY_TOP_SPEED:
            self.thrust_direction[0] = 'right'
            speeding = True

        # Vertical speed check; slow the enemy if it's going too fast
        if self.velocity[1] > ENEMY_TOP_SPEED:
            self.thrust_direction[1] = 'up'
            speeding = True
        elif self.velocity[1] < -ENEMY_TOP_SPEED:
            self.thrust_direction[1] = 'down'
            speeding = True

        # No more thrust consideration is needed if the sprite is speeding
        if speeding == True:
            print("speeding!   ", self.id)
            return 0

        # Check if the majority of the rocks are to the right
        if self.rock_quadrant_majority[0] > 6:
            # Check if the enemy is already moving to the right
            if self.velocity[0] <= 1.5:
                self.thrust_direction[0] = 'right'

        # Otherwise rock majority is to the left
        elif self.rock_quadrant_majority[0] < -6:
            if self.velocity[0] >= -1.5:
                self.thrust_direction[0] = 'left'
        else:
            self.thrust_direction[0] = 'None'

        # Check if the majority of the rocks are below
        if self.rock_quadrant_majority[1] > 6:
            # Check if the enemy is already moving down
            if self.velocity[1] <= 1.5:
                self.thrust_direction[1] = 'down'
        # Otherwise rock majority is above
        elif self.rock_quadrant_majority[1] < -6:
            if self.velocity[1] >= -1.5:
                self.thrust_direction[1] = 'up'
        else:
            self.thrust_direction[1] = 'None'

    def thrust(self):
        """ Gives a thrust according to the current thrust flags"""

        # Create a new thrust sprite and add it to the group
        for direction in self.thrust_direction:
            if direction != 'None':
                # Create a sprite for a visual depiction of the mass ejection
                ejected = ThrustSprite(self.rect.centerx,self.rect.centery,self.mass,direction)
                self.thrust_group.add(ejected)

                # Update the mass of the enemy
                self.mass *= 1-self.percent_ejection

                # Play a sound if the player is in proximity
                if self.player_in_proximity_flag:
                    self.thrust_sound.play()

                # Update the amount of force from thrust
                if direction == 'left':
                    self.thrust_force_x = -self.mass*self.thrust_mass_multiplyer
                elif direction == 'right':
                    self.thrust_force_x = self.mass*self.thrust_mass_multiplyer
                elif direction == 'up':
                    self.thrust_force_y = -self.mass*self.thrust_mass_multiplyer
                elif direction == 'down':
                    self.thrust_force_y = self.mass*self.thrust_mass_multiplyer

    def update(self, all_sprites, key_down_flag, pygame_events, screen, screen_col, screen_row, win_width, win_height, map_rect, radar_rect):
        """ Move the sprite based on AI logic"""
        self.thrust_force_x = 0
        self.thrust_force_y = 0

        for event in pygame_events:
            # Only give thrust if an event is created for it
            if event.type == self.thrust_count:
                # Sense will use the all_sprites positions and types to change some flags
                # Think will determine what direction to thrust based on the flag positions
                # Thrust will receive a direction from Think and thrust in that direction
                self.sense(all_sprites)
                self.think()
                self.thrust()

        # Calculate force on object
        force = find_force(all_sprites, self.rect[0], self.rect[1], self.mass, self.id)

        # Update acceleration
        acceleration_x = (force[0]+self.thrust_force_x)/(self.mass*framerate*framerate)
        acceleration_y = (force[1]+self.thrust_force_y)/(self.mass*framerate*framerate)

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
