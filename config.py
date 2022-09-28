# This is a configuration file for SpaceRockGame.py

# Screen parameters
framerate = 35
winHeight = 1000
winWidth =  1600

# Sound
music_on = False

# Graphics
button_image_location = 'Graphics/Blue_button.png'

# Player parameters
player_start_mass = 4e15 #kg
player_start_pos_x = winWidth/5
player_start_pos_y = winHeight/2
player_start_velocity_x = -2
player_start_velocity_y = 0
player_start_size_x = 20
player_start_size_y = 20

# Motion parameters
thrust_acc = 1000000
percent_ejection = .001
collision_slow_percent = .99
grav_threshold = 20

# Space Rock parameters
number_of_rocks = 1
helper_force =  5000
small_rock =    500000
med_rock =      50000000000000
big_rock =      100000000000000
MASSES = (small_rock, med_rock, big_rock)
rock_start_velocity = (0,500)

# Map Boudaries
outer_left = -3*winWidth
outer_right = 4*winWidth
outer_top = -3*winHeight
outer_bottom = 4*winHeight
map_width = outer_right-outer_left
map_height = outer_bottom-outer_top

# Radar coords
radar_reduction = .04
radar_left = winWidth-20-(map_width*radar_reduction)
radar_top = winHeight-20-(map_height*radar_reduction)
