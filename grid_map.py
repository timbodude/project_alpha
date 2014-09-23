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
                          MDW_BROWN, MDW_BLUE )
import params
import main_board

################################################################################

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
    
    def __init__(self, screen, nrows = params.GRID_SIZE[0], ncols = params.GRID_SIZE[1]):
        """ Create a new Grid_map with the given amount of rows and columns. 
        [x][y][layer]: x=x coord  y=y coord  
          layer: 0=empty unit slot (0 = empty)
                 1=terrain catagory
                 2=altitude
                 3=color_code
                 4=event
        """
        self.nrows = nrows # X coordinates
        self.ncols = ncols # Y coordinates
        self.grid = [[0] * self.ncols for i in range(self.nrows)] # creates & fills map with 0 - WORKS
        
        #for row in range(0,2):
            #for col in range(0,2):
                #for layer in range(0,5):
                    #self.grid[row][col][layer] = 0
        #print("grid:")
        #print(self.grid)
        #self.fill_grid()
        #self.fill_map() # repopulates map with random terrain
        self.blocked = defaultdict(lambda: False) # creates list to be populated by blocked spaces
        self.screen = screen
        self.selected = () # [0] = rows, [1] = cols
        
        # LEAVING OFF HERE - 
        """ need to SOMEWHERE create the subsystems in create_gml without getting
            stuck in a creation loop. Could create children in main program.
        """
        
    def create_gml(self, screen):
        """ creates grid map child layers """
        self.gml_unit = Gml_units(screen)
        self.gml_alt = Gml_altitude(screen)
        new_altitude.print_alt_map() # TEST OUTPUT
        self.gml_color = Gml_color(screen)
        for row in range(0, new_terrain.nrows):
            for col in range(0, new_terrain.ncols):
                new_color.grid[row][col] = new_color.adj_color(new_terrain.grid[row][col], new_altitude.grid[row][col])
                #print("adjusted color:", new_color.grid[row][col])  
        self.gml_event = Gml_event(screen)

    def fill_grid(self):
        """ fills initial grid layers with content """
        for row in range(0, self.nrows):
            for col in range(0, self.ncols):
                #self.grid[row][col][0] = self.fill_unit(row,col)
                self.fill_unit(row,col)
                self.grid[row][col][1] = self.fill_terrain(row,col)
                self.grid[row][col][2] = self.fill_altitude(row,col)
                self.grid[row][col][4] = self.fill_event(row,col)

    def fill_unit(self,row,col):
        """ fill with no unit """
        dummy = False
        #print("fill_unit check:", row, col, self.grid[row][col][0])
        #self.grid[row][col][0] = 0
        #return(0)
    
    #def fill_terrain(self,row,col):
        #""" fill with meadow terrain - TODO add variety 
        #also fills in color layer
        #number also indicates movement cost
          #0 blocked
          #1 paved roadmeadow - grass
        #"""
        #self.grid[row][col][3] = (0,128,0)
        #return(1)
    
    def fill_altitude(row,col):
        """ fill with altitude and adjust color """
        alt = int((randint(0,11) + randint(0,11) + randint(0,11) + randint(0,11))/4) - 5
        # ends with a number between -5 and 5 with average curve weighted toward 0
        r = self.grid[row][col][3][0]
        g = self.grid[row][col][3][1]
        b = self.grid[row][col][3][2]
        #print("rgb", r, g, b)
        
        ratio = alt * 18
        r *= ratio
        if r > 255: r = 255
        g *= ratio
        if g > 255: g = 255
        b *= ratio
        if b > 255: b = 255
        print("rgb - after alt adj", r, g, b)
        self.grid[row][col][3] = (r,g,b)
        return(alt)

    def fill_event(self):
        """ fill with events """
        dummy = False
    
    def update_grid(self): # TODO - add alt_map info
        for row in range(self.nrows):
            for column in range(self.ncols):
                
                #OLD METHOD - worked
                #color = LT_GRAY
                ##if self.grid[row][column] == 1:
                #if self.gml_color[row][column] == 1:                   
                    ##color = gml_alt.alt_map.color_diff(GREEN, row, column) # NOT WORKING YET
                    #color = MDW_GREEN
                #elif self.grid[row][column] == 2:
                    #color = MDW_BLUE
                #elif self.grid[row][column] == 3:
                    #color = MDW_BROWN
                    
                #NEW METHOND:
                color = gml_color.get_color(row, column)
                
                #in both methods
                pygame.draw.rect(  self.screen,
                                   color,
                                   [(params.FIELD_RECT[0] + row * (params.TILE_SIZE + params.MARGIN)),
                                    (params.FIELD_RECT[1] + column * (params.TILE_SIZE + params.MARGIN)),
                                    params.TILE_SIZE,
                                    params.TILE_SIZE] )
                                    #params.GRID_SIZE[0],
                                    #params.GRID_SIZE[1]])                     
                   
    def click_on_grid(self,pos):
        """ what happens when a grid unit gets clicked on """
        self.coord_to_grid(pos)
        if (  self.selected[0] >= 0 and
              self.selected[0] < self.nrows and 
              self.selected[1] >= 0 and 
              self.selected[1] < self.ncols):  
            print("selected:", self.selected)
            
            self.grid[self.selected[0]][self.selected[1]] = 1
        else:
            print("click out of range - ignoring")                                       
    
    #def fill_map(self):
        #""" fills map with random terrain """
        #for rows in range(self.nrows):
            #for cols in range(self.ncols):
                #self.grid[rows][cols] = choice(terrain_list) # fill from terrain types  
                
                ##self.grid[row].append(0) # Append a cell
    
    def set_blocked(self, coord, blocked=True):
        """ Set the blocked state of a coordinate. True = blocked. False = unblocked. 
            If false, is removed from the list self.blocked. """
        if blocked:
            self.blocked[coord] = True # add coordinate to blocked list
        else:
            if coord in self.blocked:
                del self.blocked[coord] # remove coordinate from blocked list

    def successors(self, c):
        """ returns list of all coordinates one step from c """
        slist = []
        for drow in (-1, 0, 1):
            for dcol in (-1, 0, 1):
                if drow == 0 and dcol == 0:
                    continue 
                newrow = c[0] + drow
                newcol = c[1] + dcol
                if (    0 <= newrow <= self.nrows - 1 and
                        0 <= newcol <= self.ncols - 1 and
                        self.grid[newrow][newcol] == 0):
                    slist.append((newrow, newcol))
        return slist 
    
    def move_cost(self, c1, c2):
            """ Returns Euclidean distance in grid spaces between c1 & c2 coordinages """
            print(c1, c2)
            return sqrt((c1[0] - c2[0]) ** 2 + (c1[1] - c2[1]) ** 2)     
    
    def is_in_range(self, c1, c2, distance = 1):
        """ returns True/False whether c1 is within specified Euclidean distance of c2 """
        print()
        print("Euclidean distance is:", self.move_cost(c1, c2))
        if self.move_cost(c1, c2) > distance:
            print("not in range")
            return(False)
        elif c2 == c1:
            print("already there")
            return(False)
        else:
            print("bingo - is in range")
            return(True) 
        
    def is_in_range_sq(self, c1, c2, distance = 1):
        """ returns True/False whether c1 is within specified non-Euclidean distance of c2 """   
        print()
        if (  c2[0] < c1[0] - distance or 
              c2[0] > c1[0] + distance or 
              c2[1] < c1[1] - distance or 
              c2[1] > c1[1] + distance  ):
            print("not in range")
            return(False)
        elif c2 == c1:
            print("already there")
            return(False)
        else:
            print("bingo - is in range")
            return(True)         
    
    def printme(self):
        """ Print the map via text """
        print("blocked:", self.blocked)
        for row in range(self.nrows):
            #print(self.grid[row])
            col_output = ""         
            for column in range(self.ncols):
                if (row,column) in self.blocked: # print X if square is blocked
                    col_output += "X " 
                else:
                    col_output += str(self.grid[row][column]) + " "
            print(col_output)

        
    def coord_to_grid(self, pos):
        """ returns grid location based on pos(x,y) """
        self.selected = (  int((pos[0] - params.FIELD_RECT[0]) / (params.TILE_SIZE + params.MARGIN)),
                           int((pos[1] - params.FIELD_RECT[1]) / (params.TILE_SIZE + params.MARGIN)))
        print(  "click pos:", pos, " grid pos:", self.selected)        
        return
    
