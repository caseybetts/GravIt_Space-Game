# Game involving space rocks
# By Casey Betts

# mustard sun by Martin Cee (softmartin) (c) copyright 2022 Licensed under a Creative Commons Attribution Noncommercial  (3.0) license. http://dig.ccmixter.org/files/softmartin/65383 Ft: subliminal
import math
import pygame
import random

from Button import *
from Calculations import (
    find_force,
    radar_coord_conversion,
    momentum,
    )
from config import *
from SpaceRock import *
from Player import *
from RadarPoint import *
from pygame.locals import *
from Setup import *
from sys import exit

if not pygame.get_init():
    print("Initializing pygame")
    pygame.init()

class Space_Rock_Program():
    """ Contains all 'Space Rock Game' program variables and functions"""
    def __init__(self):

        # Create a display window
        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        pygame.display.set_caption("GravIt!")
        self.win_width,self.win_height = self.screen.get_size()

        # Create a clock to control frames per second
        self.clock = pygame.time.Clock()

        # Font
        self.font = pygame.font.Font(pygame.font.get_default_font(), 40)

        # Button set up
        button_image = pygame.image.load(button_image_location)
        self.real_button = Button(self.win_width/2, (self.win_height/2) - 100, .7, button_image, "Real Gravity")
        self.far_button = Button(self.win_width/2, (self.win_height/2) + 100, .7, button_image, "Far Gravity")

        # Create a Game_Setup object
        self.setup = Game_Setup()

        # Create the player sprite
        self.blob = Player(
                    player_start_mass,
                    player_start_size_x,
                    player_start_size_y
                    )

        # Create radar point for the player
        self.player_point = RadarPoint(0)

        # Calculate map boundaries in pixels based on number of screens map extends to
        self.map_left_boundary = -(int(map_size_width/2))*self.win_width
        self.map_right_boundary = ((int(map_size_width/2))+1)*self.win_width
        self.map_top_boundary =-(int(map_size_height/2))*self.win_height
        self.map_bottom_boundary = ((int(map_size_height/2))+1)*self.win_height
        map_width = self.map_right_boundary - self.map_left_boundary # In pixels
        map_height = self.map_bottom_boundary - self.map_top_boundary # In pixels

        # Create pygame map surface
        self.map = pygame.Surface((map_width, map_height))
        self.map_rect = self.map.get_rect(left = self.map_left_boundary, top = self.map_top_boundary)

        # Calculate radar coords
        radar_left = self.win_width-20-(map_width*radar_reduction)
        radar_top = self.win_height-20-(map_height*radar_reduction)

        # Create Radar screen surface
        self.radar_screen = pygame.Surface(((map_width)*radar_reduction,(map_height)*radar_reduction))
        self.radar_screen.fill((25,25,25))
        self.radar_screen.set_alpha(128)
        self.radar_rect = self.radar_screen.get_rect(left = radar_left, top = radar_top)

        # Create variables for screen position
        self.screen_col = 0
        self.screen_row = 0

        # Create background image surface
        self.bg_image = pygame.image.load("Graphics/bg_stars5.jpg")
        self.bg_image = pygame.transform.scale(self.bg_image, (self.win_width,self.win_height))

        # Import background music
        self.bg_music = pygame.mixer.Sound("audio/background_music.wav")

        # Key down flag and game level flag
        self.key_down_flag = False
        self.game_level = 0

    def update_screen_position(self, player_rect):
        """Given the player's position, this determines the column and row of the screen on the map."""

        # Determine screen column
        if player_rect.left < -2*self.win_width:
            self.screen_col = -3
        elif player_rect.left < -self.win_width:
            self.screen_col = -2
        elif player_rect.left < 0:
            self.screen_col = -1
        elif player_rect.left < self.win_width:
            self.screen_col = 0
        elif player_rect.left < 2*self.win_width:
            self.screen_col = 1
        elif player_rect.left < 3*self.win_width:
            self.screen_col = 2
        else:
            self.screen_col = 3

        # Determine screen column
        if player_rect.top < -2*self.win_height:
            self.screen_row = -3
        elif player_rect.top < -self.win_height:
            self.screen_row = -2
        elif player_rect.top < 0:
            self.screen_row = -1
        elif player_rect.top < self.win_height:
            self.screen_row = 0
        elif player_rect.top < 2*self.win_height:
            self.screen_row = 1
        elif player_rect.top < 3*self.win_height:
            self.screen_row = 2
        else:
            self.screen_row = 3

    def game_loop(self):
        """ Runs the loop for the game"""

        # Create sprite group of space rocks
        self.rocks = self.setup.make_random_rocks(
                                            number_of_rocks,
                                            [self.map_left_boundary,
                                            self.map_right_boundary],
                                            [self.map_top_boundary,
                                            self.map_bottom_boundary])

        # Create sprite group of radar points
        self.point_group = self.setup.make_radar_points(number_of_rocks)
        self.point_group.add(self.player_point)

        # Create sprite group for all sprites
        self.all_sprites = pygame.sprite.Group()
        for rock in self.rocks:
            self.all_sprites.add(rock)
        self.all_sprites.add(self.blob)

        # Create variable for the number of rocks remaining
        self.remaining_rocks = len(self.rocks.sprites())

        # Set the player position and velocity
        self.blob.rect.left = self.win_width/2
        self.blob.rect.top = self.win_height/2
        self.blob.velocity = [0,0]

        while self.game_level == 1:

            # Loop through all the current pygame events in the queue
            for event in pygame.event.get():

                # Check if a key is currently pressed
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.game_level = -1
                    elif event.key == K_d:
                        self.game_level = 0
                    else:
                        # Change the key down flag to True
                        self.key_down_flag = True

                elif event.type == pygame.KEYUP:
                    # Reset the key down flag
                    self.key_down_flag = False

                elif event.type == pygame.QUIT:
                    self.game_level = -1

            # Get the set of keys pressed
            pressed_keys = pygame.key.get_pressed()

            ## Check for collisions
            # Collisions between space rocks. If so, combine space rocks.
            for rock in self.rocks:
                rock_collision = pygame.sprite.spritecollideany(rock, self.rocks)
                if rock_collision.id != rock.id:
                    if abs(rock_collision.velocity[0] - rock.velocity[0]) < 1 and abs(rock_collision.velocity[1] - rock.velocity[1]) < 1:
                        if rock_collision.mass > rock.mass:
                            rock_collision.mass += rock.mass
                            rock_collision.change_size()
                            for point in self.point_group:
                                if point.id == rock_collision.id:
                                    point.change_size(rock_collision.mass)
                                if point.id == rock.id:
                                    point.kill()
                            rock.kill()

                        else:
                            rock.mass += rock_collision.mass
                            for point in self.point_group:
                                if point.id == rock_collision.id:
                                    point.kill()
                            rock_collision.kill()
                        self.remaining_rocks = len(self.rocks.sprites())
                    else:
                        rock_collision.velocity[0] *= collision_slow_percent
                        rock_collision.velocity[1] *= collision_slow_percent
                        rock.velocity[0] *= collision_slow_percent
                        rock.velocity[1] *= collision_slow_percent
            # Collisions between space rocks and the player
            collision_rock = pygame.sprite.spritecollide(self.blob,self.rocks, True)

            if collision_rock:
                # If so, then kill the space rock and add the rock's mass to the player mass
                print( collision_rock[0].mass )
                self.blob.mass += collision_rock[0].mass
                self.blob.velocity = [momentum(self.blob.mass,self.blob.velocity[0], collision_rock[0].mass, collision_rock[0].velocity[0])/2,
                                momentum(self.blob.mass,self.blob.velocity[1], collision_rock[0].mass, collision_rock[0].velocity[1])/2]
                for point in self.point_group:
                    if point.id == collision_rock[0].id:
                        point.kill()
                self.remaining_rocks = len(self.rocks.sprites())


            # Update the coloumn and row of the screen on the map
            self.update_screen_position(self.blob.rect)

            # Update the position of the radare points
            self.point_group.update(
                            self.rocks,
                            self.blob.rect,
                            self.radar_rect,
                            self.map_rect) # Update the radar point positions
            self.blob.thrust_group.update() # Update thrust group


            ## Display: background, player, space rocks, thrust objects, radar screen and text
            self.screen.blit(self.bg_image,(0,0)) # Blit the background

            # Update the player position
            self.blob.update(
                            self.all_sprites,
                            self.key_down_flag,
                            pressed_keys,
                            )

            # Blit the player to the screen
            self.screen.blit(self.blob.surface,[
                            self.blob.rect.left + (-self.screen_col*self.win_width),
                            self.blob.rect.top + (-self.screen_row*self.win_height)])

            # Update and Blit space rocks
            for entity in self.rocks:
                entity.update(self.all_sprites, self.map_rect)
                self.screen.blit(
                            entity.surface,[
                            entity.rect.left + (-self.screen_col*self.win_width),
                            entity.rect.top + (-self.screen_row*self.win_height)])

            # Blit the thrust group with adjusted coordinates
            for sprite in self.blob.thrust_group:
                self.screen.blit(
                            sprite.surface,[
                            sprite.rect.left + (-self.screen_col*self.win_width),
                            sprite.rect.top + (-self.screen_row*self.win_height)])

            # Blit the radar screen on the window
            self.screen.blit(self.radar_screen,(self.radar_rect.left,self.radar_rect.top))

            # Calculate the display position of the shadow of the active screen on the radar
            screen_position = radar_coord_conversion(
                                        self.screen_col*self.win_width,
                                        self.screen_row*self.win_height,
                                        radar_reduction,
                                        self.radar_rect,
                                        self.map_rect
                                        )

            # Draw the shadow of the active screen on the radar screen
            pygame.draw.rect(
                            self.screen,
                            (40,40,40),
                            (   screen_position[0],
                                screen_position[1],
                                self.win_width*radar_reduction,
                                self.win_height*radar_reduction)
                            )

            # Draw the radar points on the screen
            for entity in self.point_group:
                self.screen.blit(entity.surface, entity.rect)

            # Display the current mass of the player
            mass_text_surf = self.font.render(
                                        f'Current Mass: {math.trunc(self.blob.mass)} kg              Space Rocks Remaining: {self.remaining_rocks}',
                                        False,
                                        (64,64,64))
            self.screen.blit(mass_text_surf,(10,10))


            ## Changing game state
            if not self.rocks.sprites():
                self.game_level = 0

            # Finish the loop with the framrate time and pygame flip
            self.clock.tick(framerate)
            pygame.display.flip()

    def menu_loop(self):
        """ Displays the menu with buttons for input from the user"""

        while self.game_level == 0:

            for event in pygame.event.get():

                # Check if a key is currently pressed
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.game_level = -1
                elif event.type == pygame.QUIT:
                    self.game_level = -1

            self.screen.blit(self.bg_image,(0,0)) # Blit the background
            self.screen.blit(self.real_button.image, (self.real_button.rect.x, self.real_button.rect.y))
            self.screen.blit(self.real_button.text, self.real_button.text_rect)

            self.screen.blit(self.far_button.image, (self.far_button.rect.x, self.far_button.rect.y))
            self.screen.blit(self.far_button.text, self.far_button.text_rect)

            # Have buttons check if they are clicked
            if self.real_button.check_mouse():
                self.game_level = 1
                print('real button')
            elif self.far_button.check_mouse():
                print("far button")

            # Finish the loop with the framrate time and pygame flip
            self.clock.tick(framerate)
            pygame.display.flip()

    def program_loop(self):

        # Play background music
        if music_on:
            self.bg_music.play(loops = -1)

        # Contains the loop to render the game and exit on quit event
        while True:

            # Run level 1
            if self.game_level == 1:
                self.game_loop()

            # Display the menu screen
            elif self.game_level == 0:
                self.menu_loop()

            else:
                self.cleanup()

    def cleanup(self):
        pygame.quit()
        exit()
        print("cleanup complete")

if __name__ == "__main__":

    # Create program object and run
    program = Space_Rock_Program()
    program.program_loop()
