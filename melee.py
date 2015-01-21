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
        for melee_pair in self.melee_groups: self.do_melee(melee_pair)

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

    def do_melee(self, melee_pair):
        """ process single round of melee of melee_groups pairs """
        print("melee_pair from do_melee", melee_pair)
        self.prep_melee(melee_pair)
        
        # NOTE: remove winning unit from inactive status so can move again
        # NOTE: set defeated units to dead so can't move or do anything & update image file
        # NOTE: only let unit swing the number of attack swings they have - after that they can only defend swing        
        for unit in melee_pair: self.reset_unit_markers(unit)

        
    def reset_unit_markers(self, unit):
        """ resets unit indicators after each melee round """
        unit.in_melee = False
        print("unit markers reset")
        
    def prep_melee(self, melee_pair):
        """ set up initiative & sides variables """
        side_1 = melee_pair[0]
        side_2 = melee_pair[1]
        print("melee pairs:", melee_pair, side_1, side_2)
        
        for thing in side_1: 
            print("side_1 thing", thing)
        print("melee_pair len:", len(melee_pair))

        
        # determine initiative
        initiative_roll_a = initiative_roll(side_1)
        initiative_roll_b = initiative_roll(side_2)
        print("innitiative rolls:", initiative_roll_a, initiative_roll_b)
        
        if initiative_roll_a > initiative_roll_b:
            print("side a opponent receives initiative")
            attack_round_pair(  melee_pair, 
                                attacker = side_1, 
                                #attacker_group = side1_team, 
                                defender = side_2, 
                                #defender_group = side2_team,
                                hero_is_attacker = True)
            
        elif initiative_roll_b > initiative_roll_a:
            print("side b opponent receives initiative")
            attack_round_pair(  melee_pair, 
                                attacker = side_2, 
                                #attacker_group = side2_team, 
                                defender = side_1, 
                                #defender_group = side1_team, 
                                hero_is_attacker = False)
        else:
            print("no one prevails but peace... life finds a way...")  
            
    #def attack_round_pair(melee_pair, attacker, attacker_group, defender, defender_group, hero_is_attacker):   
    def attack_round_pair(melee_pair, attacker, defender, hero_is_attacker):  
        attacker_roll_a = attacker_roll(attacker) # determine attack bonus & roll
        defender_roll_b = defender_roll(defender) # determine defense bonus & roll
        attacker.stats["swings"] +=1
        print("attack & defense rolls:", attacker_roll_a, defender_roll_b)
        # determine winner/loser and consequences
        if attacker_roll_a > defender_roll_b: # attacker wins
            print("attacker is victorious")
            attacker_group.wins += 1
            attacker.stats["melee_won"] += 1
            attacker.in_melee = False
            #units.MELEE_LIST.remove(melee_pair) 
            #if defender in defender_group.group_list: # verify that defender has not already been removed
                #defender_group.group_list.remove(defender)
            if hero_is_attacker:
                messages.HERO_WINS += 1
            else:
                messages.ENEMY_WINS += 1
                
        else: #defender wins tie
            print("defender stops the attack and counters")
            # do counter attack
            attacker_roll_a = attacker_roll(defender)
            defender_roll_b = defender_roll(attacker)
            defender.stats["swings"] +=1    


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