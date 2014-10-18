#Max Line Length As according to PEP-0008 for docstrings/comments(72)##
#Max Line Length As according to PEP-0008 for everything else(79)#############
    
  
import pygame
import sys
from images_lib import (  GREEN, GRASS, BLACK, LT_GRAY )
from grid_map import (SCREEN_WIDTH, SCREEN_HEIGHT)
from grid_map import Grid_Map
     
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption("3-D Tile Array")  
icon = pygame.image.load("images/test_icon.jpg").convert_alpha() 
pygame.display.set_icon(icon)
done = False
clock = pygame.time.Clock()   
gridmap = Grid_Map(screen) #                                                
#for unit in gridmap.pawn_group.group_list:   
    #print("---------------------------- unit loc:", unit.loc)       
#gridmap.grid_unit_color_updater()   
while done == False: #                                                      
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done = True # Flag that we are done so we exit this loop
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # User clicks the mouse. Get the position
            pos = pygame.mouse.get_pos()
            gridmap.grid_clicked(pos)                
            # Check to see if click was in grid field for testing 
            if gridmap.in_field(pos):
                print("you hit the grid")
            elif not gridmap.in_field(pos):
                print("you missed the grid")
    screen.fill(BLACK) # Set the screen background
    gridmap.update_grid() # Re-Image the grid
    clock.tick(20) # Limit to 20 frames per second
    pygame.display.flip() # Go ahead and update the screen with what we've drawn.       
gridmap.print_grid()

pygame.quit()
sys.exit()   