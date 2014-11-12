import pygame
#from grid_map import Grid_map
from grid import Tile_grid

################################################################################
## usr_events
################################################################################


class Usr_events(object):

    def __init__(self, screen):
        """ screen: screen  """
        self.screen = screen
        
    def do_usr_input(self, pos):
        """ determine action based upon mouse & kbd input 
            pos: mouse position coordinates
        """
        dummy = False
        #print("usr_events is connected.") # - works
        #if grid_map.in_field(pos): # Check to see if click was in grid field for testing 
            #grid_map.grid_clicked(pos)
        if grid.in_field(pos): # Check to see if click was in grid field for testing 
            grid.grid_clicked(pos)            