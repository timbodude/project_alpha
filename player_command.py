################################################################################
## player_command
################################################################################
""" Controls display area for player input/output """

################################################################################
import pygame
from pygame import Rect, Color
from images_lib import Image_lib
import messages

################################################################################

class Player_command(object):
    """ Display pannel for player input/output """
    
    def __init__(self):
        self.msg1 = "text area 1"
        self.msg2 = "text area 2"
        self.msg3 = "text area 3"
        self.x = 50
        self.width = 20
        self.offset = 0
        self.back_color = "black"
        self.message_rect = Rect(600, 0, 800, 600)
        self.message_size = (int(self.message_rect[2])-self.message_rect[0], int(self.message_rect[3]))
        
    def draw_messageboard(self, screen):
        self.draw_rimmed_box(screen, self.message_rect, (self.x, self.width, self.offset), 4, Color(self.back_color))
        my_font = pygame.font.SysFont('arial', 18)
        message1_sf = my_font.render(self.msg1, True, Color('white'))
        message2_sf = my_font.render(self.msg2, True, Color('white'))
        message3_sf = my_font.render(self.msg3, True, Color('white'))
        message4 = "Heroes: " + str(messages.HERO_WINS)
        message4_sf = my_font.render(message4, True, Color('white'))
        message5 = "Enemies: " + str(messages.ENEMY_WINS)  
        message5_sf = my_font.render(message5, True, Color('white'))
        
        screen.blit(message1_sf, self.message_rect.move(0, message1_sf.get_height()))
        screen.blit(message2_sf, self.message_rect.move(0, message2_sf.get_height()*2))  
        screen.blit(message3_sf, self.message_rect.move(0, message2_sf.get_height()*3))  
        screen.blit(message4_sf, self.message_rect.move(0, message4_sf.get_height()*4))  
        screen.blit(message5_sf, self.message_rect.move(0, message5_sf.get_height()*5))  
        
    def draw_rimmed_box(self, screen, box_rect, box_color, 
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
   
    def in_field(self, pos):
        """ verify if clicked pos is in playable grid area  - returns True/False """
        loc = self.coord_to_grid(pos)
        if loc[0] < 0 or loc[0] >= self.x or loc[1] < 0 or loc[1] >= params.GRID_SIZE[1]:
            #print("you missed the player_command grid")
            return(False)
        else:
            return(True)
    
    def grid_clicked(self, pos):
        """ tells what grid was clicked on and reports for testing purposes 
            pos: the passed mouse coordinates variable passed through 
        """
        if self.in_field(pos):
            #print("click is in player_command field")
            #print("pos clicked:", pos)
            dummy = False
            
################################################################################
## Unit Testing                                                               ##
################################################################################
if __name__ == "__main__":  
    player_command = Player_command()