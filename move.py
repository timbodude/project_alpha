################################################################################
## move
################################################################################
""" This method takes handles movement-related methods and utilities for units
"""
import pygame, os
import unit_simp, melee

################################################################################

def movement(grid, player_grp):
    """ overall calculations for unit movement phase
        - currently activated by button event
        unit: unit to be moved, can get current location and target location
        grid: grid_map name to update Tile_grid.matrix[x,y] contents
    """
    for player in player_grp.players:
        #print("**************total_number_of_players", len(player_grp.players))
        for unit_group in player.units:
            for unit in unit_group.group_list:
                if unit.loc != unit.targ_tile and not unit.in_melee:
                    unit.txt_status = "Moving"
                    #print("unit", unit.unit_no, ": loc, targ_tile", unit.loc, unit.targ_tile)
                    next_loc = move_to_target(grid, unit)
                    if is_grid_passable(grid, next_loc):
                        unit.loc = next_loc
                else:
                    #print("Unit Arrived", "unit", unit.unit_no, ": loc, targ_tile", unit.loc, unit.targ_tile)
                    unit.txt_status = "Arrived"
        
################################################################################

def move_to_target(grid, unit):
    """  Generates new position based upon target location and current position.
         unit: unit to be moved, can get current location and target location
         NOTE: don't forget to update grid contents at some point & verify new position is legal
         CONSIDER: if pass grid_map variable name, can update Tile_grid.matrix[x,y] contents
    """
    old_x = unit.loc[0]
    old_y = unit.loc[1]
    new_x = unit.loc[0]
    new_y = unit.loc[1]
    if new_x > unit.targ_tile[0]: new_x -= 1
    elif new_x < unit.targ_tile[0]: new_x += 1
    if new_y > unit.targ_tile[1]: new_y -= 1
    elif new_y < unit.targ_tile[1]: new_y += 1   
    next_loc = (new_x, new_y)
    if is_grid_empty(grid, next_loc, unit): 
        update_grid_pos(grid, unit, next_loc, old_x, old_y)
    return(next_loc)

def update_grid_pos(grid, unit, next_loc, old_x, old_y):
    """ place unit position into matrix and remove from previous matrix record """ # NOTE: check to see if spot taken first
    tile = grid.matrix[unit.loc[0]][unit.loc[1]]
    if unit in grid.matrix[old_x][old_y].contents: 
        grid.matrix[old_x][old_y].contents.remove(unit)
    tile.contents.append(unit)
    
def is_grid_empty(grid, next_loc, unit):
    """ returns True if next_loc is populated """
    tile = grid.matrix[unit.loc[0]][unit.loc[1]]
    new_tile = grid.matrix[unit.loc[0]][unit.loc[1]]
    if new_tile.contents == [] or new_tile.contents == unit or new_tile == unit.loc:
        #print("unit", unit.unit_no, ": tile empty")
        dummy = False
        return(True)
    else:
        #print("unit", unit.unit_no, ": space not free, waiting until later to move")
        dummy = False        
        for element in new_tile.contents:
            #print("unit", unit.unit_no, ": space contains:", element.loc, element.unit_no)
            dummy = False
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
    

    
    
    
    
    
    print("done")
    pygame.quit()