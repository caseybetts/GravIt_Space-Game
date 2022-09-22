# Game involving space rocks
# By Casey Betts

# mustard sun by Martin Cee (softmartin) (c) copyright 2022 Licensed under a Creative Commons Attribution Noncommercial  (3.0) license. http://dig.ccmixter.org/files/softmartin/65383 Ft: subliminal
import math
import pygame
import random

from Calculations import find_force, radar_coord_conversion, momentum, display_coord_conversion
from config import *
from pygame.locals import *
from sys import exit
from ThrustSprite import ThrustSprite


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

if not pygame.get_init():
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

    def change_size(self):
        """ Change the size of the space rock based on it's mass"""
        if self.mass > 2*big_rock:
            self.surface = pygame.transform.scale(self.surface, (80,80))
            self.surface.set_colorkey((0,0,0), RLEACCEL)
        if self.mass > 4*big_rock:
            self.surface = pygame.transform.scale(self.surface, (120,120))
            self.surface.set_colorkey((0,0,0), RLEACCEL)

    def update(self):
        global _screen_col
        global _screen_row

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

        # Remove space rock if it gets too far away
        if self.rect.left < outer_left or self.rect.right > outer_right:
            self.kill()
        if self.rect.top < outer_top or self.rect.bottom > outer_bottom:
            self.kill()

        ##################### For Testing: Constrain the rocks to the window ##################
        # if self.rect.left < 0: self.velocity[0] = 2
        # if self.rect.right > winWidth: self.velocity[0] = -2
        # if self.rect.top < 0: self.velocity[1] = 2
        # if self.rect.bottom > winHeight: self.velocity[1] = -2

        return [self.rect.left+(-_screen_col*winWidth), self.rect.top + (-_screen_row*winHeight)]

class Player(pygame.sprite.Sprite):
    """This is the player sprite"""
    def __init__(self, mass, x_pos, y_pos, x_velocity, y_velocity, x_size, y_size):
        super(Player,self).__init__()

        # Mass, Position and Velocity parameters initialized
        self.mass = mass
        self.velocity = [x_velocity,y_velocity]
        self.size = [x_size, y_size]
        self.id = 0
        # Create pygame Surface
        self.surface = pygame.image.load("Graphics/GreenBlob.png")
        self.surface = pygame.transform.scale(self.surface, self.size)
        self.surface.set_colorkey((0,0,0), RLEACCEL)
        self.rect = self.surface.get_rect( center = (x_pos,y_pos) )

        # Thrust sound
        self.thrust_sound = pygame.mixer.Sound("audio/thrust.flac")
        self.thrust_sound.set_volume(.5)

    def eject_mass(self, direction):
        ejected = ThrustSprite(self.rect.centerx,self.rect.centery,self.mass,direction)
        thrust_group.add(ejected)

    # Move the sprite based on user keypresses
    def update(self, pressed_keys):

        global _screen_col
        global _screen_row

        x_thrust = 0
        y_thrust = 0
        if pressed_keys[K_UP]:
            y_thrust = -(self.mass*percent_ejection)*thrust_acc      # ejection mass x acceleration
            self.mass *= 1-percent_ejection
            self.eject_mass('down')
            # Play a sound
            self.thrust_sound.play()
        if pressed_keys[K_DOWN]:
            y_thrust = (self.mass*percent_ejection)*thrust_acc       # ejection mass x acceleration
            self.mass *= 1-percent_ejection
            self.eject_mass('up')
            # Play a sound
            self.thrust_sound.play()
        if pressed_keys[K_LEFT]:
            x_thrust = -(self.mass*percent_ejection)*thrust_acc       # ejection mass x acceleration
            self.mass *= 1-percent_ejection
            self.eject_mass('right')
            # Play a sound
            self.thrust_sound.play()
        if pressed_keys[K_RIGHT]:
            x_thrust = (self.mass*percent_ejection)*thrust_acc       # ejection mass x acceleration
            self.mass *= 1-percent_ejection
            self.eject_mass('left')
            # Play a sound
            self.thrust_sound.play()
        if pressed_keys[K_c]:
            self.rect.update((200,200),self.size)

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

        # Determine screen column
        if self.rect.left < 0:
            _screen_col = -1
        if self.rect.left < -winWidth:
            _screen_col = -2
        if self.rect.left < -2*winWidth:
            _screen_col = -3
        if self.rect.left > winWidth:
            _screen_col = 1
        if self.rect.left > 2*winWidth:
            _screen_col = 2
        if self.rect.left > 3*winWidth:
            _screen_col = 3
        if self.rect.left > 0 and self.rect.left < winWidth:
            _screen_col = 0

        # Determine screen column
        _screen_row = 0
        if self.rect.top < 0:
            _screen_row = -1
        if self.rect.top < -winHeight:
            _screen_row = -2
        if self.rect.top < -2*winHeight:
            _screen_row = -3
        if self.rect.top > winHeight:
            _screen_row = 1
        if self.rect.top > 2*winHeight:
            _screen_row = 2
        if self.rect.top > 3*winHeight:
            _screen_row = 3

        return [self.rect.left+(-_screen_col*winWidth), self.rect.top + (-_screen_row*winHeight)]

