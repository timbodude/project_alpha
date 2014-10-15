import pygame
from pygame.locals import *
from grid_map import Grid_map
import params
from images_lib import (  BLACK  )

################################################################################

def main():
    # Initialise screen
    pygame.init()
    clock = pygame.time.Clock()
    #screen = pygame.display.set_mode((800, 600))
    screen = pygame.display.set_mode((params.SCREEN_WIDTH, params.SCREEN_HEIGHT), 0, 32)
    
    pygame.display.set_caption('Project Alpha')
    #icon = pygame.image.load("test_icon.jpg").convert_alpha()        
    #pygame.display.set_icon(icon)   
    
    # Access Grid Class to create a grid:
    grid_map = Grid_map(screen)

    # Fill background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 0, 0))

    # Display some text
    #spriteSheet = pygame.image.load("terminal12x12_gs_ro.png")
    #background.blit(spriteSheet, spriteSheet.get_rect())

    ## Blit everything to the screen
    #screen.blit(background, (0, 0))
    #pygame.display.flip()

    # Event loop
    while 1:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN: # User clicks the mouse. Get the position
                pos = pygame.mouse.get_pos()
                grid_map.grid_clicked(pos)
                #if grid_map.in_field(pos): # Check to see if click was in grid field for testing 
                    #print("you hit the grid")
                #elif not grid_map.in_field(pos):
                    #print("you missed the grid")       
                    
        screen.fill(BLACK) # Set the screen background
        grid_map.update_grid() # Update the grid
        clock.tick(20) # Limit to 20 frames per second
        pygame.display.flip() # Go ahead and update the screen with what we've drawn     

        #screen.blit(background, (0, 0))
        #pygame.display.flip()


if __name__ == '__main__': main()
