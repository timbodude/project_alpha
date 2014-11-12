################################################################################
## unit_simp
## simple player units for initial battle sequence testing
################################################################################

import pygame
from pygame.sprite import Sprite
import sys
import params #                                                                  NOTE: this will come from the parent loop instead of params
from random import randint
from images_lib import (  LT_GRAY , WHITE)
from helper_apps import calc_move

################################################################################
""" Things to consider and set: 
    - how far unit can move/turn
    - how likely it is for a unit to get initiative
    - how likely it is for a unit to have successful attack
    - how likely it is for a unit to have a successful defense
"""
unit_start_qty = 5 # number of starting army units under player control
players_start_qty = 2 # number of starting players 

################################################################################

class Simp_unit(Sprite):
    """ generic class for basic player unit types """ 
    def __init__(self, screen):
        """ Notes:
        """
        Sprite.__init__(self)
        self.loc = () # location in grid (in coordinates)
        self.color = LT_GRAY # can be replaced with image
        self.alt_color = WHITE
        self.state = True # (bool) True: alive False: dead
        #print("I made me a man, and his name is Jim")
        self.place_unit()
        self.active = False # True: unit has been clicked on by user
        self.targ_tile = () # tile unit is moving into (in coordinates)
        self.selected = False # indicates a unit is clicked on by player
        self.screen = screen

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
            #print("not this one at:", coord)
            dummy = False #                                                      - do whatever happense when you don't click on a unit
        
    def move_unit(self): #                                                       - should be called from gridmap updating area to see if melee occurs
        """ move unit into next square if empty """
        print("moving unit")
        if self.active == True and self.loc != self.targ_tile:
            print("i should move", self.loc, self.targ_tile)
            calc_move(self.loc, self.targ_tile)
            print("i didn't really move, I just though about where to go")
        else:
            print("I'm at my target location")
            
    def update_unit(self):
        """ update unit and print to screen """
        #print("printing a unit to screen")
        if self.selected == False: #check to see if unit is active or not to determine color and assign to curser_color
            curser_color = self.color
        else: 
            curser_color = self.alt_color
        #print("selected, curser color:", self.matrix[row][col].selected, curser_color)
        pygame.draw.rect(  self.screen,
                           curser_color,
                           [(params.FIELD_RECT[0] + self.loc[0] * (params.TILE_SIZE + params.MARGIN)),
                            (params.FIELD_RECT[1] + self.loc[1] * (params.TILE_SIZE + params.MARGIN)),
                            params.TILE_SIZE,
                            params.TILE_SIZE] )        
        
        
################################################################################                          
class Simp_unit_group(object):
    """ player unit group """
    def __init__(self, screen, total = unit_start_qty):
        """ total: number of units in group to be created (default is variable)
        """
        self.group_list = [] # create container to hold individual units for player's group
        self.Simp_unit_group_fill(screen, total) # create units
        
    def Simp_unit_group_fill(self, screen, total = unit_start_qty):
        """ fill unit group with initial units 
            total: number of units in group to be created (default is variable)
        """
        for i in range(0, unit_start_qty):
            new = Simp_unit(screen)
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
            
    def update_group(self): # Not using this at this point
        """ updating a group and outputing to screen """
        print("Updating a group of units")

################################################################################
class Player(object):
    """ Player class """
    def __init__(self, screen):
        self.name = "Player Name"
        self.units = []
        self.create_player_units(screen)
        
    def create_player_units(self, screen):
        new = Simp_unit_group(screen) # create a group of units
        self.units.append(new)
        
    def print_player_units(self):
        print("Player:", self.name)
        for group in self.units:
            for unit in group.group_list:
                print("unit loc:", unit.loc)
                
    def update_player(self):
        """ update player """
        # do whatever is necessary to update the player
        #print("updating player")
        for group in self.units:
            for unit in group.group_list:
                unit.update_unit()
        
 
class P_u_group(object):
    """ Container class to hold unit groups for each player """
    def __init__(self, screen, ttl_players = players_start_qty):
        self.players = [] # create container for each player's group
        self.create_player_group(screen, ttl_players)
        
    def create_player_group(self, screen, ttl_players):
        """ method for creating all players """
        for player in range(0,ttl_players):
            new = Player(screen)
            self.players.append(new)
            
    def print_all_player_units(self):
        """ test to print to shell all units of all teams """
        for player in self.players:
            player.print_player_units()
            
    def update_players(self):
        """ update players and print to screen """
        #print("updating all players")
        for player in self.players:
            player.update_player()
            
            
            

################################################################################
## TEST
################################################################################

if __name__ == "__main__":  
    
    #pawn = Simp_unit() 
    pawn_group = Simp_unit_group()
    for unit in pawn_group.group_list:
        print("unit loc:", unit.loc)
    #test loop to give coords to units
    for unit in pawn_group.group_list:  
        unit.targ_tile = (25,25)
        unit.active = True
    #test loop to move units    
        unit.move_unit()
    for unit in pawn_group.group_list: # check locations again to see if moved
        print("unit loc:", unit.loc)     
        
        
        
    # test player groups - test works #
    all_players = P_u_group() #                                                 - These lines are the lines to call/create the players & units for a game
    
    all_players.print_all_player_units() # Test to print all player units to shell - works
    
    all_players.update_players() # Test of update logic path
    
    
    print()
    print("-- TEST DONE --")
    print()
    pygame.quit()
    sys.exit()