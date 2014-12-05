################################################################################
## melee
################################################################################
""" determines battle results """

import random
import unit_simp, params

################################################################################

side_a = []
side_b = []
melee_groups = [side_a, side_b]

################################################################################

def create_melee_groups(grid, player_grp, ttl_players):
    """ sorts through unit positions and creates melee_groups 
        grid: grid_map name
        player_grp: player_group name
    """
    for player_no in range(0,ttl_players):
        for player in player_grp.players:
            for unit_group in player.units:
                for unit in unit_group.group_list:
                    if unit.state: # if unit is alive:
                        for check_player in range(0, len(player_grp.players)):
                            if check_player > player_no:
                                check_nearby_units(grid, unit)
                            
    print("melee_groups:", melee_groups)
    
def check_nearby_units(grid, unit):
    """ see if there is anything in nearby tiles and add to combat list """
    for x_check in range(unit.loc[0]-1,3):
        if x_check > -1 and x_check < int(params.FIELD_RECT[2]/params.TILE_SIZE):
            for y_check in range(unit.loc[1]-1,3):
                if y_check > -1 and y_check < int(params.FIELD_RECT[3]/params.TILE_SIZE):
                    if grid.matrix[x_check][y_check].contents != [] or grid.matrix[x_check][y_check].contents != unit:
                        side_a = unit
                        side_b = grid.matrix[x_check][y_check].contents
                        melee_groups.append([side_a, side_b])