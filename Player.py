# This file contains the Player class

import pygame
from Calculations import find_force
from config import *
# Import pygame.locals for easier access to key coordinates
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    K_c,
    KEYDOWN,
    QUIT,
    )
from ThrustSprite import ThrustSprite

class Player(pygame.sprite.Sprite):
    """This is the player sprite"""
    def __init__(self, mass, x_size, y_size):
        super(Player,self).__init__()

        # Mass, Position and Velocity parameters initialized
        self.mass = mass
        self.velocity = [0,0]
        self.size = [x_size, y_size]
        self.id = 0
        # Create pygame Surface
        self.surface = pygame.image.load("Graphics/GreenBlob.png")
        self.surface = pygame.transform.scale(self.surface, self.size)
        self.surface.set_colorkey((0,0,0), RLEACCEL)
        self.rect = self.surface.get_rect( center = (0,0) )

        # Thrust sound and group
        self.thrust_sound = pygame.mixer.Sound(thrust_sound_location)
        self.thrust_sound.set_volume(.75)
        self.thrust_group = pygame.sprite.Group()
        self.percent_ejection = .001

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

    # Move the sprite based on user keypresses
    def update(self, all_sprites, key_down_flag, pressed_keys):

        x_thrust = 0
        y_thrust = 0

        # Check if any key is pressed
        if key_down_flag:
            # Check which key is pressed and update thrust and mass
            if pressed_keys[K_UP]:
                y_thrust = -self.thrust('up')

            if pressed_keys[K_DOWN]:
                y_thrust = self.thrust('down')

            if pressed_keys[K_LEFT]:
                x_thrust = -self.thrust('left')

            if pressed_keys[K_RIGHT]:
                x_thrust = self.thrust('right')

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