class RadarPoint(pygame.sprite.Sprite):
    """This is a point on the radar that reflects the location of a space rock"""

    def __init__(self, id):
        super(RadarPoint, self).__init__()
        self.id = id
        # Create pygame Surface
        self.surface = pygame.Surface((1,1))
        self.rect = self.surface.get_rect()

        if id == 0:
            self.surface.fill("Green")
        else:
            self.surface.fill("Red")

    def change_size(self, mass):
        """Chage the size of the radar point"""
        if mass >= 2*big_rock:
            self.surface = pygame.Surface((2,2))
            self.surface.fill("Red")
        if mass >= 4*big_rock:
            self.surface = pygame.Surface((4,4))
            self.surface.fill("Red")


    def update(self):
        # If the point is the player
        if self.id == 0:
            player_coords = radar_coord_conversion(
                                blob.rect[0],
                                blob.rect[1],
                                radar_reduction,
                                radar_left,
                                radar_top,
                                outer_left,
                                outer_top
                                )
            self.rect[0] = player_coords[0]
            self.rect[1] = player_coords[1]
        else:
            # Find the space rock with the same id and change position to match
            alive = False
            for rock in rocks:
                if self.id == rock.id:
                    alive = True
                    rock_coords = radar_coord_conversion(
                                    rock.rect[0],
                                    rock.rect[1],
                                    radar_reduction,
                                    radar_left,
                                    radar_top,
                                    outer_left,
                                    outer_top
                                    )
                    self.rect[0] = rock_coords[0]
                    self.rect[1] = rock_coords[1]
            # If the alive flag does not get put to True then a rock was not found, kill the point
            if not alive: self.kill()

