# This file contains the RadarPoint class

import pygame
from config import *
from Calculations import radar_coord_conversion

class RadarPoint(pygame.sprite.Sprite):
    """This is a point on the radar that reflects the location of a space rock"""

    def __init__(self, id):
        super(RadarPoint, self).__init__()
        self.id = id

        # Create pygame Surface
        self.surface = pygame.Surface((2,2))
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

    def display(self, screen, screen_col, screen_row, win_width, win_height):

        # Blit the radar point to the screen
        screen.blit(self.surface,[
                        self.rect.left,
                        self.rect.top])

    def update(self, rocks, player_rect, radar_rect, map_rect, screen, screen_col, screen_row, win_width, win_height):
        # If the point is the player
        if self.id == 0:
            player_coords = radar_coord_conversion(
                                player_rect.left,
                                player_rect.top,
                                radar_reduction,
                                radar_rect,
                                map_rect
                                )
            self.rect[0] = player_coords[0]
            self.rect[1] = player_coords[1]

            self.display(screen, screen_col, screen_row, win_width, win_height)
        else:
            # Find the space rock with the same id and change position to match
            alive = False
            for rock in rocks:
                if self.id == rock.id:
                    alive = True
                    rock_coords = radar_coord_conversion(
                                    rock.rect.left,
                                    rock.rect.top,
                                    radar_reduction,
                                    radar_rect,
                                    map_rect
                                    )
                    self.rect[0] = rock_coords[0]
                    self.rect[1] = rock_coords[1]

                    self.display(screen, screen_col, screen_row, win_width, win_height)

            # If the alive flag does not get put to True then a rock was not found, kill the point
            if not alive: self.kill()
