# This file holds all the calculation functions for the game
from math import sqrt, sin, cos, atan, fabs, tan
from config import grav_threshold

#Constants
G = 6.6743e-11 # m3 kg-1 s-2
little_g = -9.8 # m/s^2

# Define a function for calculating change in velocity
def find_force(sprite_group, xcoord, ycoord, mass, ID):
    sprites = sprite_group.sprites()
    num = len(sprites)
    total_force_x = 0
    total_force_y = 0

    for i in range(num):
        # remove target sprite from the list
        if sprites[i].id == ID:
            sprites.pop(i)
            break

    for sprite in sprites:
        # Calcualate delta x and y
        distance_x = sprite.rect[0] - xcoord
        distance_y = sprite.rect[1] - ycoord
        # Calculate distance
        total_distance = sqrt((distance_x**2) + (distance_y**2) )

        if distance_x > 1 or distance_x < -1:
            angle = atan(distance_y/distance_x)
        else:
            angle = 0
        # Calculate total force
        if total_distance > grav_threshold:
            total_force = (G*mass*sprite.mass)/(total_distance**2) # N (force)
        else:
            total_force = (G*mass*sprite.mass)/(grav_threshold**2) # N (force)

        # Calculate force in x direction
        if distance_x < 0:
            force_x = -total_force*fabs(cos(angle))
        else:
            force_x = total_force*fabs(cos(angle))

        # Calculate force in y direction
        if distance_y < 0:
            force_y = -total_force*fabs(sin(angle))
        else:
            force_y = total_force*fabs(sin(angle))

        # Add object force to total force
        total_force_x += force_x
        total_force_y += force_y

    return [total_force_x, total_force_y]

# Given a motion type returns a tuple of displacement
def motion_tester(type):

    # No motion
    if type == 1:
        return (0,0)
    # Constant velocity to the right
    elif type == 2:
        return (5,0)
    # Constant velocity down
    elif type == 3:
        return (0,5)
    else:
        print("Invalid motion type. Use 1, 2 or 3.")

def pickle_ball(target,window_Height):

    # Update velocity
    target.velocity[1] -= little_g

    if target.rect.bottom >= window_Height:
        target.velocity[1] = -1*(target.velocity[1]+1)

    # Update position
    target.rect.move_ip(target.velocity[0], target.velocity[1])


def radar_coord_conversion(map_x, map_y, reduction_factor, radar_rect, map_rect):
    # Function will convert the actual x and y coordinates for coordinates on the rador screen
    radar_x = map_x - map_rect.left
    radar_x *= reduction_factor
    radar_x += radar_rect.left

    radar_y = map_y - map_rect.top
    radar_y *= reduction_factor
    radar_y += radar_rect.top

    return [radar_x, radar_y]


def momentum(m1,v1,m2,v2):
    # returns the final velocity of two objects colliding with eachother
    final_velocity = (m1*v1 + m2*v2)/(m1+m2)
    return final_velocity

def calculate_collision_force(sprite_1, sprite_2):
    """ Returns the force on each sprite as a result of their collision """

    # Define hardness factor
    k = 100

    # Calculate the distance between the center of the sprites
    dist_from_centers_x = sprite_1.rect.centerx - sprite_2.rect.centerx
    dist_from_centers_y = sprite_1.rect.centery - sprite_2.rect.centery

    # Can't allow distance be zero or div/0 error occurs
    if dist_from_centers_x == 0: dist_from_centers_x = .001
    if dist_from_centers_y == 0: dist_from_centers_y = .001

    norm = sqrt((dist_from_centers_x**2) + (dist_from_centers_y**2))

    separation = norm - (sprite_1.radius + sprite_2.radius)

    # If the distance is less than the combined radiuses, continue
    if separation < 0:

        # Calculate force on sprite 1
        total_force_on_1 = fabs(k * sprite_2.mass * (separation**5))

        # Put a check on how high the force can be
        if total_force_on_1 > 80000*sprite_1.mass:
            total_force_on_1 = 80000*sprite_1.mass

        # Calculate the angle of the force
        angle = atan(fabs(dist_from_centers_y)/fabs(dist_from_centers_x))

        # Break the total force into x and y components
        force_on_1_x = total_force_on_1*cos(angle)*(1/dist_from_centers_x)
        force_on_1_y = total_force_on_1*sin(angle)*(1/dist_from_centers_y)

        # Check if the sprites are moving away from eachother
        velocity_delta_x = sprite_1.velocity[0] - sprite_2.velocity[0]
        velocity_delta_y = sprite_1.velocity[1] - sprite_2.velocity[1]

        # Sprite_2 is to the right of sprite_1 and they are moving away from eachother
        if dist_from_centers_x < 0 and velocity_delta_x < 0:
            force_on_1_x *= .7
        if dist_from_centers_x > 0 and velocity_delta_x > 0:
            force_on_1_x *= .7

        if dist_from_centers_y < 0 and velocity_delta_y < 0:
            force_on_1_y *= .7
        if dist_from_centers_y > 0 and velocity_delta_y > 0:
            force_on_1_y *= .7

        return [ [force_on_1_x, force_on_1_y], [-force_on_1_x, -force_on_1_y] ]

    return [[0,0],[0,0]]

def exponent_split(num):
    """Convert exponential notation to value and exponent"""
    count = 0
    if num <= 0:
        return [0,0]
    elif num > 1:
        while num > 10:
            num/=10
            count+=1
    else:
        while num < 1:
            num*=10
            count-=1
    return [num, count]

def calculate_collision_force_test(dict_1, dict_2):
    """ Returns the force on each sprite as a result of their collision """
    print("dict_1:", dict_1)
    print("dict_2:", dict_2)

    # Define hardness
    k = 10

    # Calculate the distance between the center of the sprites
    dist_from_centers_x = dict_1["centerx"] - dict_2["centerx"]
    dist_from_centers_y = dict_1["centery"] - dict_2["centery"]
    print("dist from centers x:", dist_from_centers_x)
    print("dist from centers y:", dist_from_centers_y)

    norm = sqrt((dist_from_centers_x**2) + (dist_from_centers_y**2))
    print("norm:", norm)

    separation = norm - (dict_1["radius"]+dict_2["radius"])
    print("separation:", separation)

    # If the distance is less than the combined radiuses, continue
    if separation < 0:

        # Calculate force on sprite 1
        total_force_on_1 = fabs(k*separation)
        print("total_force_on_1:", total_force_on_1)

        # Calculate the angle of the force
        angle = atan(fabs(dist_from_centers_y)/fabs(dist_from_centers_x))
        print("angle: atan(",dist_from_centers_y,"/", dist_from_centers_x,") = ", angle)

        # Break the total force into x and y components
        force_on_1_x = total_force_on_1*cos(angle)*(1/dist_from_centers_x)
        force_on_1_y = total_force_on_1*sin(angle)*(1/dist_from_centers_y)
        print("force on 1 x: ", force_on_1_x)
        print("force on 1 y: ", force_on_1_y)

        return [ [force_on_1_x, force_on_1_y], [-force_on_1_x, -force_on_1_y] ]

    return [[0,0],[0,0]]

if __name__ == '__main__':

    dict_1 = {"centerx":0, "centery":0, "radius":2}
    dict_2 = {"centerx":1, "centery":-3, "radius":2}

    print(calculate_collision_force_test(dict_1, dict_2))