class _Setup():
    "Provides functions needed to set up the game"

    def make_random_rock(self, ID):
        # returns a space rock of random mass and position
        mass = random.choice(MASSES) #random.randint(5,10)*1000000000000000
        x_position = random.randint(outer_left,outer_right)
        y_position = random.randint(outer_top, outer_bottom) #[10-random.randint(1,2),10-random.randint(1,2)]
        x_velocity = random.randint(-1,1)
        y_velocity = random.randint(-1,1)
        rand_rock = SpaceRock( mass, x_position, y_position, x_velocity, y_velocity, ID )
        return rand_rock

    def make_random_rocks(self, num):
        # Create a sprite group to contain random space rocks
        sprite_group = pygame.sprite.Group()
        for i in range(num):
            sprite_group.add(self.make_random_rock(i+1))
        return sprite_group

    def make_radar_points(self, num):
        sprite_group = pygame.sprite.Group()
        for i in range(num):
            point = RadarPoint(i+1)
            sprite_group.add(point)
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
        # Create Radar screen surface
        self.radar_screen = pygame.Surface(((outer_right-outer_left)*radar_reduction,(outer_bottom-outer_top)*radar_reduction))
        self.radar_screen.fill((20,20,20))
        self.radar_screen.set_alpha(128)
        # Create variable to store the number of rocks remaining
        self.remaining_rocks = len(rocks.sprites())
        # Import background music
        self.bg_music = pygame.mixer.Sound("audio/background_music.wav")

    def run(self):

        # Play background music
        # self.bg_music.play(loops = -1)
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
                            rock_collision.change_size()
                            for point in point_group:
                                if point.id == rock_collision.id:
                                    point.change_size(rock_collision.mass)
                                if point.id == rock.id:
                                    point.kill()
                            rock.kill()

                        else:
                            rock.mass += rock_collision.mass
                            for point in point_group:
                                if point.id == rock_collision.id:
                                    point.kill()
                            rock_collision.kill()
                        self.remaining_rocks = len(rocks.sprites())
                    else:
                        rock_collision.velocity[0] *= collision_slow_percent
                        rock_collision.velocity[1] *= collision_slow_percent
                        rock.velocity[0] *= collision_slow_percent
                        rock.velocity[1] *= collision_slow_percent

            # Check if any space rocks have collided with the player
            collision_rock = pygame.sprite.spritecollide(blob,rocks, True)

            if collision_rock:
                # If so, then kill the space rock and add the rock's mass to the player mass
                print( collision_rock[0].mass )
                blob.mass += collision_rock[0].mass
                blob.velocity = [momentum(blob.mass,blob.velocity[0], collision_rock[0].mass, collision_rock[0].velocity[0])/2,
                                momentum(blob.mass,blob.velocity[1], collision_rock[0].mass, collision_rock[0].velocity[1])/2]
                for point in point_group:
                    if point.id == collision_rock[0].id:
                        point.kill()
                self.remaining_rocks = len(rocks.sprites())

            # Update player position
            self.screen.blit(blob.surface, blob.update(pressed_keys))
            # Update space rock positions
            for entity in rocks:
                self.screen.blit(entity.surface, entity.update())
            # Update the radar point positions
            point_group.update()
            # Update the thrust group
            thrust_group.update()
            for entity in thrust_group:
                thr_x = entity.rect.left+(-_screen_col*winWidth)
                thr_y = entity.rect.top + (-_screen_row*winHeight)
                self.screen.blit(entity.surface,(thr_x,thr_y))

            # Draw a rectangle for the radar view
            self.screen.blit(self.radar_screen,(radar_left,radar_top))
            # pygame.draw.rect(
            #     self.screen,
            #     (20,20,20),
            #     (radar_left,
            #         radar_top,
            #         (outer_right-outer_left)*radar_reduction,
            #         (outer_bottom-outer_top)*radar_reduction)
            #         )
            # Draw a rectangle for the screen location on the radar screen
            screen_position = radar_coord_conversion( _screen_col*winWidth,
                                        _screen_row*winHeight,
                                        radar_reduction,
                                        radar_left,
                                        radar_top,
                                        outer_left,
                                        outer_top
                                        )
            pygame.draw.rect(
                            self.screen,
                            (40,40,40),
                            (   screen_position[0],
                                screen_position[1],
                                winWidth*radar_reduction,
                                winHeight*radar_reduction)
                            )

            # Draw the radar points on the screen
            for entity in point_group:
                self.screen.blit(entity.surface, entity.rect)

            # End the game when all space rocks are gone
            if not rocks.sprites():
                print("You Win!")
                self.cleanup()

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
    # Create the rocks and add them to a sprite group
    setup = _Setup()
    rocks = setup.make_random_rocks(number_of_rocks)
    # Create radar points and add them to a sprite group
    point_group = setup.make_radar_points(number_of_rocks)
    # Create radar point for the player
    player_point = RadarPoint(0)
    point_group.add(player_point)
    # Create the player sprite
    blob = Player(
                player_start_mass,
                player_start_pos_x,
                player_start_pos_y,
                player_start_velocity_x,
                player_start_velocity_y,
                player_start_size_x,
                player_start_size_y
                )
    # Sprite group for all sprites
    all_sprites = pygame.sprite.Group()
    for rock in rocks:
        all_sprites.add(rock)
    all_sprites.add(blob)
    # Sprite group just for the player
    player_group = pygame.sprite.Group()
    player_group.add(blob)
    # Sprite group for the thrust sprites
    thrust_group = pygame.sprite.Group()

    # Create game object and run
    game = Game()
    game.run()
