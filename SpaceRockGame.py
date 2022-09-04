# Make a rock
import random
import math

#constants
G = 6.6743e-11 # m3 kg-1 s-2
framerate = 10

class SpaceRock():
    def __init__(self,m,p,v):

        # Mass, Position and Velocity parameters initialized 
        self.mass = m
        self.position = p
        self.velocity = v

    def move(self,space_objects):

        force_x = 0
        force_y = 0

        for obj in space_objects:
            # Check if objects are too close
            if abs(self.position[0] - obj.position[0]) < 1 and abs(self.position[1] - obj.position[1]) < 1:
                continue
            # Calculate force in x direction
                # by finding the distance in the x direction
            r_x = self.position[0] - obj.position[0]
            f_x = (G*self.mass*obj.mass)/((r_x)**2) # N (force)
            # Calculate force in y direction
                # by finding the distance in the x direction
            r_y = self.position[1] - obj.position[1]
            f_y = (G*self.mass*obj.mass)/((r_y)**2) # N (force)
            # Add object force to total force
            force_x += f_x
            force_y += f_y
        # Calculate displacement in X
        dist_x = (((1/framerate)**2)*(force_x/self.mass)*(.5)) + self.velocity[0]*(1/framerate)
        # Calculate displacement in y
        dist_y = (((1/framerate)**2)*(force_y/self.mass)*(.5)) + self.velocity[1]*(1/framerate)
        # Update position
        self.position[0] += dist_x
        self.position[1] += dist_y


class Game_loop():
    def __init__(self, space_objects_input):
        self.rocks = space_objects_input

    def run(self):
        k = 0

        while k < 5: # later replace with While True:
            print("Iteration ", k)
            j = 1
            for i in self.rocks:
                i.move(self.rocks)
                print(f"rock {j} is at ({i.position[0]},{i.position[1]})")
                j += 1
            k+=1



def make_rocks(num):
    # Creating a host of space rocks of random size and posititon
    rocks = []
    for i in range(num):
        rocks.append(SpaceRock(random.random()*10000000000000000, [100-random.random()*200,100-random.random()*200], [10-random.random()*20,10-random.random()*20] ))
    # Printing out the rock's size and position
    # for i in range(num):
    #     print(f"The mass of space rock {i} is {rocks[i].mass}")
    #     print(f"The position of space rock {i} is {rocks[i].position}")

    return rocks




if __name__ == "__main__":
    my_rocks = make_rocks(3)
    game1 = Game_loop(my_rocks)
    game1.run()
