################################################################################
## grid 
################################################################################

import pygame
from random import choice
import params
from images_lib import (  GREEN, MDW_GREEN )
import unit_simp

################################################################################



################################################################################

class Tile(object):
    """ - terrain class of sprite objects to populate grid 
        - created by Tile_grid group object 
        - eventually add additional terrain types
    """
    def __init__(self):
        self.terrain_type = "grass"
        self.color = MDW_GREEN
        self.alt_color = GREEN
        self.selected = False
        self.contents = ()
        self.passable = True
        self.altitude = 3 # 0: lowest 3: sealevel 6: highest
        self.movement_cost = 2
        #self.image = ________ # whatever image we want to assing - can be unique to incorporate drops or damage or whatever rather than a standard tile
        
class Tile_grid(object):
    """ class for constructing gamespace of tiles terrain in a 2d grid """
    def __init__(self, screen):
        """ screen: screen window for display
        """
        self.nrows = int(params.FIELD_RECT[2]/params.TILE_SIZE) # number of horizontal grid spaces in grid map
        self.ncols = int(params.FIELD_RECT[3]/params.TILE_SIZE) # number of vertical grid spaces in grid map
        self.matrix = [[0 for i in range(self.ncols)] for i in range(self.nrows)] # 2-d array of tiles
        self.screen = screen
        self.last_clicked =(-1,-1)# coord for last tile clicked 
        self.fill_grid() # fill matrix with individual tiles
        self.pawn_group = unit_simp.Simp_unit_group(screen) # adds group of units from unit_simp
        
    def fill_grid(self): 
        """ fill up space in grid with an individual tile """
        for row in range(0, self.nrows):
            for col in range(0, self.ncols):
                self.matrix[row][col] = Tile()            
        
    def update_grid(self): # primary grid update method
        self.update_unit_pos()
        for row in range(self.nrows):
            for col in range(self.ncols):    
                if self.matrix[row][col].selected == False: #check to see if tile is active or not to determine color and assign to curser_color
                    curser_color = self.matrix[row][col].color
                else: 
                    curser_color = self.matrix[row][col].alt_color
                #print("selected, curser color:", self.matrix[row][col].selected, curser_color)
                pygame.draw.rect(  self.screen,
                                   curser_color,
                                   [(params.FIELD_RECT[0] + row * (params.TILE_SIZE + params.MARGIN)),
                                    (params.FIELD_RECT[1] + col * (params.TILE_SIZE + params.MARGIN)),
                                    params.TILE_SIZE,
                                    params.TILE_SIZE] )
        
    def update_unit_pos(self): # adjust unit positions                          - possibly best to shift to update in unit class
        dummy = False
        
    #### Grid Helper Utilities   
    
    def coord_to_grid(self, pos):
        """ returns grid location based on sprite pos(x,y) for test purposes of clicked location """
        coord = (  int((pos[0] - params.FIELD_RECT[0]) / (params.TILE_SIZE + params.MARGIN)),
                           int((pos[1] - params.FIELD_RECT[1]) / (params.TILE_SIZE + params.MARGIN)))
        #print(  "click pos:", pos, " grid pos:", self.selected)        
        return(coord)
    
    def in_field(self, pos):
        """ verify if clicked pos is in playable grid area  - returns True/False """
        loc = self.coord_to_grid(pos)
        if loc[0] < 0 or loc[0] >= params.GRID_SIZE[0] or loc[1] < 0 or loc[1] >= params.GRID_SIZE[1]:
            #print("you missed the grid")
            return(False)
        else:
            return(True)
        
    def grid_clicked(self, pos):
        """ tells what grid was clicked on and reports for testing purposes 
            pos: the passed mouse coordinates variable passed through 
        """
        if self.in_field(pos):
            #print("click is in field")
            #print("pos clicked:", pos)
            loc = self.coord_to_grid(pos)
            if self.pawn_group.is_unit_in_grp_selected(self.coord_to_grid(pos)): # NOT WORKING - does not correctly identify tile location with mouse click
                #print("someone in this group was clicked on")
                dummy = False #                                                  - ADD things when a unit gets clicked on
            elif self.matrix[loc[0]][loc[1]].selected == False: #toggles selected to True
                self.matrix[loc[0]][loc[1]].selected = True
                print("toggled tile from false to true at this loc", loc)
            else: #toggles selected to True
                self.matrix[loc[0]][loc[1]].selected = False
                print("toggled tile from true to false")
                                
    def print_grid(self):
        """ prints text version of grid to shell """
        self.matrix[1][1].selected = True
        for row in range(0, self.nrows):
            col_output = ""
            for col in range(0, self.ncols):
                if self.matrix[row][col].contents != ():
                    col_output += " u"
                elif not self.matrix[row][col].contents and self.matrix[row][col].terrain_type == "water":
                    col_output += " -"
                else: #default is grass
                    if self.matrix[row][col].selected == True:
                        col_output += " S"
                    else:
                        col_output += " ."
            print(col_output)
            print()      
    
    def print_test_grid(self):
        self.matrix[2][2].contents = "unit"
        self.matrix[2][3].selected = True
        self.print_grid() 
        print("there should be a unit at 2,2 and a selected grassland at 2,3")
        
    #def is_adjacent(self,new_coord): #                                         NOTE: not currently using - old parameters
        #if new_coord[0] < self.coord[0] - 1 or new_coord[0] > self.coord[0] + 1 or new_coord[1] < self.coord[1] - 1 or new_coord[1] > self.coord[1] + 1:
            #print("not adjacent")
            #return(False)
        #elif new_coord  == self.coord:
            #print("already there")
            #return(False)
        #else:
            #return(True)
        
################################################################################
## TEST
################################################################################
if __name__ == "__main__":  
    pygame.init()
    
    tile_grid = Tile_grid("screen")
    # tile_grid.print_grid() # TEST to print initial grid - works
    print()
    
    tile_grid.print_test_grid() # TEST to see if units superscede terrain & grassland indicates selection
    
    
    
    print("--DONE--")  