# This file contains the Player class

# rect attributes:
# x,y
# top, left, bottom, right
# topleft, bottomleft, topright, bottomright
# midtop, midleft, midbottom, midright
# center, centerx, centery
# size, width, height
# w,h

import pygame
from Alien import *
from math import floor
from Calculations import (
                    find_force,
                    radar_coord_conversion
                    )
from config import *
# Import pygame.locals for easier access to key coordinates
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    K_RETURN,
    K_SPACE,
    K_c,
    KEYDOWN,
    QUIT,
    )
from ThrustSprite import ThrustSprite

class Player(Alien):
    """This is the player sprite"""
    def __init__(self, mass, size):
        super(Player,self).__init__(0, mass, size, [0,0], [0,0], PLAYER_IMAGE_LOCATOIN, "GREEN")

        self.percent_ejection = .003

    def thrust(self, direction):

        # Create a new thrust sprite and add it to the group
        ejected = ThrustSprite(self.rect.centerx, self.rect.centery, self.mass, direction, "Green")
        self.thrust_group.add(ejected)

        # Update the mass
        self.mass *= 1-self.percent_ejection

        # Play a sound
        self.thrust_sound.play()

        # Calculate and return the amount of force
        return self.mass*self.percent_ejection*thrust_acc

    def get_input(self, all_sprites, key_down_flag, pressed_keys, pygame_events):
        """Retrieves input from the player"""

        # Check if any key is pressed
        if key_down_flag:
            # Check which key is pressed and update thrust and mass
            if pressed_keys[K_UP]:
                self.thrust_force[1] = -self.thrust('up')

            if pressed_keys[K_DOWN]:
                self.thrust_force[1] = self.thrust('down')

            if pressed_keys[K_LEFT]:
                self.thrust_force[0] = -self.thrust('left')

            if pressed_keys[K_RIGHT]:
                self.thrust_force[0] = self.thrust('right')


if __name__ == "__main__":

    myPlayer = Player()

    print(myPlayer)
