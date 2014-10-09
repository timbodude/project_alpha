################################################################################
## gridmap
################################################################################
""" draws battle area, including grid for units """

""" NOTES:
    Make terrain altitude more consistant with surrounding terrain, allow for 
    degrees of variation based on ruggedness variable.
    
    Consider redoing with Grid_map.color, Grid_map.alt etc... as sub grids instead
    of as child class elements. less complicated and can make calls out to def 
    statements for updating different elements from a single for row for col pass. 
    Remove grid creation from main parent and create within each sub element.
    


NOTE: REDO whole thing with multidimensional array using:

2-D array:
matrix = [[0 for i in range(5)] for i in range(5)]
matrix[0][0] = 1
matrix[4][0] = 5
print(matrix)
print(matrix[0][0]) # prints 1
print(matrix[4][0]) # prints 5

3-D array:
matrix = [[[0 for i in range(5)] for i in range(5)] for i in range(5)]
matrix[0][0][0]= 1
matrix[4][0][4]= 5
print(matrix)
print(matrix[0][0][0]) # prints 1
print(matrix[4][0][4]) # prints 5

Each grid contains:
0 = terrain type - or just do a color and the color name itself is the label for the type
1 = object list (container)
2 = unit list (container)
3 = passable (true/false) ???
4 = altitude ???

    """

################################################################################
import images_lib
import sys
import pygame
from collections import defaultdict
from math import sqrt
from random import choice, randint
from images_lib import (  Image_lib, 
                          BLACK, WHITE, GREEN, RED, LT_GRAY, MDW_GREEN, 
                          MDW_BROWN, MDW_BLUE, GRASS )
import params
import main_board

################################################################################
## Note this stuff is brainstorming from BT (Before Travis) not using it, but don't want to discard it yet
terrain_des = { 0: ("impassable", "images_lib.terrain_plains_img", RED),
                1: ("road", "images_lib.terrain_plains_img", LT_GRAY),
                2: ("plains", "images_lib.terrain_plains_img", MDW_GREEN),
                4: ("woods", "images_lib.terrain_woods_img", MDW_BROWN),
                6: ("water", "images_lib.terrain_water_img", MDW_BLUE)  }
    # number: label, image file, color (movement cost = number, 0 = impassable)

terrain_list = [  2,2,2,2,2,2,
                  4,4,4,
                  6 ] 
    # possibility chart for filling in the random map

################################################################################

