# Game involving space rocks
# By Casey Betts
import pygame
from pygame.locals import *
from sys import exit
import random
import math
from Calculations import displacement, motion_tester, pickle_ball, find_force

#constants
framerate = 30
winHeight = 800
winWidth = 1200
number_of_rocks = 100
MASSES = (100000, 500000, 2000000)

pygame.init()


# Create a class for the space rocks extending pygame sprite class
class SpaceRock(pygame.sprite.Sprite):
    def __init__(self,mass,position,velocity,id):
        super(SpaceRock,self).__init__()

        # Mass, Position and Velocity parameters initialized
        self.mass = mass
        self.velocity = velocity
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
        self.rect = self.surface.get_rect( center = (position[0],position[1]) )


    def update(self):
        # Calculate force on object
        force = find_force(rocks, self.id)
        # print(self.id, "Force ", force)
        # Update acceleration
        acceleration_x = force[0]/(self.mass*framerate*framerate)
        acceleration_y = force[1]/(self.mass*framerate*framerate)
        # print(self.id, "Acceleration :", acceleration_x, ", ", acceleration_y)
        # Update object's velocity
        self.velocity[0] += acceleration_x
        self.velocity[1] += acceleration_y
        # Find the displacement in position
        self.rect.move_ip(self.velocity[0],self.velocity[1])
        # print(self.id, " Position: ", self.rect[0]," , ",self.rect[1] )

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

            self.clock.tick(framerate)

            pygame.display.flip()

    def cleanup(self):
        pygame.quit()
        exit()
        print("cleanup complete")

def make_random_rock(ID):
    # returns a space rock of random mass and position
    mass = random.choice(MASSES) #random.randint(5,10)*1000000000000000
    x_position = winWidth/2 + random.randint(-winWidth/4,winWidth/4)
    y_position = winHeight/2 + random.randint(-winHeight/4,winHeight/4) #[10-random.randint(1,2),10-random.randint(1,2)]
    x_velocity = random.randint(-5,5)
    y_velocity = random.randint(-5,5)
    rand_rock = SpaceRock( mass, [x_position, y_position], [x_velocity,y_velocity], ID )
    return rand_rock

def make_random_rocks(num):
    # Create a sprite group to contain random space rocks
    sprite_group = pygame.sprite.Group()
    for i in range(num):
        sprite_group.add(make_random_rock(i))
    return sprite_group

if __name__ == "__main__":
    # Create the rocks and add them to a sprite group
    rocks = make_random_rocks(number_of_rocks)
    # Create game object and run
    game1 = Game()
    game1.run()
