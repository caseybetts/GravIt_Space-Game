# This is a configuration file for SpaceRockGame.py

# Screen parameters
framerate = 35

# Sound
music_on = False
background_music_location = "audio/background_music.wav"
button_sound_location = "audio/button-gong-sabi.wav"
thrust_sound_location = "audio/thrust.flac"
gulp_sound_location = "audio/gulp.mp3"

# Graphics
button_image_location = 'Graphics/Blue_button2.png'
background_image_location = "Graphics/bg_stars5.jpg"
up_button_image_location = "Graphics/Up_Button.png"
down_button_image_location = "Graphics/Down_Button.png"
enemy_image_location = "Graphics/YellowBlob.png"

# Player parameters
PLAYER_START_MASS = 4e15 #kg
player_start_size_x = 25
player_start_size_y = 25

# Enemy parameters
ENEMY_MASS = 1e15
ENEMY_PERCENT_EJECTION = .007
ENEMY_TOP_SPEED = 5
ENEMY_STEALING_AMMOUNT = 5e12
LEVEL_1_ENEMY_SPECS = [[10, 1e15, 40]] # quantity, mass, size
LEVEL_2_ENEMY_SPECS = [[2, 1e15, 20]] # quantity, mass, size
LEVEL_3_ENEMY_SPECS = [[1, 1e15, 20]] # quantity, mass, size

# Motion parameters
thrust_acc = 100000
collision_slow_percent = .99
grav_threshold = 20
BOUNCE_SLOW_PERCENT = .5


# Space Rock parameters
helper_force =  0
SMALL_MASS =    1e14
MED_MASS =      5e14
BIG_MASS =      1e15
HUGE_MASS =     1e16
MASSES = (SMALL_MASS, MED_MASS, BIG_MASS)
ROCK_START_VELOCITY = (0,2)
ROCK_LOWER_GAUSS_X = -1000
ROCK_UPPER_GAUSS_X = 2000
ROCK_LOWER_GAUSS_Y = -1000
ROCK_UPPER_GAUSS_Y = 1000

# Set how many screens the map consists of
map_size_width = 7
map_size_height = 7

# Radar coords
RADAR_REDUCTION = .04

# Level parameters
LEVEL_1_BROWN_SET = [
                [ 0, "HUGE_MASS"],
                [10, "BIG_MASS"],
                [10, "MED_MASS"],
                [10, "SMALL_MASS"]]
LEVEL_1_GREY_SET = [
                [10, "BIG_MASS"],
                [ 5, "MED_MASS"],
                [ 5, "SMALL_MASS"]]

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
                [ 0, "HUGE_MASS"],
                [20, "BIG_MASS"],
                [10, "MED_MASS"],
                [10, "SMALL_MASS"]]
LEVEL_3_GREY_SET = [
                [10, "BIG_MASS"],
                [ 5, "MED_MASS"],
                [ 5, "SMALL_MASS"]]
