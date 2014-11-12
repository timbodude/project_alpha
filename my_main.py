import pygame
from pygame.locals import *
from grid import Tile_grid
import params
from images_lib import (  BLACK  )
from unit_simp import P_u_group

################################################################################

screen = pygame.display.set_mode((params.SCREEN_WIDTH, params.SCREEN_HEIGHT), 0, 32) # create screen area for tiles
grid_map = Tile_grid(screen) # Create a grid of tiles
players = P_u_group(screen)



################################################################################
def usr_events(pos):
    """ determine action based upon mouse & kbd input 
        pos: mouse position coordinates
    """
    if grid_map.in_field(pos): # Check to see if click was in grid field for testing 
        #print("you hit the battle grid area")
        #print("you're clicked on:", pos)
        grid_map.grid_clicked(pos) # do whatever happens when something gets clicked on
################################################################################

def main():
    # Initialise screen
    pygame.init()
    clock = pygame.time.Clock()
    #screen = pygame.display.set_mode((800, 600))
    #screen = pygame.display.set_mode((params.SCREEN_WIDTH, params.SCREEN_HEIGHT), 0, 32)
    ttl_round = 0 # total rounds played
    turn = 0 # who's turn it is
    
    
    pygame.display.set_caption('Project Alpha')
    #icon = pygame.image.load("test_icon.jpg").convert_alpha()        
    #pygame.display.set_icon(icon)  
    
    #grid_map = Grid_map(screen) # Access Grid Class to create a grid

    # Fill background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 0, 0))

    #Display some text
    #spriteSheet = pygame.image.load("terminal12x12_gs_ro.png")
    #background.blit(spriteSheet, spriteSheet.get_rect())

    ## Blit everything to the screen
    #screen.blit(background, (0, 0))
    #pygame.display.flip()

    # Event loop
    while 1:
        for event in pygame.event.get():
            if event.type == QUIT:
                grid_map.print_test_grid()  # print test grid to shell              
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN: # User clicks the mouse. Get the position
                #print("you clicked")
                usr_events(pygame.mouse.get_pos())
                    
        screen.fill(BLACK) # Set the screen background
        grid_map.update_grid() # Update the grid to screen
        players.update_players() # Update player groups & units to screen
        
        clock.tick(20) # Limit to 20 frames per second
        pygame.display.flip() # Go ahead and update the screen with what we've set to be drawn     

        #screen.blit(background, (0, 0))
        #pygame.display.flip()


if __name__ == '__main__': main()
