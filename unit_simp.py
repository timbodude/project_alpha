################################################################################
## unit_simp
## simple player units for initial battle sequence testing
################################################################################

import pygame
from pygame.sprite import Sprite
import sys
import params #                                                                  NOTE: this will come from the parent loop instead of params
from random import randint
from images_lib import LT_GRAY

################################################################################
""" Things to consider and set: 
    - how far unit can move/turn
    - how likely it is for a unit to get initiative
    - how likely it is for a unit to have successful attack
    - how likely it is for a unit to have a successful defense
"""
unit_start_qty = 5 # number of starting army units under player control

################################################################################

class Simp_unit(Sprite):
    """ generic class for basic player unit types """ 
    def __init__(self):
        """ Notes:
        """
        Sprite.__init__(self)
        self.loc = () # location in grid
        self.color = LT_GRAY # can be replaced with image
        self.state = True # (bool) True: alive False: dead
        #print("I made me a man, and his name is Jim")
        self.place_unit()
        self.active = False # True: unit has been clicked on by user

    def place_unit(self):
        """ set initial coordinates in tile_map during unit creation 
            Right now, I'm just picking a random tile with the hope of no duplication
            """
        dummy = False
        self.loc = (randint(0, params.GRID_SIZE[0]), randint(0, params.GRID_SIZE[1])) # location in grid
        #print("location in grid:", self.loc)
        
    def unit_click_check(self, coord):
        """ see if unit has been checked on 
            coord: grid tile position
        """
        #print("I'm checking to see if unit was clicked on")
        if coord == self.loc:
            #print("bingo, in tile #:", coord)
            self.active = True
            return True
        else:
            print("not this one at:", coord)
        
class Simp_unit_group(object):
    """ player unit group """
    def __init__(self, total = unit_start_qty):
        """ total: number of units in group to be created (default is variable)
        """
        self.group_list = [] # create container
        self.Simp_unit_group_fill(total) # create units
        
    def Simp_unit_group_fill(self, total = unit_start_qty):
        """ fill unit group with initial units 
            total: number of units in group to be created (default is variable)
        """
        for i in range(0, unit_start_qty):
            new = Simp_unit()
            self.group_list.append(new)
        #print("group:", self.group_list)
        
    def su_grp_click_check(self, coord):
        """ check to see if any unit in group was clicked to make active 
            coord: mouse click coordinates
        """
        for unit in self.group_list:
            if unit.unit_click_check(coord): 
                #print("hey, you got one!")
                return(True)


################################################################################
## TEST
################################################################################

if __name__ == "__main__":  
    
    #pawn = Simp_unit()
    pawn_group = Simp_unit_group()
    
    for unit in pawn_group.group_list:
        print("unit loc:", unit.loc)
    
    print()
    print("-- TEST DONE --")
    print()
    pygame.quit()
    sys.exit()