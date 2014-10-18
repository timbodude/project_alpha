#Max Line Length As according to PEP-0008 for docstrings/comments(72)##
#Max Line Length As according to PEP-0008 for everything else(79)#############

#######################################################################
## gridmap
#######################################################################
""" draws battle area, including grid for units """

""" NOTES:
    Make terrain altitude more consistant with surrounding terrain, 
    allow for 
    degrees of variation based on ruggedness variable.
    
    Consider redoing with Grid_map.color, Grid_map.alt etc... as sub
    grids instead of as child class elements. less complicated and can 
    make calls out to def statements for updating different elements 
    from a single for row for col pass. Remove grid creation from main 
    parent and create within each sub element.
"""
#######################################################################

import pygame
from images_lib import (  GREEN, GRASS, BLACK, LT_GRAY )
import unit_simp
from pygame import Rect

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
FIELD_RECT = Rect(0, 0, 600, 600)
MARGIN = 1
TILE_SIZE = 23
GRID_SIZE = (int(FIELD_RECT[2]/(TILE_SIZE + MARGIN)), 
             int(FIELD_RECT[3]/(TILE_SIZE + MARGIN)))
MESSAGE_RECT = Rect(600, 0, 800, 600)
MESSAGE_SIZE = (int(MESSAGE_RECT[2])-MESSAGE_RECT[0], 
                int(MESSAGE_RECT[3]))
end_check = False
paused = False
won = False # flag for battle is over
TURN_COUNT = 0

class Grid_Map(object):
    """ Rectangular grid map consisting of nrows X ncols squares.
        Squares can be blocked (by obstacles). """
    
    def __init__(self, screen):
        """ Create a new Grid_map with the given amount of 
        rows/columns/info from params. 
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
        # number of horizontal grid spaces in grid map
        self.nrows=int(FIELD_RECT[2]/TILE_SIZE)              
        #number of vertical grid spaces in grid map               
        self.ncols = int(FIELD_RECT[3]/TILE_SIZE)  
        self.fields = 8
        self.matrix = [[[0 for i in range(self.fields)] 
                        for i in range(self.ncols)] 
                       for i in range(self.nrows)]
        self.screen = screen
        # [0] = rows, [1] = cols 
        #NOTE: this is for dealing with mouse click selection
        self.selected = () 
        self.fill_grid() # fills the grid's matrix with content
        self.last_clicked =(-1,-1)# coord for last tile clicked 
        
         # adds group of units from unit_simp
        self.pawn_group = unit_simp.Simp_unit_group()
        
        
    def fill_grid(self): # this is called by the init method
        """ fills initial matrix - it's already filled with a 0 """
        for row in range(0, self.nrows):
            for col in range(0, self.ncols):
                self.matrix[row][col][0] = self.fill_terrain()
                self.matrix[row][col][1] = self.fill_object()
                # color - or sprite image of unit
                self.matrix[row][col][2] = self.fill_unit() 
                self.matrix[row][col][3] = self.fill_event()
                self.matrix[row][col][4] = self.fill_passable()               
                self.matrix[row][col][5] = self.fill_altitude()
                self.matrix[row][col][6] = self.fill_movecost()
                self.matrix[row][col][7] = self.fill_info()
        

    # fill with meadow terrain 
    # TODO: add variety 
    # TODO: replace with fill logic / default: GRASS
    def fill_terrain(self):
        fill = GRASS                                                      
        print("terrain added")
        return(fill)
    
    # TODO: add list of objects to their corresponding grid
    # TODO: replace with object list / default: empty
    def fill_object(self):
        """ initially filled with a placeholder of 0 """ 
        fill = () 
        print("object added")


    def fill_unit(self):
        """ initially filled with a placeholder of 0 """ #                      - TODO: add list of units to their corresponding grid
        fill = () #                                                             _ TODO: replace with unit list / default: empty
        print("units added")
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
    
    ## Grid Helper Methods #####################################################

    def update_grid(self): #                                                    - TODO - adapt to grid spaces with contents
        self.grid_unit_color_updater() # update unit positions
        for row in range(self.nrows):
            for col in range(self.ncols):
                if self.matrix[row][col][2] == 0: # print tile color if tile is empty
                    curser_color = self.matrix[row][col][0]
                else: # print unit color if tile has a unit in it
                    curser_color = self.matrix[row][col][2]
                pygame.draw.rect(  self.screen,
                                   curser_color,
                                   [(FIELD_RECT[0] + row * (TILE_SIZE + MARGIN)),
                                    (FIELD_RECT[1] + col * (TILE_SIZE + MARGIN)),
                                    TILE_SIZE,
                                    TILE_SIZE] )              
                        
    def grid_unit_color_updater(self):
        for row in range(self.nrows): # erase old data
            for col in range(self.ncols):
                self.matrix[row][col][2] = 0        
        for unit in self.pawn_group.group_list: # replace current unit locations
            #print("oh, here's a unit.")    
            #print("---------------------------- unit loc:", unit.loc)
            self.matrix[unit.loc[0]][unit.loc[1]][2] = unit.color
            #print("unit color:", unit.color)

    def coord_to_grid(self, pos):
        """ prints grid location based on pos(x,y) for test purposes of clicked location """
        self.selected = (  int((pos[0] - FIELD_RECT[0]) / (TILE_SIZE + MARGIN)),
                           int((pos[1] - FIELD_RECT[1]) / (TILE_SIZE + MARGIN)))
        #print(  "click pos:", pos, " grid pos:", self.selected)        
        return(self.selected)
    
    def print_grid(self):
        """ outputs text version of grid for testing """
        junk = False
        print("I'm printing the screen now")
        
    def in_field(self, pos):
        """ verify if clicked pos is in grid area  - returns True/False """
        loc = self.coord_to_grid(pos)
        if loc[0] < 0 or loc[0] >= GRID_SIZE[0] or loc[1] < 0 or loc[1] >= GRID_SIZE[1]:
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
                FIELD_RECT[0], 
                TILE_SIZE, 
                MARGIN )        
        if self.in_field(pos):
            if self.last_clicked != (-1,-1) and self.matrix[self.last_clicked[0]][self.last_clicked[1]][0] == GREEN: #reset previous tile clicked
                self.matrix[self.last_clicked[0]][self.last_clicked[1]][0] = GRASS 
            self.last_clicked = self.coord_to_grid(pos) # toggle target tile to new color
            self.matrix[self.last_clicked[0]][self.last_clicked[1]][0] = GREEN
            #print("last click was on:", self.last_clicked)