# Game involving space rocks
# By Casey Betts

# mustard sun by Martin Cee (softmartin) (c) copyright 2022 Licensed under a Creative Commons Attribution Noncommercial  (3.0) license. http://dig.ccmixter.org/files/softmartin/65383 Ft: subliminal
import pygame
import random

from Button import *
from Calculations import (
    find_force,
    radar_coord_conversion,
    momentum,
    exponent_split,
    elastic_momentum
    )
from config import *
from Enemy import *
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
        self.win_width, self.win_height = self.screen.get_size()

        # Create a clock to control frames per second
        self.clock = pygame.time.Clock()

        # Fonts
        self.font = pygame.font.Font(pygame.font.get_default_font(), 40)
        self.level_font = pygame.font.Font(pygame.font.get_default_font(), 150)
        self.win_font = pygame.font.Font(pygame.font.get_default_font(), 150)
        self.inst_font = pygame.font.Font(pygame.font.get_default_font(), 30)

        # Button set up
        button_image = pygame.image.load(button_image_location)
        self.real_button = Button(self.win_width/2, (self.win_height/2) - 100, .7, "GravIt!", "Black", 200, button_image)
        self.far_button = Button(self.win_width/2, (self.win_height/2) + 100, .7, "Speed Round", "Black", 200, button_image)
        self.exit_button = Button(self.win_width - 20, 20, .5, "X", (64,64,64), 100)
        up_button_image = pygame.image.load(up_button_image_location)
        down_button_image = pygame.image.load(down_button_image_location)
        self.increase_mass_button = Button(30, (self.win_height/4)-40, .25, "", "Blue", 100, up_button_image)
        self.decrease_mass_button = Button(30, (self.win_height/4)+40, .25, "", "Blue", 100, down_button_image)

        # Create a Game_Setup object
        self.setup = Game_Setup()

        # Create the player sprite
        self.blob = Player(
                    PLAYER_START_MASS,
                    player_start_size_x,
                    player_start_size_y
                    )

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
        radar_left = self.win_width-20-(map_width*RADAR_REDUCTION)
        radar_top = self.win_height-20-(map_height*RADAR_REDUCTION)

        # Create Radar screen surface
        self.radar_screen = pygame.Surface(((map_width)*RADAR_REDUCTION,(map_height)*RADAR_REDUCTION))
        self.radar_screen.fill((25,25,25))
        self.radar_screen.set_alpha(128)
        self.radar_rect = self.radar_screen.get_rect(left = radar_left, top = radar_top)

        # Create variables for screen position
        self.screen_col = 0
        self.screen_row = 0

        # Create background image surface
        self.bg_image = pygame.image.load(background_image_location)
        self.bg_image = pygame.transform.scale(self.bg_image, (self.win_width,self.win_height))

        # Import background music
        self.bg_music = pygame.mixer.Sound(background_music_location)

        # Create a level event to start the next level at a given interval
        self.level_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.level_timer, 10000)

        # Variables
        self.key_down_flag = False
        self.number_of_rocks = 0
        self.game_level = 0
        self.win_mass = 0
        self.level_text_count = 0
        self.space_rock_set = []
        self.grey_collision_flag = 1
        self.enemy_grey_collision_flag = 1

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

    def set_level_parameters(self):

        if self.game_level == 1:
            self.number_of_rocks = 90
            self.win_mass = 6e15
            self.brown_space_rock_set = LEVEL_1_BROWN_SET
            self.grey_space_rock_set = LEVEL_1_GREY_SET
            self.enemy_specs = LEVEL_1_ENEMY_SPECS
        elif self.game_level == 2:
            self.number_of_rocks = 50
            self.win_mass = 8e15
            self.brown_space_rock_set = LEVEL_2_BROWN_SET
            self.grey_space_rock_set = LEVEL_2_GREY_SET
            self.enemy_specs = LEVEL_2_ENEMY_SPECS
        elif self.game_level == 3:
            self.number_of_rocks = 20
            self.win_mass = 10e15
            self.brown_space_rock_set = LEVEL_3_BROWN_SET
            self.grey_space_rock_set = LEVEL_3_GREY_SET
            self.enemy_specs = LEVEL_3_ENEMY_SPECS

        self.level_text_count = 100

        print("Level parameters set ")

    def release_space_rocks(self):
        print("releasing rocks")
        if self.game_level == 1:
            new_rocks = self.setup.rock_generator(self.brown_space_rock_set, "Brown", self.win_width, self.win_height)
        for rock in new_rocks:
            self.brown_rocks.add(rock)
            self.all_rocks.add(rock)
            self.all_sprites.add(rock)
            print(rock.velocity)

    def release_enemies(self):
        pass

    def collision_handler(self):
        """ Handels collision events between sprites """

        # Get collided sprites between player and enemies

        # Get collided sprites between player and brown rocks

        # Get collided sprites between player and grey rocks

        # Get collided sprites between enemies and enemies
        myCollisions = pygame.sprite.groupcollide(self.brown_rocks, self.brown_rocks, False, False)
        for element in myCollisions:
            print(element)



    def game_loop(self, level):
        """ Runs the loop for the game"""
        print("Running Game Loop")

        # Set the parameters for the current game level
        self.set_level_parameters()

        # Create text object for displaying the level
        level_text = self.level_font.render('Level {}'.format(self.game_level), False, (84,84,84))

        # Create the enemy
        self.enemies = self.setup.enemy_generator(self.enemy_specs)

        # Create sprite group of space rocks
        self.brown_rocks = self.setup.rock_generator(self.brown_space_rock_set, "Brown", self.win_width, self.win_height)
        self.grey_rocks = self.setup.rock_generator(self.grey_space_rock_set, "Grey", self.win_width, self.win_height)

        # Create sprite group for all rocks and all sprites
        self.all_rocks = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        # Add the brown and grey rocks to both sprite groups
        for rock in self.brown_rocks:
            self.all_sprites.add(rock)
            self.all_rocks.add(rock)
        for rock in self.grey_rocks:
            self.all_sprites.add(rock)
            self.all_rocks.add(rock)
        for sprite in self.enemies:
            self.all_sprites.add(sprite)
        # Add the player to the all sprites group
        self.all_sprites.add(self.blob)

        # Create variable for the number of rocks remaining
        self.remaining_rocks = len(self.brown_rocks.sprites()) + len(self.grey_rocks.sprites())

        # Set the player position and velocity
        self.blob.rect.left = self.win_width/2
        self.blob.rect.top = self.win_height/2
        self.blob.velocity = [0,0]

        while self.game_level == level:

            self.events = pygame.event.get()
            # Loop through all the current pygame events in the queue
            for event in self.events:
                # Check if a key is currently pressed
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.game_level = -1
                    elif event.key == K_d:
                        self.game_level = 0
                    elif event.key == K_m:
                        self.blob.mass *= 1.1
                    elif event.key == K_LSHIFT and event.key == K_g:
                        print("Next Level")
                    else:
                        # Change the key down flag to True
                        self.key_down_flag = True

                elif event.type == pygame.KEYUP:
                    # Reset the key down flag
                    self.key_down_flag = False

                elif event.type == self.level_timer:
                    print("level timer")
                    # Increase the level and release the next wave
                    self.release_space_rocks()
                    self.release_enemies()

                elif event.type == pygame.QUIT:
                    self.game_level = -1

            # Get the set of keyboard keys pressed
            pressed_keys = pygame.key.get_pressed()

            # collision_handler
            #self.collision_handler()

            ## Check for collisions
            # Collisions between brown space rocks. If so, combine space rocks.
            for rock in self.brown_rocks:
                rock_collision = pygame.sprite.spritecollideany(rock, self.brown_rocks)

                if rock_collision.id != rock.id:

                    if abs(rock_collision.velocity[0] - rock.velocity[0]) < 1 and abs(rock_collision.velocity[1] - rock.velocity[1]) < 1:

                        if rock_collision.mass > rock.mass:
                            rock_collision.mass += rock.mass
                            rock_collision.change_size()
                            rock.kill()
                        else:
                            rock.mass += rock_collision.mass
                            rock_collision.kill()
                        self.remaining_rocks = len(self.brown_rocks.sprites())
                    else:
                        rock_collision.velocity[0] *= collision_slow_percent
                        rock_collision.velocity[1] *= collision_slow_percent
                        rock.velocity[0] *= collision_slow_percent
                        rock.velocity[1] *= collision_slow_percent

            # Collisions between grey space rocks. If so, combine space rocks.
            for rock in self.grey_rocks:
                rock_collision = pygame.sprite.spritecollideany(rock, self.grey_rocks)
                if rock_collision.id != rock.id:
                    if abs(rock_collision.velocity[0] - rock.velocity[0]) < 1 and abs(rock_collision.velocity[1] - rock.velocity[1]) < 1:
                        if rock_collision.mass > rock.mass:
                            rock_collision.mass += rock.mass
                            rock_collision.change_size()
                            rock.kill()

                        else:
                            rock.mass += rock_collision.mass
                            rock_collision.kill()
                        self.remaining_rocks = len(self.grey_rocks.sprites())+len(self.brown_rocks.sprites())
                    else:
                        rock_collision.velocity[0] *= collision_slow_percent
                        rock_collision.velocity[1] *= collision_slow_percent
                        rock.velocity[0] *= collision_slow_percent
                        rock.velocity[1] *= collision_slow_percent

            # Collisions with the player
            player_collisions = pygame.sprite.spritecollide(self.blob,self.all_sprites, False)
            if len(player_collisions) == 2:
                for sprite in player_collisions:
                    # Check if the sprite is an enemy
                    if sprite.id >= 1000:
                        self.blob.collision("Enemy", sprite)
                    # Or if the sprite is a grey rock
                    elif sprite.id > 200:
                        self.blob.collision("Grey", sprite)
                    # Otherwise it must be a brown rock
                    elif sprite.id > 0:
                        self.blob.collision("Brown", sprite)
                        self.remaining_rocks -= 1
            else:
                self.blob.player_collisions = False
                self.blob.enemy_collision_flag = False
                self.blob.grey_collision_flag = False


            # Collisions with the enemies
            for enemy in self.enemies:
                enemy_collisions = pygame.sprite.spritecollide(enemy,self.all_sprites, False)
                if len(enemy_collisions) == 2:
                    for sprite in enemy_collisions:
                        # Check if the sprite is the player:
                        if sprite.id == 0:
                            enemy.collision("Player", sprite)
                        # Or if the sprite is an enemy
                        elif sprite.id >= 1000:
                            enemy.collision("Enemy", sprite)
                        # Or if the sprite is a grey rock
                        elif sprite.id > 200:
                            enemy.collision("Grey", sprite)
                        # Otherwise it must be a brown rock
                        elif sprite.id > 0:
                            enemy.collision("Brown", sprite)
                            self.remaining_rocks -= 1
                    else:
                        enemy.player_collision_flag = False
                        enemy.enemy_collision_flag = False
                        enemy.grey_collision_flag = False

            # Update the coloumn and row of the screen on the map
            self.update_screen_position(self.blob.rect)

            # Blit the background
            self.screen.blit(self.bg_image,(0,0))

            # Blit the radar screen on the window
            self.screen.blit(self.radar_screen,(self.radar_rect.left,self.radar_rect.top))

            # Calculate the display position of the shadow of the active screen on the radar
            screen_position = radar_coord_conversion(
                                        self.screen_col*self.win_width,
                                        self.screen_row*self.win_height,
                                        RADAR_REDUCTION,
                                        self.radar_rect,
                                        self.map_rect
                                        )

            # Draw the shadow of the active screen on the radar screen
            pygame.draw.rect(
                            self.screen,
                            (40,40,40),
                            (   screen_position[0],
                                screen_position[1],
                                self.win_width*RADAR_REDUCTION,
                                self.win_height*RADAR_REDUCTION)
                            )

            # Update the player position
            self.blob.update(
                            self.all_sprites,
                            self.key_down_flag,
                            pressed_keys,
                            self.screen,
                            self.screen_col,
                            self.screen_row,
                            self.win_width,
                            self.win_height,
                            self.map_rect,
                            self.radar_rect
                            )

            # Update the enemy position
            self.enemies.update(
                            self.all_sprites,
                            self.key_down_flag,
                            self.events,
                            self.screen,
                            self.screen_col,
                            self.screen_row,
                            self.win_width,
                            self.win_height,
                            self.map_rect,
                            self.radar_rect
                            )

            # Update the brown_rocks
            for entity in self.brown_rocks:
                entity.update(
                                self.all_sprites,
                                self.map_rect,
                                self.screen,
                                self.screen_col,
                                self.screen_row,
                                self.win_width,
                                self.win_height,
                                self.radar_rect)

            # Update the space grey rocks
            for entity in self.grey_rocks:
                entity.update(
                                self.all_sprites,
                                self.map_rect,
                                self.screen,
                                self.screen_col,
                                self.screen_row,
                                self.win_width,
                                self.win_height,
                                self.radar_rect)

            # Display the current percent_ejection value
            percent_ejection_label_surf = self.font.render('Thrust Control', False, (64,64,64))
            percent_ejection_surf = self.font.render('{}'.format(round(self.blob.percent_ejection,4)), False, (64,64,64))
            self.screen.blit(percent_ejection_label_surf, (15, (self.win_height/4)-150))
            self.screen.blit(percent_ejection_surf,(15,(self.win_height/4)-100))

            # Display the current mass of the player
            disp_mass = exponent_split(self.blob.mass)
            mass_text_surf = self.font.render(
                                        'Current Mass: {mass} e {disp_mass} kg              Space Rocks Remaining: {remaining_rocks}'.format(mass=round(disp_mass[0],2),disp_mass=disp_mass[1],remaining_rocks=self.remaining_rocks),
                                        False,
                                        (64,64,64))
            self.screen.blit(mass_text_surf,(10,10))

            # Blit the exit button
            self.screen.blit(self.exit_button.text, self.exit_button.text_rect)

            # BLit the mass changing buttons
            self.screen.blit(self.increase_mass_button.image, self.increase_mass_button.rect)
            self.screen.blit(self.decrease_mass_button.image, self.decrease_mass_button.rect)

            # Display the current level at start of level
            if self.level_text_count > 0:
                self.screen.blit(level_text,((self.win_width-level_text.get_width())/2, (self.win_height-level_text.get_height())/2))
                self.level_text_count -= 1

            # Check up/down buttons for mouse click
            if self.increase_mass_button.check_mouse():
                self.blob.percent_ejection *= 1.1
            if self.decrease_mass_button.check_mouse():
                self.blob.percent_ejection *= .9

            # Check exit button for a click
            if self.exit_button.check_mouse():
                self.game_level = -1

            # Check if your mass is great enough to win the level
            if self.blob.mass > self.win_mass:
                self.game_level += 1

            # Finish the loop with the framrate time and pygame flip
            self.clock.tick(framerate)
            pygame.display.flip()

    def menu_loop(self):
        """ Displays the menu with buttons for input from the user"""

        # Display the winning message
        instruction_text1 = self.inst_font.render("Used the arrow keys to expel matter and propel yourself through",
                                                False,
                                                (110,100,100))

        instruction_text2 = self.inst_font.render("the field of space rocks. If you can collide with a rock you can eat it and",
                                                False,
                                                (110,100,100))

        instruction_text3 = self.inst_font.render("increase your mass. Grow your mass enough to get to the next level!",
                                                False,
                                                (110,100,100))
        while self.game_level == 0:

            for event in pygame.event.get():

                # Check if a key is currently pressed
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.game_level = -1
                    elif event.key == K_w:
                        self.game_level = 4
                elif event.type == pygame.QUIT:
                    self.game_level = -1
            # Blit the background
            self.screen.blit(self.bg_image,(0,0))

            # Blit the instruction text
            self.screen.blit(instruction_text1,(self.win_width/4, self.win_height - 200))
            self.screen.blit(instruction_text2,(self.win_width/4 - 20, self.win_height - 160))
            self.screen.blit(instruction_text3,(self.win_width/4, self.win_height - 120))

            # Blit the real_button image and text
            self.screen.blit(self.real_button.image, (self.real_button.rect.x, self.real_button.rect.y))
            self.screen.blit(self.real_button.text, self.real_button.text_rect)

            # Blit the far button image and text
            self.screen.blit(self.far_button.image, (self.far_button.rect.x, self.far_button.rect.y))
            self.screen.blit(self.far_button.text, self.far_button.text_rect)

            # Blit the exit button
            self.screen.blit(self.exit_button.text, self.exit_button.text_rect)

            # Have buttons check if they are clicked
            if self.exit_button.check_mouse():
                self.game_level = -1

            if self.real_button.check_mouse():
                self.real_button.button_sound.play()
                self.game_level = 1

            elif self.far_button.check_mouse():
                self.far_button.button_sound.play()
                self.game_level = 1

            # Finish the loop with the framrate time and pygame flip
            self.clock.tick(framerate)
            pygame.display.flip()

    def win_loop(self):
        """ Displays the congradulations message when you win!"""
        # Blit the background
        self.screen.blit(self.bg_image,(0,0))

        # Display the winning message
        winning_message = self.win_font.render('You Win!', False,("#8eb8d4"))
        self.screen.blit(winning_message,((self.win_width-winning_message.get_width())/2, (self.win_height-winning_message.get_height())/2))

        # Blit the exit button
        self.screen.blit(self.exit_button.text, self.exit_button.text_rect)

        while self.game_level > 0:

            # Iterate through all the current pygame events in the queue
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

            # Have buttons check if they are clicked
            if self.exit_button.check_mouse():
                self.game_level = -1

            # Finish the loop with the framrate time and pygame flip
            self.clock.tick(framerate)
            pygame.display.flip()

    def cleanup(self):
        """ Exits pygame and ends the program """
        print("running cleanup")
        pygame.quit()
        exit()

    def program_loop(self):

        # Play background music
        if music_on:
            self.bg_music.play(loops = -1)

        # Contains the loop to render the game and exit on quit event
        while self.game_level > -1:

            # Run level
            if self.game_level > 3:
                self.win_loop()

            elif self.game_level > 0:
                self.game_loop(self.game_level)

            # Display the menu screen
            elif self.game_level == 0:
                self.menu_loop()

        self.cleanup()

if __name__ == "__main__":

    # Create program object and run
    program = Space_Rock_Program()
    program.program_loop()
