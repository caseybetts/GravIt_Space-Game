# This is a configuration file for SpaceRockGame.py

# Screen parameters
framerate = 35

# Sound
music_on = True
background_music_location = "audio/background_music.wav"
button_sound_location = "audio/button-gong-sabi.wav"
thrust_sound_location = "audio/thrust.flac"

# Graphics
button_image_location = 'Graphics/Blue_button2.png'
background_image_location = "Graphics/bg_stars5.jpg"
up_button_image_location = "Graphics/Up_Button.png"
down_button_image_location = "Graphics/Down_Button.png"
# Player parameters
player_start_mass = 4e15 #kg
player_start_size_x = 20
player_start_size_y = 20

# Motion parameters
thrust_acc = 100000
collision_slow_percent = .99
grav_threshold = 20

# Space Rock parameters
helper_force =  5000
small_rock =    1e14
med_rock =      5e14
big_rock =      1e15
MASSES = (small_rock, med_rock, big_rock)
rock_start_velocity = (0,2)

# Set how many screens the map consists of
map_size_width = 7
map_size_height = 7

# Radar coords
radar_reduction = .04
