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
    display_coord_conversion
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
        self.screen = pygame.display.set_mode((winWidth,winHeight))
        pygame.display.set_caption("GravIt!")

        # Create a clock to control frames per second
        self.clock = pygame.time.Clock()

        # Font
        self.font = pygame.font.Font(pygame.font.get_default_font(), 40)

        # Create a Game_Setup object
        self.setup = Game_Setup()

        # Create the player sprite
        self.blob = Player(
                    player_start_mass,
                    player_start_pos_x,
                    player_start_pos_y,
                    player_start_velocity_x,
                    player_start_velocity_y,
                    player_start_size_x,
                    player_start_size_y
                    )



        # Create Radar screen surface
        self.radar_screen = pygame.Surface(((outer_right-outer_left)*radar_reduction,(outer_bottom-outer_top)*radar_reduction))
        self.radar_screen.fill((20,20,20))
        self.radar_screen.set_alpha(128)

        # Create variables for number of rocks left, game state and screen position

        self.game_active = True
        self.screen_col = 0
        self.screen_row = 0

        # Create background image surface
        self.bg_image = pygame.image.load("Graphics/bg_stars5.jpg")
        self.bg_image = pygame.transform.scale(self.bg_image, (winWidth,winHeight))

        # Import background music
        self.bg_music = pygame.mixer.Sound("audio/background_music.wav")

        # Key down flag and game level flag
        self.key_down_flag = False
        self.game_level = 0

    def update_screen_position(self, player_rect):
        """Given the player's position, this determines the column and row of the screen on the map."""

        # Determine screen column
        if player_rect.left < -2*winWidth:
            self.screen_col = -3
        elif player_rect.left < -winWidth:
            self.screen_col = -2
        elif player_rect.left < 0:
            self.screen_col = -1
        elif player_rect.left < winWidth:
            self.screen_col = 0
        elif player_rect.left < 2*winWidth:
            self.screen_col = 1
        elif player_rect.left < 3*winWidth:
            self.screen_col = 2
        else:
            self.screen_col = 3

        # Determine screen column
        if player_rect.top < -2*winHeight:
            self.screen_row = -3
        elif player_rect.top < -winHeight:
            self.screen_row = -2
        elif player_rect.top < 0:
            self.screen_row = -1
        elif player_rect.top < winHeight:
            self.screen_row = 0
        elif player_rect.top < 2*winHeight:
            self.screen_row = 1
        elif player_rect.top < 3*winHeight:
            self.screen_row = 2
        else:
            self.screen_row = 3

    def game_loop(self):
        """ Runs the first level of the game"""
        print("Running game_loop with gmae level:", self.game_level)

        self.rocks = self.setup.make_random_rocks(number_of_rocks)

        # Create radar points and add them to a sprite group
        self.point_group = self.setup.make_radar_points(number_of_rocks)

        # Create sprite group for all sprites
        self.all_sprites = pygame.sprite.Group()
        for rock in self.rocks:
            self.all_sprites.add(rock)
        self.all_sprites.add(self.blob)

        # Create radar point for the player
        player_point = RadarPoint(0)
        self.point_group.add(player_point)

        self.remaining_rocks = len(self.rocks.sprites())

        while self.game_level == 1:

            # Loop through all the current pygame events in the queue
            for event in pygame.event.get():

                # Check if a key is currently pressed
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.cleanup()
                    elif event.key == K_d:
                        self.game_level = 0
                    else:
                        # Change the key down flag to True
                        self.key_down_flag = True

                elif event.type == pygame.KEYUP:
                    # Reset the key down flag
                    self.key_down_flag = False

                elif event.type == pygame.QUIT:
                    self.cleanup()

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


            ## Update coordinate for: screen and radar points
            self.update_screen_position(self.blob.rect) # Update screen position
            self.point_group.update(
                            self.rocks,
                            self.blob.rect.left,
                            self.blob.rect.top) # Update the radar point positions
            self.blob.thrust_group.update() # Update thrust group


            ## Display: background, player, space rocks, thrust objects, radar screen and text
            self.screen.blit(self.bg_image,(0,0)) # Blit the background

            self.screen.blit(self.blob.surface, self.blob.update(
                                            self.all_sprites,
                                            self.key_down_flag,
                                            pressed_keys,
                                            self.screen_col,
                                            self.screen_row)) # Update/display player
            # Update/display space rocks
            for entity in self.rocks:
                self.screen.blit(
                            entity.surface,
                            entity.update(
                                    self.all_sprites,
                                    self.screen_col,
                                    self.screen_row))

            # Blit the thrust group with adjusted coordinates
            for sprite in self.blob.thrust_group:
                # Change coordinates based on the screen position
                thr_x = sprite.rect.left + (-self.screen_col*winWidth)
                thr_y = sprite.rect.top + (-self.screen_row*winHeight)

                # Blit the thrust sprite on the screen
                self.screen.blit(sprite.surface,(thr_x,thr_y))

            # Blit the radar screen on the window
            self.screen.blit(self.radar_screen,(radar_left,radar_top))
            screen_position = radar_coord_conversion( self.screen_col*winWidth,
                                        self.screen_row*winHeight,
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
                        self.cleanup()
                elif event.type == pygame.QUIT:
                    self.cleanup()

            self.screen.blit(self.bg_image,(0,0)) # Blit the background
            self.screen.blit(real_button.image, (real_button.rect.x, real_button.rect.y))
            self.screen.blit(real_button.text, real_button.text_rect)

            self.screen.blit(far_button.image, (far_button.rect.x, far_button.rect.y))
            self.screen.blit(far_button.text, far_button.text_rect)

            # Have buttons check if they are clicked
            if real_button.check_mouse():
                self.game_level = 1
                print('real button')
            elif far_button.check_mouse():
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
            else:
                self.menu_loop()

    def cleanup(self):
        pygame.quit()
        exit()
        print("cleanup complete")

if __name__ == "__main__":



    # Button set up
    button_image = pygame.image.load(button_image_location)
    real_button = Button(winWidth/2, (winHeight/2) - 100, .7, button_image, "Real Gravity")
    far_button = Button(winWidth/2, (winHeight/2) + 100, .7, button_image, "Far Gravity")

    # Create game object and run
    game = Space_Rock_Program()
    game.program_loop()
