import pygame, os
from pygame.locals import *
from grid import Tile_grid
import params, player_command
from images_lib import (  BLACK, WHITE,  DARKGRAY, GRAY, LIGHTGRAY )
from unit_simp import P_u_group
import pygbutton

################################################################################

# Get things started
screen = pygame.display.set_mode((params.SCREEN_WIDTH, params.SCREEN_HEIGHT), 0, 32) # create screen area for tiles
grid_map = Tile_grid(screen) # Create a grid of tiles
player_command = player_command.Player_command()
players = P_u_group(screen) 

# try a pygbutton
#button_1 = PygButton.PygButton(rect=None, caption='', bgcolor=LIGHTGRAY, fgcolor=BLACK, font=None, normal=None, down=None, highlight=None)
button_1 = pygbutton.PygButton(rect=(700,170,75,20), caption='btn_1', bgcolor=LIGHTGRAY, fgcolor=BLACK, font=None, normal=None, down=None, highlight=None)

################################################################################

def usr_events(pos):
    """ determine action based upon mouse & kbd input 
        pos: mouse position coordinates
    """
    if grid_map.in_field(pos): # Check to see if click was in grid field for testing 
        #print("you hit the battle grid area")
        #print("you're clicked on:", pos)
        grid_map.grid_clicked(pos) # do whatever happens when something gets clicked on
 
def update_all():
    """ update everything & put on screen """
    screen.fill(BLACK) # Set the screen background
    grid_map.update_grid() # Update the grid to screen
    player_command.draw_messageboard(screen) # update player_command area
    players.update_players(player_command) # Update player groups & units to screen    
    button_1._update()
    button_1.draw(screen)
        
################################################################################

def main():
    # Initialise screen
    pygame.init()
    clock = pygame.time.Clock()
    pygame.display.set_caption('Project Alpha')
    #icon = pygame.image.load("test_icon.jpg").convert_alpha()        
    #pygame.display.set_icon(icon)  
    # Fill background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 0, 0))
    
    ttl_round = 0 # total rounds played
    turn = 0 # who's turn it is    
    
    # Event loop
    while 1:
        for event in pygame.event.get():
            if event.type == QUIT:
                grid_map.print_test_grid()  # print test grid to shell              
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN: # User clicks the mouse. Get the position
                usr_events(pygame.mouse.get_pos())
            if "click" in button_1.handleEvent(event):
                print("Hey, I was clicked")
                    
        update_all()            

        clock.tick(20) # Limit to 20 frames per second
        pygame.display.flip() # Go ahead and update the screen with what we've set to be drawn     

if __name__ == '__main__': main()