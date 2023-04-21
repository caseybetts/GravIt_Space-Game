# This is a configuration file for SpaceRockGame.py

from math import ceil, floor

# Screen parameters
framerate = 35

# Sound
music_on = True
background_music_location = "audio/background_music.wav"
button_sound_location = "audio/button-gong-sabi.wav"
THRUST_SOUND_LOCATION = "audio/thrust.flac"
GULP_SOUND_LOCATION = "audio/gulp.mp3"

# Graphics
PLAYER_IMAGE_LOCATOIN = 'Graphics/GreenBlob.png'
button_image_location = 'Graphics/Blue_button2.png'
background_image_location = "Graphics/bg_stars5.jpg"
up_button_image_location = "Graphics/Up_Button.png"
down_button_image_location = "Graphics/Down_Button.png"
ENEMY_IMAGE_LOCATION = "Graphics/YellowBlob.png"

# Player parameters
PLAYER_START_MASS = 4e15 #kg
PLAYER_STARAT_SIZE = 25


# Enemy parameters
ENEMY_MASS = 1e15
ENEMY_PERCENT_EJECTION = .007
ENEMY_TOP_SPEED = 5
ENEMY_STEALING_AMMOUNT = 5e12
LEVEL_1_ENEMY_SPECS = [[0, 1e15, 40]] # quantity, mass, size
LEVEL_2_ENEMY_SPECS = [[0, 1e15, 20]] # quantity, mass, size
LEVEL_3_ENEMY_SPECS = [[1, 1e15, 20]] # quantity, mass, size
LEVEL_4_ENEMY_SPECS = [[2, 1e15, 20]] # quantity, mass, size
LEVEL_5_ENEMY_SPECS = [[5, 1e15, 20]] # quantity, mass, size
LEVEL_6_ENEMY_SPECS = [[2, 1e16, 40]] # quantity, mass, size

# Motion parameters
thrust_acc = 100000
collision_slow_percent = .99
grav_threshold = 20
BOUNCE_SLOW_PERCENT = .5

# Set how many screens the map consists of
MAP_SIZE_WIDTH = 7
MAP_SIZE_HEIGHT = 7

# Min and Max for the map rows and columns
MAP_MIN_COL = ceil(-MAP_SIZE_WIDTH/2)
MAP_MAX_COL = floor(MAP_SIZE_WIDTH/2)
MAP_MIN_ROW = ceil(-MAP_SIZE_HEIGHT/2)
MAP_MAX_ROW = floor(MAP_SIZE_HEIGHT/2)

print(MAP_MIN_COL, MAP_MAX_COL, MAP_MIN_ROW, MAP_MAX_ROW)

# Space Rock parameters
helper_force =  0
SMALL_MASS =    1e14
MED_MASS =      5e14
BIG_MASS =      1e15
HUGE_MASS =     1e16
MASSES = (SMALL_MASS, MED_MASS, BIG_MASS)
ROCK_START_VELOCITY = (0,2)
ROCK_LOWER_GAUSS_X = -3000
ROCK_UPPER_GAUSS_X = 4000
ROCK_LOWER_GAUSS_Y = -3000
ROCK_UPPER_GAUSS_Y = 4000

# Radar coords
RADAR_REDUCTION = .04

# Level parameters
LEVEL_1_BROWN_SET = [
                [ 0, "HUGE_MASS"],
                [50, "BIG_MASS"],
                [0, "MED_MASS"],
                [0, "SMALL_MASS"]]
LEVEL_1_GREY_SET = [
                [0, "BIG_MASS"],
                [ 0, "MED_MASS"],
                [ 0, "SMALL_MASS"]]

LEVEL_2_BROWN_SET = [
                [ 0, "HUGE_MASS"],
                [20, "BIG_MASS"],
                [10, "MED_MASS"],
                [10, "SMALL_MASS"]]
LEVEL_2_GREY_SET = [
                [10, "BIG_MASS"],
                [ 5, "MED_MASS"],
                [ 5, "SMALL_MASS"]]

LEVEL_3_BROWN_SET = [
                [ 2, "HUGE_MASS"],
                [20, "BIG_MASS"],
                [10, "MED_MASS"],
                [10, "SMALL_MASS"]]
LEVEL_3_GREY_SET = [
                [10, "BIG_MASS"],
                [ 5, "MED_MASS"],
                [ 5, "SMALL_MASS"]]

LEVEL_4_BROWN_SET = [
                [ 2, "HUGE_MASS"],
                [15, "BIG_MASS"],
                [7, "MED_MASS"],
                [10, "SMALL_MASS"]]
LEVEL_4_GREY_SET = [
                [10, "BIG_MASS"],
                [ 5, "MED_MASS"],
                [ 5, "SMALL_MASS"]]
LEVEL_5_BROWN_SET = [
                [ 2, "HUGE_MASS"],
                [10, "BIG_MASS"],
                [5, "MED_MASS"],
                [10, "SMALL_MASS"]]
LEVEL_5_GREY_SET = [
                [10, "BIG_MASS"],
                [ 5, "MED_MASS"],
                [ 5, "SMALL_MASS"]]
LEVEL_6_BROWN_SET = [
                [ 3, "HUGE_MASS"],
                [5, "BIG_MASS"],
                [5, "MED_MASS"],
                [5, "SMALL_MASS"]]
LEVEL_6_GREY_SET = [
                [5, "BIG_MASS"],
                [ 5, "MED_MASS"],
                [ 5, "SMALL_MASS"]]
