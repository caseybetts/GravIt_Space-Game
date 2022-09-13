# Game involving space rocks
# By Casey Betts
import pygame
from pygame.locals import *
from sys import exit
import random
import math
from Calculations import displacement, motion_tester, pickle_ball

#constants
framerate = 10
winHeight = 400
winWidth = 800
number_of_rocks = 3

pygame.init()


# Create a class for the space rocks extending pygame sprite class
class SpaceRock(pygame.sprite.Sprite):
    def __init__(self,mass,position,velocity):
        super(SpaceRock,self).__init__()

        # Mass, Position and Velocity parameters initialized
        self.mass = mass
        self.velocity = velocity

        if pygame.get_init():
            self.surface = pygame.Surface((10,10))
            self.surface.fill("Red")
            self.rect = self.surface.get_rect( center = (position[0],position[1]) )
        else:
            print("pygame is not initialized")

    def update(self):
        # Find the displacement in position
        #dist = displacement(rocks, self, framerate)
        ##### Testing
        #dist = motion_tester(1)
        # Update position
        #self.rect.move_ip(dist[0]+self.velocity[0],dist[1]+self.velocity[1])
        pickle_ball(self,winHeight)

class Game():
    # Contains the loop for running the game
    def __init__(self):
        # Create a display window
        self.screen = pygame.display.set_mode((winWidth,winHeight))
        # Create a clock to control frames per second
        self.clock = pygame.time.Clock()

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
            self.screen.fill('White')

            # Update rock positions
            rocks.update()

            # Draw all sprites
            for entity in rocks:
                self.screen.blit(entity.surface, entity.rect)

            self.clock.tick(15)

            pygame.display.flip()

    def cleanup(self):
        pygame.quit()
        exit()
        print("cleanup complete")

def make_random_rock():
    # returns a space rock of random mass and position
    rand_rock = SpaceRock(
                    100000000000000000,
                    #random.randint(1,100)*1000000000000000,
                    [winWidth/2 + random.randint(-winWidth/2,winWidth/2),winHeight/2 + random.randint(-winHeight/2,winHeight/2)],
                    [0,0]
                    #[10-random.randint(1,2),10-random.randint(1,2)]
                    )
    return rand_rock

def make_random_rocks(num):
    # Create a sprite group to contain random space rocks
    sprite_group = pygame.sprite.Group()
    for i in range(num):
        sprite_group.add(make_random_rock())
    return sprite_group

if __name__ == "__main__":
    # Create the rocks and add them to a sprite group
    rocks = make_random_rocks(2)

    ############ testing
    for rock in rocks:
        pass
        #print(f"Mass: {rock.mass}\nPosition: {rock.position}\nVelocity: {rock.velocity}")
        #print(rock.rect)
    ##############

    # Create game object and run
    game1 = Game()
    game1.run()
