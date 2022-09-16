# Game involving space rocks
# By Casey Betts

# mustard sun by Martin Cee (softmartin) (c) copyright 2022 Licensed under a Creative Commons Attribution Noncommercial  (3.0) license. http://dig.ccmixter.org/files/softmartin/65383 Ft: subliminal

import pygame
from pygame.locals import *
from sys import exit
import random
import math
from Calculations import find_force

# Import pygame.locals for easier access to key coordinates
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

#constants
number_of_rocks = 60
framerate = 30
winHeight = 1000
winWidth = 1600
player_start_mass = 1000
player_start_velocity = [0,0]
player_start_size = [20,20]
helper_force = 5000
thrust_acc = 100000
percent_ejection = .001
rebound_velocity = 2
collision_slow_percent = .99
MASSES = (100000, 500000, 2000000)

pygame.init()


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


    def update(self):
        # Calculate force on object
        force = find_force(all_sprites, self.rect[0], self.rect[1], self.mass, self.id)
        # print(self.id, "Force ", force)
        # Give the rocks a little force to keep them from clustering at the edges
        if self.rect[0] < 0:
            force[0]+= helper_force
        elif self.rect[0] > winWidth:
            force[0]-= helper_force

        if self.rect[1] < 0:
            force[1]+= helper_force
        elif self.rect[1] > winHeight:
            force[1]-= helper_force

        # Update acceleration
        acceleration_x = force[0]/(self.mass*framerate*framerate)
        acceleration_y = force[1]/(self.mass*framerate*framerate)
        # print(self.id, "Acceleration :", acceleration_x, ", ", acceleration_y)
        # Update object's velocity
        self.velocity[0] += acceleration_x
        self.velocity[1] += acceleration_y
        # Find the displacement in position
        self.rect.move_ip(self.velocity[0],self.velocity[1])

        # Keep sprite within the boudary
        if self.rect.left < boundary.left:
            self.velocity[0] = rebound_velocity
        if self.rect.right > boundary.right:
            self.velocity[0] = -rebound_velocity
        if self.rect.top <= boundary.top:
            self.velocity[1] = rebound_velocity
        if self.rect.bottom >= boundary.bottom:
            self.velocity[1] = -rebound_velocity

class Player(pygame.sprite.Sprite):
    """This is the player sprite"""
    def __init__(self):
        super(Player,self).__init__()

        # Mass, Position and Velocity parameters initialized
        self.mass = player_start_mass
        self.velocity = player_start_velocity
        self.size = player_start_size
        self.id = 0
        # Create pygame Surface
        self.surface = pygame.image.load("Graphics/GreenBlob.png")
        self.surface = pygame.transform.scale(self.surface, self.size)
        self.surface.set_colorkey((0,0,0), RLEACCEL)
        self.rect = self.surface.get_rect( center = (winWidth/2,winHeight/2) )

    # Move the sprite based on user keypresses
    def update(self, pressed_keys):
        x_thrust = 0
        y_thrust = 0
        if pressed_keys[K_UP]:
            y_thrust = -(self.mass*percent_ejection)*thrust_acc      # ejection mass x acceleration
            self.mass *= .99
        if pressed_keys[K_DOWN]:
            y_thrust = (self.mass*percent_ejection)*thrust_acc       # ejection mass x acceleration
            self.mass *= .99
        if pressed_keys[K_LEFT]:
            x_thrust = -(self.mass*percent_ejection)*thrust_acc       # ejection mass x acceleration
            self.mass *= .99
        if pressed_keys[K_RIGHT]:
            x_thrust = (self.mass*percent_ejection)*thrust_acc       # ejection mass x acceleration
            self.mass *= .99

        # Calculate force on object
        force = find_force(all_sprites, self.rect[0], self.rect[1], self.mass, self.id)
        # print(self.id, "Force ", force)
        # Update acceleration
        acceleration_x = (force[0]+x_thrust)/(self.mass*framerate*framerate)
        acceleration_y = (force[1]+y_thrust)/(self.mass*framerate*framerate)
        # print(self.id, "Acceleration :", acceleration_x, ", ", acceleration_y)
        # Update object's velocity
        self.velocity[0] += acceleration_x
        self.velocity[1] += acceleration_y
        # Find the displacement in position
        self.rect.move_ip(self.velocity[0],self.velocity[1])

        # Keep player on the screen
        if self.rect.left < 0:
            self.velocity[0] = 1
        if self.rect.right > winWidth:
            self.velocity[0] = -1
        if self.rect.top <= 0:
            self.velocity[1] = 1
        if self.rect.bottom >= winHeight:
            self.velocity[1] = -1

