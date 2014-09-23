################################################################################
## message board
################################################################################

import pygame
from pygame import Rect, Color
import draw_areas
from images_lib import Image_lib
import messages

################################################################################

def draw_messageboard(screen, rect, message1, message2, message3):
    draw_areas.draw_rimmed_box(screen, rect, (50, 20, 0), 4, Color('black'))
    
    my_font = pygame.font.SysFont('arial', 18)
    message1_sf = my_font.render(message1, True, Color('white'))
    message2_sf = my_font.render(message2, True, Color('white'))
    message3_sf = my_font.render(message3, True, Color('white'))
    message4 = "Heroes: " + str(messages.HERO_WINS)
    message4_sf = my_font.render(message4, True, Color('white'))
    message5 = "Enemies: " + str(messages.ENEMY_WINS)  
    message5_sf = my_font.render(message5, True, Color('white'))
    
    screen.blit(message3_sf, rect)
    screen.blit(message1_sf, rect.move(0, message1_sf.get_height()))
    screen.blit(message2_sf, rect.move(0, message2_sf.get_height()*2))  
    screen.blit(message4_sf, rect.move(0, message4_sf.get_height()*3))  
    screen.blit(message5_sf, rect.move(0, message5_sf.get_height()*4))  
    


################################################################################
## Test
################################################################################

if __name__ == "__main__": 
    
    pygame.init()
    
    import params
    
    screen = pygame.display.set_mode((params.SCREEN_WIDTH, params.SCREEN_HEIGHT), 0, 32)
    
    image_lib = Image_lib()
    msg1 = "testing"
    msg2 = "message"
    msg3 = "board"
    draw_messageboard(screen, params.MESSAGE_RECT, msg1, msg2, msg3)
    
    print("Done")