# pawn 0.5


# Startups
import pygame, sys
from pygame.locals import *

clock = pygame.time.Clock()
pygame.init()

from pawn_units import *

# Globals
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
BATTLE_AREA = [600,350]
START_SIZ = 20
START_LOC = [50,50]
GAME_SPEED = .02


# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 128)
RED = (255, 30, 56)
DRK_RED = (128, 0, 0)
COMMAND_GRAY = (80, 100, 100)
BLACK = (0, 0, 0)


# Constants
# aids_names = ["Attack", "Initiative", "Defense", "Speed"] # (relocated to pawn_groups)



# Set Screen
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pawn Arena!")


class Game():  
    """ Game methods """
    def __init__(self):
        self.done = False
        
    def event(self):
        # oversees event handlers
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # If user clicked close
                self.end()
            elif event.type == pygame.KEYDOWN:
                self.user_keydown(event.key)
            elif event.type == pygame.KEYUP:
                self.user_keyup(event.key) 
                
    def end(self):
        self.done = True # Flag that we are done so we exit this loop
        pygame.quit()
        sys.exit()    
            
    def user_keydown(self,user_in):
        # handle user keydown and translate into stop action
        dummy = False     
    
    def user_keyup(self,user_in):
        # handle user keyup and translate into stop action
        dummy = False   
        
    def control_display(self):
        """ set-up control area """
        pygame.draw.rect(DISPLAYSURF, COMMAND_GRAY, [0,BATTLE_AREA[1]+1,SCREEN_WIDTH,50], 0)     
        
def draw_rimmed_box(screen, box_rect, box_color, rim_width=0, rim_color=Color('black')):
            """ Draw a rimmed box on the given surface. The rim is drawn
                outside the box rect.
            """        
            
def post_clock(time_count):
    d_min = int(time_count/50/60)
    d_sec = int(time_count/50 %60)
    if d_sec > 59:
        d_sec = 0
    dt_min = str(d_min)
    dt_sec = str(d_sec)
    if len(dt_sec) < 2:
        dt_sec = "0" + dt_sec
    return("clock: " + dt_min + ":" + dt_sec)      

def draw_background(screen, tile_img, field_rect):
    img_rect = tile_img.get_rect()
    nrows = int(screen.get_height() / img_rect.height) + 1
    ncols = int(screen.get_width() / img_rect.width) + 1
    
    for y in range(nrows):
        for x in range(ncols):
            img_rect.topleft = (x * img_rect.width, y * img_rect.height)
            screen.blit(tile_img, img_rect)
    
    field_color = (109, 41, 1)
    draw_rimmed_box(screen, field_rect, field_color, 4, Color("BLACK"))
    
def draw_messageboard(screen, rect, message1, message2, message3):
    draw_rimmed_box(screen, rect, (50, 20, 0), 4, Color("BLACK"))
    
    my_font = pygame.font.SysFont('arial', 20)
    message1_sf = my_font.render(message1, True, Color('white'))
    message2_sf = my_font.render(message2, True, Color('white'))
    message3_sf = my_font.render(message3, True, Color('white'))
    
    screen.blit(message3_sf, rect)
    screen.blit(message1_sf, rect.move(0, message1_sf.get_height()))
    screen.blit(message2_sf, rect.move(0, message2_sf.get_height()*2))

# GAME BEGINS ------------------------------------------------------------------
pygame.init()
game = Game()

FIELD_RECT = Rect(50, 50, 300, 300)
MESSAGE_RECT = Rect(360, 50, 130, 75)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
BG_TILE_IMG = 'images/brick_tile.png'
bg_tile_img = pygame.image.load(BG_TILE_IMG).convert_alpha()
win_test = False
time_count = 0

# PRE_GAME TESTS ---------------------------------------------------------------
pawn_group = Pawn_group() # make a pawn group for testing purposes
pawn_group.make_group(5)





while True: # main game loop
    DISPLAYSURF.fill(WHITE)
    # Add command area
    draw_background(screen, bg_tile_img, FIELD_RECT)    
    game.control_display() # draw master control area
    #DISPLAYSURF.blit(textSurfaceObj, textRectObj)
    game.event()
    done = game.done # check for end-of-loop-flag
                



    # IN-GAME ------------------------------------------------------------------
    


    # WRAP UP GAME LOOP --------------------------------------------------------
    msg1 = "Pawns: "
    msg2 = "You won!" if win_test == True else " "
    msg3 = post_clock(time_count)
    draw_messageboard(screen, MESSAGE_RECT, msg1, msg2, msg3)    
    pygame.display.update()
    pawn_group.draw_group()
    
    # set game speed
    clock.tick(50)
    time_count += 1