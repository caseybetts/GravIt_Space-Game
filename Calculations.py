# This file holds all the calculation functions for the game
from math import sqrt, sin, cos, atan, fabs

#Constants
G = 6.6743e-1 # m3 kg-1 s-2
little_g = -9.8 # m/s^2


# This will take in a group of rocks and determin the displacement of a given rock
def displacement(group,target,framerate):

    total_force_x = 0
    total_force_y = 0
    # For each rock in the sprite group calculate the force on the target rock
    for rock in group:

        # Find the distance in each direction
        distance_x = target.rect[0] - rock.rect[0]
        distance_y = target.rect[1] - rock.rect[1]

        # Calculate force in x direction
        if distance_x < -2:
            force_x = (-1)*(G*target.mass*rock.mass)/((distance_x)**2) # N (force)
        elif distance_x > 2:
            force_x = (G*target.mass*rock.mass)/((distance_x)**2) # N (force)
        else:
            force_x = 0

        # Calculate force in y direction
        if distance_y < -2:
            force_y = (-1)*(G*target.mass*rock.mass)/((distance_y)**2) # N (force)
        elif distance_y > 2:
            force_y = (G*target.mass*rock.mass)/((distance_y)**2) # N (force)
        else:
            force_y = 0

        # Add object force to total force
        total_force_x += force_x
        total_force_y += force_y
    # Calculate the displacement of the tartet rock in each direction
    displacement_x = (((1/framerate)**2)*(total_force_x/target.mass)*(.5)) + target.velocity[0]*(1/framerate)
    displacement_y = (((1/framerate)**2)*(total_force_y/target.mass)*(.5)) + target.velocity[1]*(1/framerate)

    # Return displacement in a tuple
    return (displacement_x, displacement_y)

# Define a function for calculating change in velocity
def find_force(sprite_group, ID):
    sprites = sprite_group.sprites()
    num = len(sprites)
    total_force_x = 0
    total_force_y = 0
    target = sprites[0]

    for i in range(num):
        # remove target sprite from the list; save to variable
        if sprites[i].id == ID:
            target = sprites.pop(i)
            break

    for sprite in sprites:
        # Calcualate delta x and y
        distance_x = sprite.rect[0] - target.rect[0]
        distance_y = sprite.rect[1] - target.rect[1]
        # Calculate distance
        total_distance = sqrt((distance_x**2) + (distance_y**2) )
        print(target.id, "dist: ", total_distance)
        if distance_x > 1 or distance_x < -1:
            angle = atan(distance_y/distance_x)
        else:
            angle = 0
        # Calculate total force
        if total_distance > 40:
            total_force = (G*target.mass*sprite.mass)/(total_distance**2) # N (force)
        else:
            total_force = (G*target.mass*sprite.mass)/(40**2) # N (force)

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

        print(target.id, f"Force: ({force_x},{force_y})")
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
