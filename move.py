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
        - currently activated by button event
        unit: unit to be moved, can get current location and target location
        grid: grid_map name to update Tile_grid.matrix[x,y] contents
    """
    for player in player_grp.players:
        for unit_group in player.units:
            for unit in unit_group.group_list:
                if unit.loc != unit.targ_tile:
                    unit.txt_status = "Moving"
                    print("unit", unit.unit_no, ": loc, targ_tile", unit.loc, unit.targ_tile)
                    next_loc = move_to_target(grid, unit)
                    if is_grid_passable(grid, next_loc):
                        #grid.matrix[unit.loc[0]][unit.loc[1]].remove(unit)
                        unit.loc = next_loc
                        #grid.matrix[next_loc[0]][next_loc[1]].append(unit)
                else:
                    print("Unit Arrived", "unit", unit.unit_no, ": loc, targ_tile", unit.loc, unit.targ_tile)
                    unit.txt_status = "Arrived"
        
################################################################################

def move_to_target(grid, unit):
    """  Generates new position based upon target location and current position.
         unit: unit to be moved, can get current location and target location
         NOTE: don't forget to update grid contents at some point & verify new position is legal
         CONSIDER: if pass grid_map variable name, can update Tile_grid.matrix[x,y] contents
    """
    new_x = unit.loc[0]
    new_y = unit.loc[1]
    if new_x > unit.targ_tile[0]: new_x -= 1
    elif new_x < unit.targ_tile[0]: new_x += 1
    if new_y > unit.targ_tile[1]: new_y -= 1
    elif new_y < unit.targ_tile[1]: new_y += 1   
    next_loc = (new_x, new_y)
    if is_grid_empty(grid, next_loc, unit): update_grid_pos(grid, unit, next_loc)
    return(next_loc)

def update_grid_pos(grid, unit, next_loc):
    """ place unit position into matrix and remove from previous matrix record """ # NOTE: check to see if spot taken first
    tile = grid.matrix[unit.loc[0]][unit.loc[1]]
    if unit in tile.contents:
        tile.contents.remove(unit)
    tile.contents.append(unit)
    
def is_grid_empty(grid, next_loc, unit):
    """ returns True if next_loc is populated """
    tile = grid.matrix[unit.loc[0]][unit.loc[1]]
    new_tile = grid.matrix[unit.loc[0]][unit.loc[1]]
    if new_tile.contents == [] or new_tile.contents == unit or new_tile == unit.loc:
        print("unit", unit.unit_no, ": tile empty")
        return(True)
    else:
        print("unit", unit.unit_no, ": space not free, waiting until later to move")
        for element in new_tile.contents:
            print("unit", unit.unit_no, ": space contains:", element.loc, element.unit_no)
        return(False)
    
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