class Grid_map(object):
    """ Rectangular grid map consisting of nrows X ncols squares.
        Squares can be blocked (by obstacles). """
    
    def __init__(self, screen):
        """ Create a new Grid_map with the given amount of rows/columns/info from params. 
        [x][y][info field]: x=x coord  y=y coord  
          layer: 0 = terrain color name (name and color name are same)
                 1 = object list (container)
                 2 = unit list (container)
                 3 = event list (container)
                 4 = passable (bool)
                 5 = altitude
                 6 = movement cost
                 7 = additional info
        """
        self.nrows = int(params.FIELD_RECT[2]/params.TILE_SIZE) # number of horizontal grid spaces in grid map
        self.ncols = int(params.FIELD_RECT[3]/params.TILE_SIZE) # number of vertical grid spaces in grid map
        self.fields = 8
        self.matrix = [[[0 for i in range(self.fields)] for i in range(self.ncols)] for i in range(self.nrows)]
        self.screen = screen
        self.selected = () # [0] = rows, [1] = cols NOTE: this is for dealing with mouse click selection
        self.fill_grid() # fills the grid's matrix with content
        self.last_clicked =(-1,-1)# coord for last tile clicked 
        
    def fill_grid(self): # this is called by the init method
        """ fills initial matrix - it's already filled with a 0 """
        for row in range(0, self.nrows):
            for col in range(0, self.ncols):
                self.matrix[row][col][0] = self.fill_terrain()
                self.matrix[row][col][1] = self.fill_object()
                self.matrix[row][col][2] = self.fill_unit()
                self.matrix[row][col][3] = self.fill_event()
                self.matrix[row][col][4] = self.fill_passable()               
                self.matrix[row][col][5] = self.fill_altitude()
                self.matrix[row][col][6] = self.fill_movecost()
                self.matrix[row][col][7] = self.fill_info()
    
    # BELOW are sub-methods called to by the fill_grid() method
    def fill_terrain(self):
        # fill with meadow terrain                                              - TODO: add variety 
        fill = GRASS #                                                          - TODO: replace with fill logic / default: GRASS
        print("terrain added")
        return(fill)
    
    def fill_object(self):
        """ initially filled with a placeholder of 0 """ #                      - TODO: add list of objects to their corresponding grid
        fill = () #                                                             _ TODO: replace with object list / default: empty
        print("object added")
        #return(fill)

    def fill_unit(self):
        """ initially filled with a placeholder of 0 """ #                      - TODO: add list of units to their corresponding grid
        fill = () #                                                             _ TODO: replace with unit list / default: empty
        print("unit added")
        #return(fill)
    
    def fill_event(self):
        # fill with meadow terrain                                              - TODO: add variety 
        fill = () #                                                             - TODO: replace with fill logic / default: empty
        print("event added")
        return(fill)
    
    def fill_passable(self):
        # show if tile is passable (bool) / default: True (passable)
        fill = True
        print("passable added")
        return(fill)    
    
    def fill_altitude(self):
        """ fill with altitude and adjust color """ #                           - TODO: add alt formula for geo shape of hills/valleys
        """ altitude = range from 0=6, with 3 being sea level """
        alt = 3 #                                                               - TODO: replace with altutude logic / default: 3
        print("altitude added")
        return(alt)
    
    def fill_movecost(self):
        # show cost to enter tile / default: 1
        fill = 1 #                                                              - TODO: change cost based upon altitude and terrain type
        print("movement cost added")
        return(fill) 
    
    def fill_info(self):
        # any special info regarding tile / default: none
        fill = "" #                                                             - TODO: develop section
        print("info added")
        return(fill)  
    
    ## Grid Helper Methods ########################

    def update_grid(self): #                                                    - TODO - adapt to grid spaces with contents
        for row in range(self.nrows):
            for col in range(self.ncols):
                pygame.draw.rect(  self.screen,
                                   self.matrix[row][col][0],
                                   [(params.FIELD_RECT[0] + row * (params.TILE_SIZE + params.MARGIN)),
                                    (params.FIELD_RECT[1] + col * (params.TILE_SIZE + params.MARGIN)),
                                    params.TILE_SIZE,
                                    params.TILE_SIZE] )
        
    def coord_to_grid(self, pos):
        """ prints grid location based on pos(x,y) for test purposes of clicked location """
        self.selected = (  int((pos[0] - params.FIELD_RECT[0]) / (params.TILE_SIZE + params.MARGIN)),
                           int((pos[1] - params.FIELD_RECT[1]) / (params.TILE_SIZE + params.MARGIN)))
        print(  "click pos:", pos, " grid pos:", self.selected)        
        return(self.selected)
    
    def print_grid(self):
        """ outputs text version of grid for testing """
        junk = False
        print("I'm printing the screen now")
        
    def in_field(self, pos):
        """ verify if clicked pos is in grid area  - returns True/False """
        loc = self.coord_to_grid(pos)
        if loc[0] < 0 or loc[0] >= params.GRID_SIZE[0] or loc[1] < 0 or loc[1] >= params.GRID_SIZE[1]:
            print("you missed the grid")
            return(False)
        else:
            return(True)
        
    def grid_clicked(self, pos):
        """ tells what grid was clicked on and reports for testing purposes 
            pos: the passed mouse coordinates variable passed through """
        print("I'm checking to see what grid was clicked on.")
        print(  "pos, matrix coord, fieldrect0, tilesize, margin:  ", 
                pos, 
                self.coord_to_grid(pos),
                params.FIELD_RECT[0], 
                params.TILE_SIZE, 
                params.MARGIN )        
        if self.in_field(pos):
            if self.last_clicked != (-1,-1) and self.matrix[self.last_clicked[0]][self.last_clicked[1]][0] == GREEN: #reset previous tile clicked
                self.matrix[self.last_clicked[0]][self.last_clicked[1]][0] = GRASS 
            self.last_clicked = self.coord_to_grid(pos) # toggle target tile to new color
            self.matrix[self.last_clicked[0]][self.last_clicked[1]][0] = GREEN
            print("last click was on:", self.last_clicked)
    
    
################################################################################
## TEST
################################################################################
if __name__ == "__main__":  
    #pygame.init()

    screen = pygame.display.set_mode((params.SCREEN_WIDTH, params.SCREEN_HEIGHT), 0, 32)
    #pygame.display.set_caption("Array Backed Grid")
    #image_lib = Image_lib()
    #battle_grid_img = images_lib.battle_grid_img    
    done = False
    clock = pygame.time.Clock()
    
    # TEST INIT - works
    #gridmap = Gml_terrain(screen, 5 , 5)
    #new_unit_grid = Gml_units(screen, 5, 5)
    #new_alt_grid = Gml_altitude(screen, 5, 5)
    
    gridmap = Grid_map(screen) #                                                * REQUIRED CALL TO CREATE GRIDMAP
    
    ##TEST PRINTME - works
    gridmap.print_grid()
    
    #TEST move_cost
    cost = gridmap.matrix[1][1][6]
    print("movement cost =", cost)
    print()
      
    print("-- It all works pre-screen--")
    
    while done == False:
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                done = True # Flag that we are done so we exit this loop
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # User clicks the mouse. Get the position
                pos = pygame.mouse.get_pos()
                gridmap.grid_clicked(pos)
                
                # Check to see if click was in grid field
                if gridmap.in_field(pos):
                    print("you hit the grid")
                elif not gridmap.in_field(pos):
                    print("you missed the grid")

        # Set the screen background
        #main_board.draw_background(screen, image_lib.battle_grid_img, params.FIELD_RECT) # Redraw the background
        screen.fill(BLACK)
     
        # Draw the grid
        gridmap.update_grid()
         
        # Limit to 20 frames per second
        clock.tick(20)
     
        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()
         
    gridmap.print_grid()
   
    print()
    print("-- TEST DONE --")
    print()
    pygame.quit()
    sys.exit()   