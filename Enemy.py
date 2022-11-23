# This file contains the Enemy class

import pygame
import random

from Alien import *
from Calculations import (
                    find_force,
                    radar_coord_conversion
                    )
from config import *
from math import fabs, floor
from pygame.locals import RLEACCEL
from ThrustSprite import ThrustSprite

class Enemy(Alien):
    """This is the enemy sprite"""

    # Must pass in a mass (int), size (int), postion (2 element list), velocity (2 element list)
    def __init__(self, id, mass, size, position, velocity):
        super(Enemy,self).__init__(id, mass, size, position, velocity, ENEMY_IMAGE_LOCATION, "Yellow")

        self.percent_ejection = ENEMY_PERCENT_EJECTION ##
        self.thrust_direction = ['left', 'up'] ##
        self.thrust_mass_multiplyer = self.percent_ejection*thrust_acc ##

        # Only allow the enemy to thrust at a certain frequency
        self.thrust_count = pygame.USEREVENT + 2
        pygame.time.set_timer(self.thrust_count, 1000)

        # Sensor parameters
        self.player_in_proximity_flag = False
        self.enemy_in_proximity_flag = False
        self.rock_quadrant_majority = [0, 0]

        # Collision parameters
        self.colliding_enemies = []
        self.colliding_grey = []
        self.collision_force = [0,0]

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
                ejected = ThrustSprite(self.rect.centerx, self.rect.centery, self.mass, direction, "Yellow")
                self.thrust_group.add(ejected)

                # Update the mass of the enemy
                self.mass *= 1-self.percent_ejection

                # Play a sound if the player is in proximity
                if self.player_in_proximity_flag:
                    self.thrust_sound.play()

                # Update the amount of force from thrust
                if direction == 'left':
                    self.thrust_force[0] = -self.mass*self.thrust_mass_multiplyer
                elif direction == 'right':
                    self.thrust_force[0] = self.mass*self.thrust_mass_multiplyer
                elif direction == 'up':
                    self.thrust_force[1] = -self.mass*self.thrust_mass_multiplyer
                elif direction == 'down':
                    self.thrust_force[1] = self.mass*self.thrust_mass_multiplyer

    def get_input(self, all_sprites, key_down_flag, pressed_keys, pygame_events):
        """Retrieves input from the system"""

        for event in pygame_events:
            # Only give thrust if an event is created for it
            if event.type == self.thrust_count:
                # Sense will use the all_sprites positions and types to change some flags
                # Think will determine what direction to thrust based on the flag positions
                # Thrust will receive a direction from Think and thrust in that direction
                self.sense(all_sprites)
                self.think()
                self.thrust()
