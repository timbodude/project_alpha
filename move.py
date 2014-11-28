################################################################################
## move
################################################################################
""" This method takes handles movement-related methods and utilities for units
"""
import pygame, os
import unit_simp

################################################################################

def movement(grid, player_grp):
    """ overall calculations for unit movement phase
        unit: unit to be moved, can get current location and target location
        grid: grid_map name to update Tile_grid.matrix[x,y] contents
    """
    for player in player_grp.players:
        for unit_group in player.units:
            for unit in unit_group.group_list:
                next_loc = move_to_target(unit)
                if is_grid_passable(grid, next_loc):
                    #grid.matrix[unit.loc[0]][unit.loc[1]].remove(unit)
                    unit.loc = next_loc
                    #grid.matrix[next_loc[0]][next_loc[1]].append(unit)
        
################################################################################

def move_to_target(unit):
    """  Generates new position based upon target location and current position.
         unit: unit to be moved, can get current location and target location
         NOTE: don't forget to update grid contents at some point & verify new position is legal
         CONSIDER: if pass grid_map variable name, can update Tile_grid.matrix[x,y] contents
    """
    next_loc = [0,0]
    for x in range(0,2):
        if unit.loc[x] > unit.targ_tile[x]:
            next_loc[x] = unit.loc[x] - 1
        elif unit.loc[x] < unit.targ_tile[x]:
            next_loc[x] = unit.loc[x] + 1
        else:
            next_loc[x]= unit.loc[x]
    return(next_loc)

def is_grid_passable(grid, next_loc):
    """ returns True if next_location is passable 
        grid: name of Tile_grid
        next_loc: target location
    """
    return(True)

################################################################################
## TEST
################################################################################

if __name__ == "__main__":  
    
    screen = pygame.display.set_mode((100, 100), 0, 32) # create screen area for tiles
    
    # TEST move_to_target                                                       - WORKS
    unit_group = unit_simp.Simp_unit_group(screen, total = 3)
    for unit in unit_group.group_list:
        unit.targ_tile = [10,10]
        print(unit.loc, unit.targ_tile, move_to_target(unit))
    
    
    
    
    
    print("done")
    pygame.quit()