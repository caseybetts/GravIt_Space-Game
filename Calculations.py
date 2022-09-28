# This file holds all the calculation functions for the game
from math import sqrt, sin, cos, atan, fabs
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
        # remove target sprite from the list; save to variable
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


def pickle_ball(target,winHeight):

    # Update velocity
    target.velocity[1] -= little_g

    if target.rect.bottom >= winHeight:
        target.velocity[1] = -1*(target.velocity[1]+1)

    # Update position
    target.rect.move_ip(target.velocity[0], target.velocity[1])


def radar_coord_conversion(map_x, map_y, reduction_factor, radar_left, radar_top, map_left, map_top):
    # Function will convert the actual x and y coordinates for coordinates on the rador screen
    radar_x = map_x - map_left
    radar_x *= reduction_factor
    radar_x += radar_left

    radar_y = map_y - map_top
    radar_y *= reduction_factor
    radar_y += radar_top

    return [radar_x, radar_y]

def display_coord_conversion(map_x, map_y, scrn_col, scrn_row):
    # This converts the coordinate from the map to what should be displayed based on what area of the map is being shown

    # Calculate the display x coord based on the screen col
    disp_x = map_x + (winWidth * scrn_col)

    # Calculate the display y coord based on the screen row
    disp_y = map_y + (winWidth * scrn_row)

    return [disp_x,disp_y]

def momentum(m1,v1,m2,v2):
    # returns the final velocity of two objects colliding with eachother
    final_velocity = (m1*v1 + m2*v2)/(m1+m2)
    return final_velocity
