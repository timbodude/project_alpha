################################################################################
## player_command
################################################################################

import pygame
from pygame import Rect, Color
from images_lib import Image_lib
import messages

################################################################################

msg1 = "text area 1"
msg2 = "text area 2"
msg3 = "text area 3"

def draw_messageboard(screen, rect, message1 = msg1, message2 = msg2, message3 = msg3):
    draw_rimmed_box(screen, rect, (50, 20, 0), 4, Color('black'))
    my_font = pygame.font.SysFont('arial', 18)
    message1_sf = my_font.render(message1, True, Color('white'))
    message2_sf = my_font.render(message2, True, Color('white'))
    message3_sf = my_font.render(message3, True, Color('white'))
    message4 = "Heroes: " + str(messages.HERO_WINS)
    message4_sf = my_font.render(message4, True, Color('white'))
    message5 = "Enemies: " + str(messages.ENEMY_WINS)  
    message5_sf = my_font.render(message5, True, Color('white'))
    
    screen.blit(message1_sf, rect.move(0, message1_sf.get_height()))
    screen.blit(message2_sf, rect.move(0, message2_sf.get_height()*2))  
    #screen.blit(message3_sf, rect)  
    screen.blit(message3_sf, rect.move(0, message2_sf.get_height()*3))  
    screen.blit(message4_sf, rect.move(0, message4_sf.get_height()*4))  
    screen.blit(message5_sf, rect.move(0, message5_sf.get_height()*5))  
    
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