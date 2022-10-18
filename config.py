# This is a configuration file for SpaceRockGame.py

# Screen parameters
framerate = 35

# Sound
music_on = True
background_music_location = "audio/background_music.wav"
button_sound_location = "audio/button-gong-sabi.wav"
thrust_sound_location = "audio/thrust.flac"
gulp_sound_location = "audio/gulp.mp3"

# Graphics
button_image_location = 'Graphics/Blue_button2.png'
background_image_location = "Graphics/bg_stars5.jpg"
up_button_image_location = "Graphics/Up_Button.png"
down_button_image_location = "Graphics/Down_Button.png"

# Player parameters
PLAYER_START_MASS = 4e15 #kg
player_start_size_x = 20
player_start_size_y = 20

# Motion parameters
thrust_acc = 100000
collision_slow_percent = .99
grav_threshold = 20
BOUNCE_SLOW_PERCENT = .5


# Space Rock parameters
helper_force =  5000
SMALL_MASS =    1e14
MED_MASS =      5e14
BIG_MASS =      1e15
HUGE_MASS =     1e16
MASSES = (SMALL_MASS, MED_MASS, BIG_MASS)
ROCK_START_VELOCITY = (0,2)

# Set how many screens the map consists of
map_size_width = 7
map_size_height = 7

# Radar coords
RADAR_REDUCTION = .04

# Level parameters
LEVEL_1_BROWN_SET = [
                ["HUGE_MASS",1],
                ["BIG_MASS",10],
                ["MED_MASS",10],
                ["SMALL_MASS",10]]
LEVEL_1_GREY_SET = [
                ["BIG_MASS",3],
                ["MED_MASS",50],
                ["SMALL_MASS",9]]

LEVEL_2_BROWN_SET = [
                ["BIG_MASS",10],
                ["MED_MASS",10],
                ["SMALL_MASS",20]]
LEVEL_2_GREY_SET = [
                ["HUGE_MASS", 1],
                ["BIG_MASS",5],
                ["MED_MASS",10],
                ["SMALL_MASS",20]]

LEVEL_3_BROWN_SET = [
                ["HUGE_MASS", 1],
                ["BIG_MASS",5],
                ["MED_MASS",10],
                ["SMALL_MASS",20]]
LEVEL_3_GREY_SET = [
                ["BIG_MASS",5],
                ["MED_MASS",10],
                ["SMALL_MASS",20]]
RADAR_REDUCTION