class OuterBoudary():
    def __init__(self,left,right,top,bottom):
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom

class _Setup():
    "Provides functions needed to set up the game"

    def make_random_rock(self, ID):
        # returns a space rock of random mass and position
        mass = random.choice(MASSES) #random.randint(5,10)*1000000000000000
        x_position = random.randint(boundary.left,boundary.right)
        y_position = random.randint(boundary.top, boundary.bottom) #[10-random.randint(1,2),10-random.randint(1,2)]
        x_velocity = random.randint(-5,5)
        y_velocity = random.randint(-5,5)
        rand_rock = SpaceRock( mass, x_position, y_position, x_velocity, y_velocity, ID )
        return rand_rock

    def make_random_rocks(self, num):
        # Create a sprite group to contain random space rocks
        sprite_group = pygame.sprite.Group()
        for i in range(num):
            sprite_group.add(self.make_random_rock(i+1))
        return sprite_group

class Game():
    # Contains the loop for running the game
    def __init__(self):
        # Create a display window
        self.screen = pygame.display.set_mode((winWidth,winHeight))
        # Create a clock to control frames per second
        self.clock = pygame.time.Clock()
        # Font
        self.font = pygame.font.Font(pygame.font.get_default_font(), 40)
        # Create variable to store the number of rocks remaining
        self.remaining_rocks = len(rocks.sprites())

    def run(self):
        # Contains the loop to render the game and exit on quit event

        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.cleanup()
                elif event.type == pygame.QUIT:
                    self.cleanup()

            # White background
            self.screen.fill('Black')

            # Get the set of keys pressed and check for user input
            pressed_keys = pygame.key.get_pressed()

            # Check if any space rocks have collided with eachother
            for rock in rocks:
                rock_collision = pygame.sprite.spritecollideany(rock, rocks)
                if rock_collision.id != rock.id:
                    if abs(rock_collision.velocity[0] - rock.velocity[0]) < 1 and abs(rock_collision.velocity[1] - rock.velocity[1]) < 1:
                        if rock_collision.mass > rock.mass:
                            rock_collision.mass += rock.mass
                            rock.kill()
                        else:
                            rock.mass += rock_collision.mass
                            rock_collision.kill()
                        self.remaining_rocks = len(rocks.sprites())
                    else:
                        rock_collision.velocity[0] *= collision_slow_percent
                        rock_collision.velocity[1] *= collision_slow_percent
                        rock.velocity[0] *= collision_slow_percent
                        rock.velocity[1] *= collision_slow_percent
                        print(rock_collision.id)

            # Check if any space rocks have collided with the player
            collision = pygame.sprite.spritecollide(blob,rocks, True)

            if collision:
                # If so, then kill the space rock and add the rock's mass to the player mass
                print( collision[0].mass )
                blob.mass += collision[0].mass
                self.remaining_rocks = len(rocks.sprites())

            # Update player position
            blob.update(pressed_keys)
            self.screen.blit(blob.surface, blob.rect)
            # Update space rock positions
            rocks.update()
            for entity in rocks:
                self.screen.blit(entity.surface, entity.rect)

            # End the game when all space rocks are gone
            if not rocks.sprites(): self.cleanup()

            # Display the current mass of the player
            mass_text_surf = self.font.render(
                f'Current Mass: {math.trunc(blob.mass)} kg              Space Rocks Remaining: {self.remaining_rocks}',
                False, (64,64,64))
            self.screen.blit(mass_text_surf,(10,10))

            self.clock.tick(framerate)

            pygame.display.flip()

    def cleanup(self):
        pygame.quit()
        exit()
        print("cleanup complete")

if __name__ == "__main__":
    # Create rock boundary
    boundary = OuterBoudary(-winWidth,2*winWidth,-winHeight,2*winHeight)
    # boundary = OuterBoudary(0,winWidth,0,winHeight)
    # Create the rocks and add them to a sprite group
    setup = _Setup()
    rocks = setup.make_random_rocks(number_of_rocks)
    # Create the player sprite
    blob = Player()
    # Sprite group for all sprites
    all_sprites = pygame.sprite.Group()
    for rock in rocks:
        all_sprites.add(rock)
    all_sprites.add(blob)
    # Sprite group just for the player
    player_group = pygame.sprite.Group()
    player_group.add(blob)

    # Create game object and run
    game1 = Game()
    game1.run()
