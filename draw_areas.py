################################################################################
## draw_areas
################################################################################

import pygame
from pygame import Rect, Color
from images_lib import Image_lib

################################################################################


def draw_rimmed_box(screen, box_rect, box_color, 
                    rim_width=0, 
                    rim_color=Color('black')):
    """ Draw a rimmed box on the given surface. The rim is drawn outside the box rect. """
    if rim_width:
        rim_rect = Rect(box_rect.left - rim_width,
                        box_rect.top - rim_width,
                        box_rect.width + rim_width * 2,
                        box_rect.height + rim_width * 2)
        pygame.draw.rect(screen, rim_color, rim_rect)
    
    pygame.draw.rect(screen, box_color, box_rect)




################################################################################
## test
################################################################################

if __name__ == "__main__": 
    
    pygame.init()
    import params    
    
    screen = pygame.display.set_mode((params.SCREEN_WIDTH, params.SCREEN_HEIGHT), 0, 32)
    
    
    image_lib = Image_lib()
    
    print("Done")