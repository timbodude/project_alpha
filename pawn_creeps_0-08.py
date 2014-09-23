import os, sys
from random import randint, choice
from math import sin, cos, radians

import pygame
from pygame import Rect, Color
from pygame.sprite import Sprite

from vec2d import vec2d
from simpleanimation import SimpleAnimation

# ------------------------------------------------------------------------------                
# Libraries, Lists, & Globals

# ------------------------------------------------------------------------------                
# Unit Classes

        
# ------------------------------------------------------------------------------
# Game Setup Classes

# ------------------------------------------------------------------------------
# Run Game Classes

  

# ------------------------------------------------------------------------------
# Set up stuff for game

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

def draw_messageboard(screen, rect, message1, message2, message3):
    draw_rimmed_box(screen, rect, (50, 20, 0), 4, Color('black'))
    
    my_font = pygame.font.SysFont('arial', 20)
    message1_sf = my_font.render(message1, True, Color('white'))
    message2_sf = my_font.render(message2, True, Color('white'))
    message3_sf = my_font.render(message3, True, Color('white'))
    
    screen.blit(message3_sf, rect)
    screen.blit(message1_sf, rect.move(0, message1_sf.get_height()))
    screen.blit(message2_sf, rect.move(0, message2_sf.get_height()*2))

def draw_rimmed_box(screen, box_rect, box_color, 
                    rim_width=0, 
                    rim_color=Color('black')):
    """ Draw a rimmed box on the given surface. 
        The rim is drawn outside the box rect.
    """
    if rim_width:
        rim_rect = Rect(box_rect.left - rim_width,
                        box_rect.top - rim_width,
                        box_rect.width + rim_width * 2,
                        box_rect.height + rim_width * 2)
        pygame.draw.rect(screen, rim_color, rim_rect)
    
    pygame.draw.rect(screen, box_color, box_rect)
    

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
    draw_rimmed_box(screen, field_rect, field_color, 4, Color('black'))

# ------------------------------------------------------------------------------        

def run_game():
    
    # Game parameters
    SCREEN_WIDTH, SCREEN_HEIGHT = 500, 400
    FIELD_RECT = Rect(50, 50, 300, 300)
    MESSAGE_RECT = Rect(360, 50, 130, 200)
    BG_TILE_IMG = 'images/brick_tile.png'
    time_count = 0
    
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
    clock = pygame.time.Clock()
    paused = False
    won = False

    bg_tile_img = pygame.image.load(BG_TILE_IMG).convert_alpha()

# ------------------------------------------------------------------------------        
# The main game loop

    while True:
        time_passed = clock.tick(50) # Limit frame speed to 50 FPS
        
        #if paused == False and len(creeps) != 0:
        if paused == False:    
            time_count += 1
        #~ time_passed = clock.tick()
        #~ print time_passed
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused
            elif (  event.type == pygame.MOUSEBUTTONDOWN and
                    pygame.mouse.get_pressed()[0] and
                    paused != True):
                for creep in creeps:
                    creep.mouse_click_event(pygame.mouse.get_pos())
                for pawn in pawns:
                    pawn.mouse_click_event(pygame.mouse.get_pos())                    
                    
        
        if not paused:
            # Redraw the background
            draw_background(screen, bg_tile_img, FIELD_RECT)
            
            #msg1 = 'Creeps: %d' % len(creeps)
            msg1 = "Creeps: "
            #msg2 = 'You won!' if len(creeps) == 0 else ''
            msg2 = 'You won!' if won == True else ''
            msg3 = post_clock(time_count)
            draw_messageboard(screen, MESSAGE_RECT, msg1, msg2, msg3)
            
            # Update and redraw all units


        pygame.display.flip()


def exit_game():
    pygame.quit()
    sys.exit()


run_game()