################################################################################
## gml_units                                               grid map layer: units
class Gml_units(Grid_map):
    """ Grid_map child class containing units
        fill with no unit """
    def __init__(self, screen, nrows = params.GRID_SIZE[0], ncols = params.GRID_SIZE[1]):
        Grid_map.__init__(self, screen, nrows = params.GRID_SIZE[0], ncols = params.GRID_SIZE[1])
        #populate map with non-overlapping units
        for row in range(0, nrows):
            for col in range(0, ncols):
                #print("fill_unit check:", row, col, self.grid[row][col])
                self.grid[row][col] = 0
                #return(0)
        
class Gml_terrain(Grid_map):
    """ Grid_map child class containing terrain
        number also indicates movement cost
          0 blocked
          1 paved roadmeadow - grass
        """
    def __init__(self, screen, nrows = params.GRID_SIZE[0], ncols = params.GRID_SIZE[1]):
        Grid_map.__init__(self, screen, nrows = params.GRID_SIZE[0], ncols = params.GRID_SIZE[1])  
        for row in range(0, nrows):
            for col in range(0, ncols):
                self.grid[row][col] = self.fill_map(row,col) # get terrain from method 
                #self.grid[row][col] = (0,128,0) # - sets color
                #self.fill_map(row, col) # repopulates map with random terrain

    def fill_map(self, row, col):
        """ fills map with random terrain """
        terrain = choice(terrain_list)
        #print(terrain, terrain_des[terrain][0])
        return(terrain) # fill from terrain types  

    def update_terrain(self, row, col):
        """ output color from terrain gml to grid """
        dummy = False
          
