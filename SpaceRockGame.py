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
    calculate_collision_force
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
        self.next_level_font = pygame.font.Font(pygame.font.get_default_font(), 40)
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
                    PLAYER_STARAT_SIZE
                    )

        # Calculate map boundaries in pixels based on number of screens map extends to
        self.map_left_boundary = -(int(MAP_SIZE_WIDTH/2))*self.win_width
        self.map_right_boundary = ((int(MAP_SIZE_WIDTH/2))+1)*self.win_width
        self.map_top_boundary =-(int(MAP_SIZE_HEIGHT/2))*self.win_height
        self.map_bottom_boundary = ((int(MAP_SIZE_HEIGHT/2))+1)*self.win_height
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
        self.radar_screen.fill((30,30,30))
        self.radar_screen.set_alpha(128)
        self.radar_rect = self.radar_screen.get_rect(left = radar_left, top = radar_top)

        # Create background image surface
        self.bg_image = pygame.image.load(background_image_location)
        self.bg_image = pygame.transform.scale(self.bg_image, (self.win_width,self.win_height))

        # Import background music
        self.bg_music = pygame.mixer.Sound(background_music_location)

        # Create a level event to start the next level at a given interval
        self.level_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.level_timer, 5000)

        # Game level variables
        self.level_won = False
        self.game_level = 0
        self.win_mass = 0
        self.level_text_count = 0

        # Variables
        self.key_down_flag = False
        self.number_of_rocks = 0
        self.space_rock_set = []
        self.colliding_enemies = 1

    def set_level_parameters(self):

        # Reset the win flag
        self.level_won = False

        # Set parameters for each level
        if self.game_level == 1:
            self.number_of_rocks = 90
            self.win_mass = 6e15
            self.brown_space_rock_set = LEVEL_1_BROWN_SET
            self.grey_space_rock_set = LEVEL_1_GREY_SET
            self.enemy_specs = LEVEL_1_ENEMY_SPECS
        elif self.game_level == 2:
            self.number_of_rocks = 50
            self.win_mass = 10e15
            self.brown_space_rock_set = LEVEL_2_BROWN_SET
            self.grey_space_rock_set = LEVEL_2_GREY_SET
            self.enemy_specs = LEVEL_2_ENEMY_SPECS
        elif self.game_level == 3:
            self.number_of_rocks = 20
            self.win_mass = 14e15
            self.brown_space_rock_set = LEVEL_3_BROWN_SET
            self.grey_space_rock_set = LEVEL_3_GREY_SET
            self.enemy_specs = LEVEL_3_ENEMY_SPECS

        self.level_text_count = 100

        print("Level parameters set ")

    def release_space_rocks(self):

        rock_id = 0
        # Find the highest rock id
        for rock in self.all_rocks:
            if rock.id > rock_id:
                rock_id = rock.id

        if self.game_level == 1:
            rock = SpaceRock((rock_id + 1), "BIG_MASS", "Brown", .5*self.win_width, -4*self.win_height, 0, 2)
            self.brown_rocks.add(rock)
            self.all_rocks.add(rock)
            self.all_sprites.add(rock)

        elif self.game_level == 2:
            rock = SpaceRock((rock_id + 1), "BIG_MASS", "Grey", .5*self.win_width, -4*self.win_height, 0, 2)
            self.grey_rocks.add(rock)
            self.all_rocks.add(rock)
            self.all_sprites.add(rock)

    def release_enemies(self):
        pass

    def collision_handler(self):
        """ Handels collision events between sprites """

        ############# PLAYER AND ENEMIES #############
        # Get collided sprites
        player_enemy_collisions = pygame.sprite.spritecollide(self.blob, self.enemies, False)

        # Create a list of enemies that were not colliding with the player before, but are now
        new_collisions = [x for x in player_enemy_collisions if x not in self.blob.colliding_enemies]

        # Create a list of enemies that were colliding with the player, but are not any more
        no_longer_colliding = [x for x in self.blob.colliding_enemies if x not in player_enemy_collisions]

        # print("blob.colliding_enemies:", self.blob.colliding_enemies)

        for sprite in new_collisions:
            # Add sprite to colliding enemies list
            self.blob.colliding_enemies.append(sprite)

        for sprite in self.blob.colliding_enemies:
            # Calculate force on each sprite
            forces = calculate_collision_force(self.blob, sprite)
            # Update respective collision_force values
            self.blob.collision_force[0] += forces[0][0]
            self.blob.collision_force[1] += forces[0][1]
            sprite.collision_force[0] += forces[1][0]
            sprite.collision_force[1] += forces[1][1]


        for sprite in no_longer_colliding:
            self.blob.colliding_enemies.remove(sprite)

        ############# PLAYER AND BROWN ROCKS #############
        # Get collided sprites
        player_brown_collisions = pygame.sprite.spritecollide(self.blob,self.brown_rocks, True)

        for sprite in player_brown_collisions:
            # Add the rock's mass to the player mass
            self.blob.mass += sprite.mass
            self.blob.velocity = [momentum(self.blob.mass,self.blob.velocity[0], sprite.mass, sprite.velocity[0])/2,
                            momentum(self.blob.mass,self.blob.velocity[1], sprite.mass, sprite.velocity[1])/2]
            self.blob.gulp_sound.play()

        ############# PLAYER AND GREY ROCKS #############
        # Get collided sprites
        player_grey_collisions = pygame.sprite.spritecollide(self.blob,self.grey_rocks, False)

        # Create a list of grey rocks that were not colliding with the player, but are now
        new_collisions = [x for x in player_grey_collisions if x not in self.blob.colliding_grey]

        # Create a list of grey rocks that were colliding with the player, but no longer are
        no_longer_colliding = [x for x in self.blob.colliding_grey if x not in player_grey_collisions]

        for sprite in new_collisions:
            # Add sprite to colliding enemies list
            self.blob.colliding_grey.append(sprite)

        for sprite in self.blob.colliding_grey:
            # Calculate force on each sprite
            forces = calculate_collision_force(self.blob, sprite)
            # Update respective collision_force values
            self.blob.collision_force[0] += forces[0][0]
            self.blob.collision_force[1] += forces[0][1]
            sprite.collision_force[0] += forces[1][0]
            sprite.collision_force[1] += forces[1][1]

        for sprite in no_longer_colliding:
            self.blob.colliding_grey.remove(sprite)

        # ############# ENEMIES AND ENEMIES #############
        # Get collided sprites
        enemy_collisions = pygame.sprite.groupcollide(self.enemies, self.enemies, False, False)

        for enemy in enemy_collisions:
            # Create a list of enemies that were not colliding with this enemy before, but are now
            new_collisions = [x for x in enemy_collisions[enemy] if x not in enemy.colliding_enemies]

            # Create a list of enemies that were colliding with this enemy, but are not any more
            no_longer_colliding = [x for x in enemy.colliding_enemies if x not in enemy_collisions[enemy]]

            for sprite in new_collisions:
                # Add sprite to colliding enemies list
                enemy.colliding_enemies.append(sprite)

            for sprite in enemy.colliding_enemies:
                # Calculate force on each sprite
                forces = calculate_collision_force(enemy, sprite)

                # Update respective collision_force values
                enemy.collision_force[0] += forces[0][0]/2
                enemy.collision_force[1] += forces[0][1]/2
                sprite.collision_force[0] += forces[1][0]/2
                sprite.collision_force[1] += forces[1][1]/2

            for sprite in no_longer_colliding:
                    enemy.colliding_enemies.remove(sprite)

        ############# ENEMIES AND BROWN ROCKS #############
        # Get collided sprites
        enemy_brown_collisions = pygame.sprite.groupcollide(self.enemies,self.brown_rocks, False, False)

        for enemy in enemy_brown_collisions:

            for sprite in enemy_brown_collisions[enemy]:

                # Add the rock's mass to the enemies mass
                enemy.mass += sprite.mass

                # Reduce the velocity using the momentum function
                enemy = [momentum(enemy.mass, enemy.velocity[0], sprite.mass, sprite.velocity[0])/2,
                                momentum(enemy.mass, enemy.velocity[1], sprite.mass, sprite.velocity[1])/2]

                # Kill the space rock
                sprite.kill()

        ############# ENEMIES AND GREY ROCKS #############
        # Get collided sprites
        enemy_grey_collisions = pygame.sprite.groupcollide(self.enemies, self.grey_rocks, False, False)

        for enemy in enemy_grey_collisions:
            # Create a list of grey rocks that were not colliding with this enemy before, but are now
            new_collisions = [x for x in enemy_grey_collisions[enemy] if x not in enemy.colliding_grey]

            # Create a list of grey rocks that were colliding with this enemy, but are not any more
            no_longer_colliding = [x for x in enemy.colliding_grey if x not in enemy_grey_collisions[enemy]]

            for sprite in new_collisions:
                # Add sprite to colliding enemies list
                enemy.colliding_grey.append(sprite)

            for sprite in enemy.colliding_grey:
                # Calculate force on each sprite
                forces = calculate_collision_force(enemy, sprite)
                # Update respective collision_force values
                enemy.collision_force[0] += forces[0][0]/2
                enemy.collision_force[1] += forces[0][1]/2
                sprite.collision_force[0] += forces[1][0]/2
                sprite.collision_force[1] += forces[1][1]/2

            for sprite in no_longer_colliding:
                enemy.colliding_grey.remove(sprite)

        ############# BROWN ROCKS AND BROWN ROCKS #############
        # Get collided sprites
        brown_collisions = pygame.sprite.groupcollide(self.brown_rocks, self.brown_rocks, False, False)

        for rock in brown_collisions:
            # For every brown rock that is currently in the colliding list (this is every rock since it counts collisions with itself, but we handle that next)

            if len(brown_collisions[rock]) > 1:
                # If it is colliding with a rock in addition to itself

                for sprite in brown_collisions[rock]:
                    # For each rock in the collision list for this rock (Again this will include itself)

                    if rock.id != sprite.id:
                        # If the collision rock is not itself

                        if abs(sprite.velocity[0] - rock.velocity[0]) < 1 and abs(sprite.velocity[1] - rock.velocity[1]) < 1:
                            # Determine if they are moving together

                            if rock.mass >= sprite.mass:
                                # Choose the larger of the two rocks to keep

                                rock.mass += sprite.mass
                                rock.change_size()

                                # Ensure the pair of rocks are only addressed once
                                brown_collisions[sprite] = []

                                # Kill the smaller space rock
                                sprite.kill()

                                # Update the total number of rocks to reflect the combination
                                self.remaining_rocks -= 1
                            else:
                                # Choose the larger of the two rocks to keep

                                sprite.mass += rock.mass
                                sprite.change_size()

                                # Ensure the pair of rocks are only addressed once
                                brown_collisions[sprite] = []

                                # Kill the smaller space rock
                                rock.kill()

                                # Update the total number of rocks to reflect the combination
                                self.remaining_rocks -= 1

                        else:
                            sprite.velocity[0] *= collision_slow_percent
                            sprite.velocity[1] *= collision_slow_percent
                            rock.velocity[0] *= collision_slow_percent
                            rock.velocity[1] *= collision_slow_percent

        ############# GREY ROCKS AND GREY ROCKS #############
        # Get collided sprites
        grey_collisions = pygame.sprite.groupcollide(self.grey_rocks, self.grey_rocks, False, False)

        for rock in grey_collisions:
            # For every grey rock that is currently in the colliding list (this is every rock since it counts collisions with itself, but we handle that next)

            if len(grey_collisions[rock]) > 1:

                for sprite in grey_collisions[rock]:

                    if rock.id != sprite.id:

                        if abs(sprite.velocity[0] - rock.velocity[0]) < 1 and abs(sprite.velocity[1] - rock.velocity[1]) < 1:
                            # Determine if they are moving together

                            if rock.mass >= sprite.mass:
                                # Choose the larger of the two rocks to keep

                                rock.mass += sprite.mass
                                rock.change_size()

                                # Ensure the pair of rocks are only addressed once
                                grey_collisions[sprite] = []

                                # Kill the smaller space rock
                                sprite.kill()

                                # Update the total number of rocks to reflect the combination
                                self.remaining_rocks -= 1
                            else:
                                # Choose the larger of the two rocks to keep

                                sprite.mass += rock.mass
                                sprite.change_size()

                                # Ensure the pair of rocks are only addressed once
                                grey_collisions[sprite] = []

                                # Kill the smaller space rock
                                rock.kill()

                                # Update the total number of rocks to reflect the combination
                                self.remaining_rocks -= 1

                        else:
                            sprite.velocity[0] *= collision_slow_percent
                            sprite.velocity[1] *= collision_slow_percent
                            rock.velocity[0] *= collision_slow_percent
                            rock.velocity[1] *= collision_slow_percent


        ############# BROWN ROCKS AND GREY ROCKS #############
        # Get collided sprites
        brown_collisions = pygame.sprite.groupcollide(self.brown_rocks, self.grey_rocks, False, False)

        for rock in brown_collisions:

            if len(brown_collisions[rock]) > 1:

                for sprite in brown_collisions[rock]:
                    sprite.velocity[0] *= collision_slow_percent
                    sprite.velocity[1] *= collision_slow_percent
                    rock.velocity[0] *= collision_slow_percent
                    rock.velocity[1] *= collision_slow_percent

    def update_sprite_positions(self):
        """ Update the posistions of all the sprites """

        # Get the set of keyboard keys pressed
        pressed_keys = pygame.key.get_pressed()

        # Update the player position
        self.blob.update(
                        self.all_sprites,
                        self.key_down_flag,
                        pressed_keys,
                        self.events,
                        self.screen,
                        self.blob.screen_row,
                        self.blob.screen_col,
                        self.win_width,
                        self.win_height,
                        self.map_rect,
                        self.radar_rect
                        )

        # Update the enemy position
        self.enemies.update(
                        self.all_sprites,
                        self.key_down_flag,
                        pressed_keys,
                        self.events,
                        self.screen,
                        self.blob.screen_row,
                        self.blob.screen_col,
                        self.win_width,
                        self.win_height,
                        self.map_rect,
                        self.radar_rect
                        )

        # Update all the rocks
        for entity in self.all_rocks:
            entity.update(
                            self.all_sprites,
                            self.map_rect,
                            self.screen,
                            self.blob.screen_col,
                            self.blob.screen_row,
                            self.win_width,
                            self.win_height,
                            self.radar_rect)

    def heads_up_display(self):
        """ Display all text and radar objects during gameplay """

        # Blit the radar screen on the window
        self.screen.blit(self.radar_screen,(self.radar_rect.left,self.radar_rect.top))

        # Calculate the display position of the shadow of the active screen on the radar
        screen_position = radar_coord_conversion(
                                    self.blob.screen_col*self.win_width,
                                    self.blob.screen_row*self.win_height,
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

        # If the winning mass is reached display next level instruction
        if self.level_won == True:
            self.screen.blit(self.next_level_text,((self.win_width-self.next_level_text.get_width())/2, (self.win_height-self.next_level_text.get_height())/2))

    def create_level_info_text(self):

        # Create text object for displaying the level
        self.level_text = self.level_font.render('Level {}'.format(self.game_level), False, (84,84,84))

        # Create text object for instructions on moving to next level
        self.next_level_text = self.next_level_font.render("""Achieved Critical Mass! (Press Space Bar to Advance)""", False, (84,84,84))

    def game_loop(self, level):
        """ Runs the loop for the game"""
        print("Running Game Loop")

        # Set the parameters for the current game level
        self.set_level_parameters()

        # Create all the text objects needed for level info
        self.create_level_info_text()

        # Create the enemy
        self.enemies = self.setup.enemy_generator(self.enemy_specs)

        # Create sprite group of space rocks
        self.brown_rocks = self.setup.rock_generator(self.brown_space_rock_set, "Brown", 0)
        self.grey_rocks = self.setup.rock_generator(self.grey_space_rock_set, "Grey", 200)

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
                    elif event.key == K_SPACE and self.level_won == True:
                        self.game_level += 1
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

            # collision_handler
            self.collision_handler()

            # Blit the background
            self.screen.blit(self.bg_image,(0,0))

            # Display text and radar
            self.heads_up_display()

            # Update sprite positions
            self.update_sprite_positions()

            # Display the current level at start of level
            if self.level_text_count > 0:
                self.screen.blit(self.level_text,((self.win_width-self.level_text.get_width())/2, (self.win_height-self.level_text.get_height())/2))
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
                self.level_won = True

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
                    elif event.key == pygame.K_RETURN:
                        self.real_button.button_sound.play()
                        self.game_level = 1
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
