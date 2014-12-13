################################################################################
## melee
################################################################################
""" determines battle results """

from random import randint
import unit_simp, params, dice, messages

################################################################################

dice = dice.Dice()

################################################################################

class Melee_engine():
    """ combat handler 
        grid: grid_map name
        player_grp: player_group name
        ttl_players: total number of player
    """
    def __init__(self, grid, player_grp, ttl_players):
        self.melee_groups = []
        self.grid = grid
        self.player_grp = player_grp
        self.ttl_players = ttl_players

    def update_melee(self):
        """ primary processes """
        self.create_melee_groups()
        for melee_pair in self.melee_groups: self.do_melee()

    def create_melee_groups(self):
        """ sorts through unit positions and creates melee_groups 
            grid: grid_map name
            player_grp: player_group name
        """
        self.melee_groups = []  # reset every round
                    
        for player_units in self.player_grp.players[0].units:
            for player_unit in player_units.group_list:
                if player_unit.state:
                    for enemy_player_number in range(1, self.ttl_players):
                        for enemy_units in self.player_grp.players[enemy_player_number].units:
                            for enemy_unit in enemy_units.group_list:
                                #print("player_unit", player_unit.loc, "  v.s. enemy_unit", enemy_unit.loc)
                                if enemy_unit.state:
                                    if player_unit.loc[0] >= enemy_unit.loc[0] - 1 and player_unit.loc[0] <= enemy_unit.loc[0] + 1 :
                                        if player_unit.loc[1] >= enemy_unit.loc[1] - 1 and player_unit.loc[1] <= enemy_unit.loc[1] + 1:
                                            #print("player_unit in range of enemy", player_unit.loc, enemy_unit.loc)
                                            side_a = [player_unit]
                                            side_b = [enemy_unit]
                                            self.melee_groups.append([side_a, side_b])
                                            player_unit.in_melee = True
                                            enemy_unit.in_melee = True                        

    def do_melee(self):
        """ process single round of melee of melee_groups pairs """
        print("melee_groups from do_melee", self.melee_groups)

        # NOTE: remove winning unit from inactive status so can move again
        # NOTE: set defeated units to dead so can't move or do anything & update image file



############################################################################
## melee formulas
############################################################################
    
def attacker_roll(unit):
    roll = dice.diceroll(die_tries = 3)
    bonus = (unit.attack * unit.gov_attack) + (unit.speed/2*unit.gov_speed)
    roll += bonus
    return(roll)
    
def defender_roll(unit):
    #roll = ((randint(0,10) + randint(0,10) + randint(0,10))/3)
    roll = dice.diceroll(die_tries = 3)
    bonus = (unit.defense * unit.gov_defense) + (unit.speed/2 * unit.gov_speed)
    roll += bonus
    return(roll)

def initiative_roll(unit):
    roll = dice.diceroll()
    bonus = (unit.initiative * unit.gov_initiative) + (unit.speed/2* unit.gov_initiative)
    roll += bonus
    return(roll)