class Gml_altitude(Grid_map):
    """ fills map with altitude
        also fills in and adjusts color layer - but not yet!
    """
        
    def __init__(self, screen, nrows = params.GRID_SIZE[0], ncols = params.GRID_SIZE[1]):
        Grid_map.__init__(self, screen, nrows = params.GRID_SIZE[0], ncols = params.GRID_SIZE[1])  
        #print()
        #print()
        #print("row/col:", nrows, ncols)
        #print()
        #print()
        for row in range(0, nrows):
            alt = ""
            for col in range(0, ncols):  
                self.grid[row][col] = self.fill_map(row, col) # get altitude from method 
            
    def fill_map(self, row, col):
        """ fills map with random altitude, most common at 0 """
        variation = 10 # determines how uneven the land is
        amount = 0
        for num in range(variation):
            amount += randint(0,11)
        amount = int(amount/variation) -5
        return(amount) # fill with altitude types
    
    def get_alt(self, row, col):
        return(self.grid[row][col])
        
    def print_alt_map(self):
        for row in range(0, self.nrows):
            alt = ""
            for col in range(0, self.ncols):         
              ## print a test
                if self.grid[row][col] <0: alt += " " + str(self.grid[row][col])
                else: alt += "  " + str(self.grid[row][col])
            #print(alt)

class Gml_color(Grid_map):
    """ Grid_map child class containing color adjusted by altitude
    """
    def __init__(self, screen, nrows = params.GRID_SIZE[0], ncols = params.GRID_SIZE[1]):
        Grid_map.__init__(self, screen, nrows = params.GRID_SIZE[0], ncols = params.GRID_SIZE[1])  
        for row in range(0, nrows):
            for col in range(0, ncols):
                self.grid[row][col] = 2
                # send row & col to color changeer in terrain method
                # return will be new color
                # self.grid[row][col] = 2
                
    def adj_color(self, terrain, altitude):
        """ adjust color by altitude
            NOTE: half the code loop must be in regular run-program block
        """
        old_color_formula = terrain_des[terrain][2]
        #print("old_color_formula, altitude:", old_color_formula, altitude)  
        r = old_color_formula[0]
        g = old_color_formula[1]
        b = old_color_formula[2]
        adjustment = altitude * 18
        #print("rgb:", r, g, b, "adjustment", adjustment)
        new_r = r + adjustment
        if new_r < 0: new_r = 0
        elif new_r>255: new_r = 255
        new_g = g + adjustment
        if new_g < 0: new_g = 0
        elif new_g>255: new_g = 255        
        new_b = b + adjustment
        if new_b < 0: new_b = 0
        elif new_b>255: new_b = 255        
        #print("new color:", new_r, new_g, new_b)
        return((new_r, new_g, new_b))
    
    def print_me(self):
        print()
        print("checking gml_color")
        for row in range(self.nrows):
            print(gml_color.grid[row])      
            
    def get_color(self, row, column):
        return(self.grid[row][column])

class Gml_event(Grid_map):
    """ Grid_map child class containing events - but no events yet!
    """
    def __init__(self, screen, nrows = params.GRID_SIZE[0], ncols = params.GRID_SIZE[1]):
        Grid_map.__init__(self, screen, nrows = params.GRID_SIZE[0], ncols = params.GRID_SIZE[1])  
        for row in range(0, nrows):
            for col in range(0, ncols):
                self.grid[row][col] = 0
        
