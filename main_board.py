################################################################################
## main board
################################################################################
""" draws main board """

################################################################################

import pygame
from pygame import Rect, Color
import draw_areas
from images_lib import Image_lib

################################################################################
    
def draw_background(screen, tile_img, field_rect):
    img_rect = tile_img.get_rect()
    
    nrows = int(screen.get_height() / img_rect.height) + 1
    ncols = int(screen.get_width() / img_rect.width) + 1
    
    for y in range(nrows):
        for x in range(ncols):
            img_rect.topleft = (x * img_rect.width, 
                                y * img_rect.height)
            screen.blit(tile_img, img_rect)
    
    field_color = (109, 41, 1)
    draw_areas.draw_rimmed_box(screen, field_rect, field_color, 4, Color('black'))    
    
################################################################################
## Test
################################################################################

if __name__ == "__main__": 
    
    pygame.init()
    import params
    screen = pygame.display.set_mode((params.SCREEN_WIDTH, params.SCREEN_HEIGHT), 0, 32)
    
    image_lib = Image_lib()
    battle_grid_img = image_lib.battle_grid_img
    msg1 = "testing"
    msg2 = "message"
    msg3 = "board"
    
    draw_background(screen, image_lib.battle_grid_img, params.FIELD_RECT) # Redraw the background
    
    print("Done")