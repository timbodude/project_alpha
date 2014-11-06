################################################################################
## grid
################################################################################

import pygame
from random import choice
import params

################################################################################



################################################################################

class Tile(object):
    """ - terrain class of sprite objects to populate grid 
        - created by Tile_grid group object 
        - eventually add additional terrain types
    """
    def __init__(self):
        self.terrain_type = "grass"
        self.selected = False
        self.contents = ()
        self.passable = True
        self.altitude = 3 # 0: lowest 3: sealevel 6: highest
        self.movement_cost = 2
        
        #print("i made a tile")
        
               
class Tile_grid(object):
    """ class for constructing gamespace of tiles terrain in a 2d grid """
    def __init__(self, screen):
        """ screen: screen window for display
        """
        self.nrows = int(params.FIELD_RECT[2]/params.TILE_SIZE) # number of horizontal grid spaces in grid map
        self.ncols = int(params.FIELD_RECT[3]/params.TILE_SIZE) # number of vertical grid spaces in grid map
        self.matrix = [[0 for i in range(self.ncols)] for i in range(self.nrows)]
        self.screen = screen
        
        self.fill_grid() # fill matrix with individual tiles
            
        #print("I made a tile grid")
        
        
        
    def fill_grid(self): 
        """ fill up space in grid with an individual tile """
        for row in range(0, self.nrows):
            for col in range(0, self.ncols):
                self.matrix[row][col] = Tile()            
                
    def print_grid(self):
        """ outputs visual version of grid to shell """
        print("printing the grid")
        for row in range(0, self.nrows):
            col_output = ""
            for col in range(0, self.ncols):
                occupant = self.matrix[row][col]
                if occupant.contents != ():
                    col_output += " u"
                elif not occupant.contents and occupant.terrain_type == "water":
                    col_output += " -"
                else: #default is grass
                    col_output += " g"
            print(col_output)
            print()
            

            
    def is_adjacent(self,new_coord):
        if new_coord[0] < self.coord[0] - 1 or new_coord[0] > self.coord[0] + 1 or new_coord[1] < self.coord[1] - 1 or new_coord[1] > self.coord[1] + 1:
            print("not adjacent")
            return(False)
        elif new_coord  == self.coord:
            print("already there")
            return(False)
        else:
            return(True)
        
################################################################################
## TEST
################################################################################
if __name__ == "__main__":  
    pygame.init()
    
    
    tile_grid = Tile_grid("screen")
    tile_grid.print_grid()
    print("grid printed")
    print()
    
    # TEST to see if units superscede terrain ##################################
    
    occupant = tile_grid.matrix[2][2]
    occupant.contents = "unit"
    tile_grid.matrix[2][2] = occupant
    print("there should be a unit at: 2,2")
    tile_grid.print_grid()
    
    
    
    print("--DONE--")  