################################################################################        
## helper functions

   
        
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
    gridmap.create_gml #                                                        * REQUIRED CALL TO CREATE GRIDMAP


    # TESTING THESE - also copying to battle_grid temporarily
    gml_unit = Gml_units(screen)
    gml_alt = Gml_altitude(screen)
    gml_alt.print_alt_map() # TEST OUTPUT
    gml_color = Gml_color(screen)
    for row in range(0, gridmap.nrows):
        for col in range(0, gridmap.ncols):
            gml_color.grid[row][col] = gml_color.adj_color(gridmap.grid[row][col], gml_alt.grid[row][col])
            #print("adjusted color:", gml_color.grid[row][col])  
    gml_event = Gml_event(screen)    
    
    
    
    
    
    #new_alt = Gml_altitude(screen, 5 , 5)
    #gridmap = Grid_map(screen)
    
    #gridmap.printme()
    
    ##TEST PRINTME - works
    #gridmap.grid[0][0] = 5
    #gridmap.grid[4][2] = 9
    #gridmap.printme()
    
    ##TEST move_cost - works
    #cost = gridmap.move_cost((0,0), (4,4))
    #print("movement cost =", cost)
    #cost = gridmap.move_cost((0,0), (0,4))
    #print("movement cost =", cost)  
    #print()
    
    ##TEST blocked - works
    #gridmap.set_blocked((2,2))
    #gridmap.set_blocked((0,0))
    #gridmap.printme()
    #gridmap.set_blocked((0,0), blocked = False)
    #gridmap.set_blocked((2,2), blocked = False)
    #gridmap.printme()   
    
    ##TEST successors - works
    #print(gridmap.successors((2,2)))
    
    ##TEST is_in_range
    #gridmap.is_in_range((1,1), (2,2))
    #gridmap.is_in_range((1,1), (3,3))
    #gridmap.is_in_range((3,3), (3,3))
    #gridmap.is_in_range((1,1), (2,2), 2)
    #gridmap.is_in_range((1,0), (1,4), 3)
    #gridmap.is_in_range((1,0), (4,0), 3)
    #gridmap.is_in_range((1,0), (4,4), 4)
    #gridmap.is_in_range((1,0), (3,3), 4)
    #gridmap.is_in_range((0,0), (0,1))
    #gridmap.is_in_range((0,0), (1,0))
    #gridmap.is_in_range((0,0), (1,1))
    #gridmap.is_in_range((0,1), (0,0))
    #gridmap.is_in_range((1,0), (0,0))
    #gridmap.is_in_range((1,1), (0,0))    
    
    ##TEST is_in_range_sq - works
    #gridmap.is_in_range_sq((0,0), (0,1))
    #gridmap.is_in_range_sq((0,0), (1,0))
    #gridmap.is_in_range_sq((0,0), (1,1))
    
    print("-- It all works pre-screen--")
    
    while done == False:
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                done = True # Flag that we are done so we exit this loop
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # User clicks the mouse. Get the position
                pos = pygame.mouse.get_pos()
                # Change the x/y screen coordinates to grid coordinates
                
                #x = params.GRID_SIZE[0] * params.GRID_SIZE
                #y = params.GRID_SIZE[1] * params.GRID_SIZE
                #gridmap.cols = pos[0] // (x + params.MARGIN)
                #gridmap.rows = pos[1] // (y + params.MARGIN)
                
                #TODO - create function to identify location of grid by click pos
                #[int(pos[0]/params.GRID_SIZE)][int(pos[1]/params.GRID_SIZE)] 
                
                #print("pos, posx, fieldrect0, tilesize, margin:  ", pos, pos[0], params.FIELD_RECT[0], params.TILE_SIZE, params.MARGIN)

                      
                gridmap.click_on_grid(pos)
                
                
                #gridmap.coord_to_grid(pos)
                #if (  gridmap.selected[0] >= 0 and
                      #gridmap.selected[0] < gridmap.nrows and 
                      #gridmap.selected[1] >= 0 and 
                      #gridmap.selected[1] < gridmap.ncols):  
                    #print("selected:", gridmap.selected)
                    
                    #gridmap.grid[gridmap.selected[0]][gridmap.selected[1]] = 1
                #else:
                    #print("click out of range - ignoring")
                
                
                
                # Set that location to zero
                #gridmap[gridmap.rows][gridmap.cols] = 1
     
        # Set the screen background
        #main_board.draw_background(screen, image_lib.battle_grid_img, params.FIELD_RECT) # Redraw the background
        screen.fill(BLACK)
     
        # Draw the grid
        #gridmap.update_grid()
        #gridmap.update_grid(new_alt) # this version pre- child class creation in class init
         
        # Limit to 20 frames per second
        clock.tick(20)
     
        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()
         
    # Be IDLE friendly. If you forget this line, the program will 'hang'
    # on exit.
    
    gridmap.printme()
    gml_color.print_me()
    
    print()
    print("-- TEST DONE --")
    print()
    pygame.quit()
    sys.exit()   