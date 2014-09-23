################################################################################
## hex_grid
################################################################################

import images_lib
import pygame
from random import choice

################################################################################

terrain_des = { 0: ("plains", 0, "images_lib.terrain_plains_img"), # number: label, movement penalty, image file
                1: ("water", 0.3, "images_lib.terrain_water_img"), 
                2: ("woods", 0.6, "images_lib.terrain_woods_img") }

terrain_list = [0,0,0,0,0,0,2,2,2,1] # possibility chart for filling in the random map

################################################################################

class Hex_space(object):
    """ individual space in hex grid """
    def __init__(self, loc):
        self.terrain = [0] # terrain type - correlates with terrain_des library
        self.c_lvl = 0 # elevation
        self.contents = {} # library container for characteristics, effects, events...  
        print("I made a hex_space.")
        
class Hex_grid(object):
    """ class for containing battle map 
        (0,0) is upper left corner """
    def __init__(self, width = 10, height = 10):
        self.width = width
        self.height = height
        #self.hex_map = [0,0]
        print("I made a hex_grid.")
        self.fill_grid() # fill up grid with individual spaces
        
    def fill_grid(self):
        self.grid = []
        for row in range(self.width):
            self.grid.append([])
            for column in range(self.height):
                self.grid[row].append(choice(terrain_list)) # fill from terrain types
            print(self.grid[row])
        
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
    
    
    new_grid = Hex_grid()
    print("contents of 2,2:", new_grid.grid[2][2])
    print("contents of row 4:", new_grid.grid[4])
    
 
    #new_space = Hex_space((0,0))
    
    #new_grid.is_adjacent()
    
    print("--DONE--")