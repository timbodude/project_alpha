################################################################################
## unit_simp
## simple player units for initial battle sequence testing
################################################################################

from random import randint
from images_lib import LT_GRAY
import grid_map 

################################################################################
""" Things to consider and set: 
    - how far unit can move/turn
    - how likely it is for a unit to get initiative
    - how likely it is for a unit to have successful attack
    - how likely it is for a unit to have a successful defense
"""
unit_start_qty = 5 # number of starting army units under player control

################################################################################

class Simp_unit():
    """ generic class for basic player unit types """ 
    def __init__(self):
        self.loc = () # location in grid
        self.color = LT_GRAY # can be replaced with image
        self.state = True # (bool) True: alive False: dead
        print("I made me a man, and his name is Jim")
        self.place_unit()

    def place_unit(self):
        """ set initial coordinates in tile_map during unit creation 
            Right now, I'm just picking a random tile with the hope of no duplication
            """
        dummy = False
        self.loc = (randint(0, grid_map.GRID_SIZE[0]), randint(0, grid_map.GRID_SIZE[1])) # location in grid
        print("location in grid:", self.loc)
        
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
        print("group:", self.group_list)         
