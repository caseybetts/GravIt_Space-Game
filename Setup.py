# This file contains the Game_Setup class

import pygame
import random

from config import *
from Enemy import *
from SpaceRock import *
from RadarPoint import *

class Game_Setup():
    """Provides functions needed to set up the game"""

    def print_sprite(self, sprite):
        """Prints the attributes of the sprite"""
        print("id=", sprite.id,
                "\nmass=", sprite.mass)

    def enemy_generator(self, enemy_specs):
        """ Produces a group of enemies of the given specs. The enemy_specs argument
        should be a list of lists like [[quantity, mass, size], ...]"""

        sprite_group = pygame.sprite.Group()

        i = 1001

        for group in enemy_specs:
            print(group)
            for j in range(group[0]):
                sprite_group.add(self.make_enemy(i, group[1], group[2]))
                i += 1

        print(sprite_group)
        return sprite_group

    def make_enemy(self, id, mass, size, position = None, velocity = None):
        """ Returns an enemy sprite """

        if position == None:
            position = [int(random.gauss(500,1000)),
                        int(random.gauss(500,1000))]

        if velocity == None:
            velocity = [random.randint(-1,1),
                        random.randint(-1,1)]

        return Enemy(id, mass, size, position, velocity)

    def rock_generator(self, rock_specs, color):
        """Produces a group of rocks of the specified sizes. The rock_specs argument
        should be a list of lists like [ [quantity, rock size],...]"""

        if color == "Brown":
            i = 1
        elif color == "Grey":
            i = 200

        # Create a sprite group to contain the rocks
        sprite_group = pygame.sprite.Group()

        for size_group in rock_specs:
            for j in range(size_group[0]):
                sprite_group.add(self.make_rock(i,size_group[1], color))
                i+=1

        return sprite_group

    def make_rock(self, id, mass, color, position = None, velocity = None):
        "Returns one SpaceRock object"

        if position == None:
            position = [int(random.gauss(ROCK_LOWER_GAUSS_X, ROCK_UPPER_GAUSS_X)),
                        int(random.gauss(ROCK_LOWER_GAUSS_Y, ROCK_UPPER_GAUSS_Y))]

        if velocity == None:
            velocity = [random.randint(ROCK_START_VELOCITY[0],ROCK_START_VELOCITY[1]),
                        random.randint(ROCK_START_VELOCITY[0],ROCK_START_VELOCITY[1])]

        return SpaceRock( id, mass, color, position[0], position[1], velocity[0], velocity[1])

    def make_random_rock(self, id, x_bound, y_bound, mass = None):
        # returns a space rock of random mass and position

        # If a mass is not given then choose a random mass from the list
        if mass == None:
            mass = random.choice(MASSES)

        x_position = random.randint(x_bound[0], x_bound[1])
        y_position = random.randint(y_bound[0], y_bound[1])
        x_velocity = random.randint(ROCK_START_VELOCITY[0],ROCK_START_VELOCITY[1])
        y_velocity = random.randint(ROCK_START_VELOCITY[0],ROCK_START_VELOCITY[1])
        rand_rock = SpaceRock( id, mass, x_position, y_position, x_velocity, y_velocity)
        return rand_rock

    def make_random_rocks(self, num, x_bound, y_bound):
        # Create a sprite group to contain random space rocks
        sprite_group = pygame.sprite.Group()
        for i in range(num):
            sprite_group.add(self.make_random_rock(i+1, x_bound, y_bound))
        return sprite_group

    def make_radar_points(self, num):
        sprite_group = pygame.sprite.Group()
        for i in range(num):
            point = RadarPoint(i+1)
            sprite_group.add(point)
        return sprite_group


if __name__ == "__main__":

    setup = Game_Setup()
    my_sprites = setup.rock_generator([[500,3], [200,10], [100, 20]], "Grey")

    for sprite in my_sprites:
        setup.print_sprite(sprite)
