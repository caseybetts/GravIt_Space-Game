# This file holds all the calculation functions for the game

#Constants
G = 6.6743e-11 # m3 kg-1 s-2


# This will take in a group of rocks and determin the displacement of a given rock
def displacement(group,target,framerate):

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
