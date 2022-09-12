# Game involving space rocks
# By Casey Betts
import pygame
from pygame.locals import *
from sys import exit
import random
import math

#constants
G = 6.6743e-11 # m3 kg-1 s-2
framerate = 10
winHeight = 400
winWidth = 800
number_of_rocks = 3

pygame.init()


# Create a class for the space rocks extending pygame sprite class
class SpaceRock(pygame.sprite.Sprite):
    def __init__(self,m,p,v):
        super(SpaceRock,self).__init__()

        # Mass, Position and Velocity parameters initialized
        self.mass = m
        self.position = p
        self.velocity = v

        if pygame.get_init():
            self.surface = pygame.Surface((10,10))
            self.surface.fill("Red")
            self.rect = self.surface.get_rect()
        else:
            print("pygame is not initialized")

    def update(self):
        # Find the displacement in position
        dist = displacement(rocks, self)
        # Update position
        self.rect.move_ip(dist[0],dist[1])

# This will take in a group of rocks and determin the displacement of a given rock
def displacement(group,target):

    total_force_x = 0
    total_force_y = 0
    # For each rock in the sprite group calculate the force on the target rock
    for rock in group:
        if (target.position[0] - rock.position[0]) < 1 and (target.position[1] - rock.position[1]) < 1:
            continue
        # Calculate force in x direction by finding the distance in the x direction
        distance_x = target.position[0] - rock.position[0]
        force_x = (G*target.mass*rock.mass)/((distance_x)**2) # N (force)
        # Calculate force in x direction by finding the distance in the y direction
        distance_y = target.position[1] - rock.position[1]
        force_y = (G*target.mass*rock.mass)/((distance_y)**2) # N (force)
        # Add object force to total force
        total_force_x += force_x
        total_force_y += force_y
    # Calculate the displacement of the tartet rock
    # Calculate displacement in X
    displacement_x = (((1/framerate)**2)*(total_force_x/target.mass)*(.5)) + target.velocity[0]*(1/framerate)
    # Calculate displacement in y
    displacement_y = (((1/framerate)**2)*(total_force_y/target.mass)*(.5)) + target.velocity[1]*(1/framerate)

    # Return displacement in a tuple
    return (displacement_x, displacement_y)

# Create a sprite group to contain the space rocks
rocks = pygame.sprite.Group()

class Game():
    # Contains the loop for running the game
    def __init__(self):
        # Create a display window
        self.screen = pygame.display.set_mode((winWidth,winHeight))
        # Create a clock to control frames per second
        self.clock = pygame.time.Clock()

    def run(self):
        # Contains the loop to render the game and exit on quit event
        print("is pygame init? ", pygame.get_init())


        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.cleanup()
                elif event.type == pygame.QUIT:
                    self.cleanup()
            # White background
            self.screen.fill('White')

            # Update rock positions
            rocks.update()

            # Draw all sprites
            for entity in rocks:
                self.screen.blit(entity.surface, entity.rect)

            # for i in range(number_of_rocks):
            #     print(f"rock {i}")
            #     self.rocks[i].move(self.rocks)
            #     print(int(self.rocks[i].position[0]), "and",int(self.rocks[i].position[1]) )
                #self.screen.blit(self.rocks[i].surface,(int(self.rocks[i].position[0]),int(self.rocks[i].position[1])))

            self.clock.tick(10)

            pygame.display.flip()

    def cleanup(self):
        pygame.quit()
        exit()
        print("cleanup complete")

# returns a list of space rock objects
def make_rocks(num):
    # Creating a host of space rocks of random size and posititon
    rocks = []
    for i in range(num):
        rocks.append(
            SpaceRock(
                random.randint(1,10)*10000000000000000,
                [random.randint(1,10)*winWidth,random.randint(1,10)*winHeight],
                [10-random.randint(1,10)*20,10-random.randint(1,10)*20]
                )
            )
    # Printing out the rock's size and position
    # for i in range(num):
    #     print(f"The mass of space rock {i} is {rocks[i].mass}")
    #     print(f"The position of space rock {i} is {rocks[i].position}")

    return rocks

if __name__ == "__main__":
    # Create the rocks and add them to a sprite group
    rock_list = make_rocks(number_of_rocks)
    for rock in rock_list:
        rocks.add(rock)
    # Create game object and run
    game1 = Game()
    game1.run()
