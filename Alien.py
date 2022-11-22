# This file contains the Alien class

import pygame

from config import *
from Calculations import (
                    find_force,
                    radar_coord_conversion
                    )
from pygame.locals import RLEACCEL
from math import floor
from ThrustSprite import ThrustSprite

class Alien(pygame.sprite.Sprite):
    """This is the Alien sprite. Enemies and the Player are classes of Alien"""

    # Must pass in a mass (int), size (int), postion (2 element list), velocity (2 element list)
    def __init__(self, id, mass, size, position, velocity, image, radar_color):
        super(Alien, self).__init__()

        # Mass, Position and Velocity parameters initialized
        self.mass = mass
        self.radius = size/2
        self.velocity = velocity
        self.position = position
        self.id = id

        # Create pygame surface
        self.surface = pygame.image.load(image)
        self.surface = pygame.transform.scale(self.surface, [size,size])
        self.surface.set_colorkey((0,0,0), RLEACCEL)
        self.rect = self.surface.get_rect( center = position )

        # Thrust parameters
        self.thrust_sound = pygame.mixer.Sound(THRUST_SOUND_LOCATION)
        self.thrust_sound.set_volume(.5)
        self.thrust_group = pygame.sprite.Group()
        self.thrust_force = [0,0]

        # Gulp Sound
        self.gulp_sound = pygame.mixer.Sound(GULP_SOUND_LOCATION)
        self.gulp_sound.set_volume(.15)

        # Bounce Sound
        # TBD

        # Create radar point parameters
        self.radar_point_position = [0,0]
        self.radar_point_color = radar_color
        self.radar_point_size = 2
        self.screen_row = 0
        self.screen_col = 0
        self.on_map_flag = True

        # Collision parameters
        self.colliding_enemies = []
        self.colliding_grey = []
        self.collision_force = [0,0]

    def display(self, screen, player_row, player_col, win_width, win_height):
        """ Displays the sprite on the screen"""

        # Adjust the effective player column and row if the player goes off the map
        if player_col < MAP_MIN_COL: player_col = MAP_MIN_COL
        elif player_col > MAP_MAX_COL: player_col = MAP_MAX_COL

        if player_row < MAP_MIN_ROW: player_row = MAP_MIN_ROW
        elif player_row > MAP_MAX_ROW: player_row = MAP_MAX_ROW

        # Determing if the sprite is on the same screen as the player
        if self.screen_row == player_row and self.screen_col == player_col:
            # Blit the sprite to the screen
            screen.blit(self.surface,[
                            self.rect.centerx - (self.screen_col*win_width),
                            self.rect.centery - (self.screen_row*win_height)])

        # Blit the radar point to the screen
        pygame.draw.rect(
                        screen,
                        self.radar_point_color,
                        (self.radar_point_position[0],
                          self.radar_point_position[1],
                          self.radar_point_size,
                          self.radar_point_size))

        # Blit the thrust group with adjusted coordinates
        for sprite in self.thrust_group:
            sprite.display(
                            screen,
                            self.screen_col,
                            self.screen_row,
                            win_width,
                            win_height)

    def update(self,
                all_sprites,
                key_down_flag,
                pressed_keys,
                pygame_events,
                screen,
                player_row,
                player_col,
                win_width,
                win_height,
                map_rect,
                radar_rect):
        """ Move the sprite based on user keypresses """

        self.thrust_force = [0,0]

        self.get_input(all_sprites, key_down_flag, pressed_keys, pygame_events)

        # Calculate force on object
        force = find_force(all_sprites, self.rect[0], self.rect[1], self.mass, self.id)

        # Add in collision force and thrust force
        force[0] += self.collision_force[0] + self.thrust_force[0]
        force[1] += self.collision_force[1] + self.thrust_force[1]

        # Update acceleration
        acceleration_x = (force[0])/(self.mass*framerate*framerate)
        acceleration_y = (force[1])/(self.mass*framerate*framerate)

        # Update velocity
        self.velocity[0] += acceleration_x
        self.velocity[1] += acceleration_y

        # Update the displacement
        self.rect.move_ip(self.velocity[0],self.velocity[1])

        # Update screen row and column
        self.screen_col = floor(self.rect.centerx / win_width)
        self.screen_row = floor(self.rect.centery / win_height)

        # Update the on map flag
        if pygame.Rect.contains(map_rect, self.rect):
            self.on_map_flag = True
        else:
            self.on_map_flag = False

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
                                self.screen_col,
                                self.screen_row,
                                win_width,
                                win_height)

        # Reset collision force
        self.collision_force = [0,0]

        self.display(screen, player_row, player_col, win_width, win_height)
