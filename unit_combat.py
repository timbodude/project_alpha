import units
import dice
from random import randint

dice = dice.Dice()

# ------------------------------------------------------------------------------
# Add Stat Governor - A = .55 | I = .91 | D = .95 | S = .79
# ------------------------------------------------------------------------------

class Do_combat(object):
    """ determine a round of combat """
    def __init__(self, side1, side2):
        print("initiating combat...")
        self.side1 = side1
        self.side2 = side2
        
    def do_group_melee(self):
        melee_pairs = len(self.side1.group_list)
        print("melee pairs:", melee_pairs)
        for melee in range(0,len(self.side1.group_list)): 
            # determine initiative
            initiative_roll_a = self.initiative_roll(self.side1.group_list[melee])
            initiative_roll_b = self.initiative_roll(self.side2.group_list[melee])
            print("innitiative rolls:", initiative_roll_a, initiative_roll_b)
            
            if initiative_roll_a > initiative_roll_b:
                print("side a opponent receives initiative")
                self.attack_round(   attacker = self.side1.group_list[melee], 
                                     attacker_group = self.side1,
                                     attacker_no = melee,
                                     defender = self.side2.group_list[melee],
                                     defender_group = self.side2,
                                     defender_no = melee)
                
            elif initiative_roll_b > initiative_roll_a:
                print("side b opponent receives initiative")
                self.attack_round(   attacker = self.side2.group_list[melee], 
                                     attacker_group = self.side2,
                                     attacker_no = melee,
                                     defender = self.side1.group_list[melee],
                                     defender_group = self.side1,
                                     defender_no = melee)
            else:
                print("no one prevails but peace... life finds a way...")
        # remove pair
        self.side1.dump_removal_list()
        self.side2.dump_removal_list()
        
    def do_pair_melee(self, melee_pair):
        """ computes battle between 2 units """
        self.side1 = melee_pair[0]
        self.side1_team = melee_pair[1]
        self.side2 = melee_pair[2]
        self.side2_team = melee_pair[3]
        print("melee pairs:", self.side1, self.side2)
        # determine initiative
        initiative_roll_a = self.initiative_roll(self.side1)
        initiative_roll_b = self.initiative_roll(self.side2)
        print("innitiative rolls:", initiative_roll_a, initiative_roll_b)
        
        if initiative_roll_a > initiative_roll_b:
            print("side a opponent receives initiative")
            self.attack_round_pair(  melee_pair, 
                                     attacker = self.side1, 
                                     attacker_group = self.side1_team, 
                                     defender = self.side2, 
                                     defender_group = self.side2_team)
            
        elif initiative_roll_b > initiative_roll_a:
            print("side b opponent receives initiative")
            self.attack_round_pair( melee_pair,
                                    attacker = self.side2, 
                                    attacker_group = self.side2_team,
                                    defender = self.side1_team,
                                    defender_group = self.side1)
        else:
            print("no one prevails but peace... life finds a way...")
            
    def attack_round_pair(melee_pair, self, attacker, attacker_group, defender, defender_group):   
        attacker_roll_a = self.attacker_roll(attacker) # determine attack bonus & roll
        defender_roll_b = self.defender_roll(defender) # determine defense bonus & roll
        print("attack & defense rolls:", attacker_roll_a, defender_roll_b)
        # determine winner/loser and consequences
        if attacker_roll_a > defender_roll_b: # attacker wins
            print("attacker is victorious")
            attacker_group.wins += 1
            attacker.in_combat = False
            units.MELEE_LIST.remove(melee_pair) 
            defender_group.remove_unit(defender)
        else: #defender wins tie
            print("defender stops the attack and counters")
            # do counter attack
            attacker_roll_a = self.attacker_roll(defender)
            defender_roll_b = self.defender_roll(attacker)
            units.MELEE_LIST.remove(melee_pair)
            if attacker_roll_a > defender_roll_b: # counterattack wins
                print("defender's counterattack overcomes attacker")
                defender_group.wins += 1
                #attacker_group.removal_list.append(attacker)
                attacker_group.remove_unit(attacker)
                defender.in_combat = False
            else: # defender vs counterattack wins - including tie
                print("counterattack failed - they live to fight again")
        print()            
            
    def attack_round(self, attacker, attacker_group, attacker_no, defender, defender_group, defender_no):   
        attacker_roll_a = self.attacker_roll(attacker) # determine attack bonus & roll
        defender_roll_b = self.defender_roll(defender) # determine defense bonus & roll
        print("attack & defense rolls:", attacker_roll_a, defender_roll_b)
        # determine winner/loser and consequences
        if attacker_roll_a > defender_roll_b: # attacker wins
            print("attacker is victorious")
            attacker_group.wins += 1
            attacker_group.removal_list.append(attacker)
            defender_group.removal_list.append(defender)
        else: #defender wins tie
            print("defender stops the attack and counters")
            # do counter attack
            attacker_roll_a = self.attacker_roll(defender)
            defender_roll_b = self.defender_roll(attacker)
            if attacker_roll_a > defender_roll_b: # counterattack wins
                print("defender's counterattack overcomes attacker")
                defender_group.wins += 1
                attacker_group.removal_list.append(attacker)
                defender_group.removal_list.append(defender)
            else: # defender vs counterattack wins - including tie
                print("counterattack failed - they live to fight again")
        print()

    ############################################################################
    ## combat formulas
    ############################################################################
    
    def attacker_roll(self, unit):
        roll = dice.diceroll(die_tries = 3)
        bonus = (unit.attack * unit.gov_attack) + (unit.speed/2*unit.gov_speed)
        roll += bonus
        return(roll)
    
    def defender_roll(self, unit):
        #roll = ((randint(0,10) + randint(0,10) + randint(0,10))/3)
        roll = dice.diceroll(die_tries = 3)
        bonus = (unit.defense * unit.gov_defense) + (unit.speed/2 * unit.gov_speed)
        roll += bonus
        return(roll)
    
    def initiative_roll(self, unit):
        roll = dice.diceroll()
        bonus = (unit.initiative * unit.gov_initiative) + (unit.speed/2* unit.gov_initiative)
        roll += bonus
        return(roll)
    
# ------------------------------------------------------------------------------


################################################################################
## Unit Testing - Combat                                                      ##
################################################################################
if __name__ == "__main__":  
    
    ttl_groups = []
    ttl_groups.append(units.Unit_group())
    ttl_groups.append(units.Unit_group())
    battle = Do_combat(ttl_groups[0], ttl_groups[1])  
    dice = dice.Dice()
       
    #Testing combat ###########################################################
    
    ttl_units = int(input("Units per side?: "))
    
    print("building armies")
    
    for unit_no in range(0, ttl_units):
        ttl_groups[0].add_unit()
        ttl_groups[1].add_unit()
    print("army sizes (1 and 2):", len(ttl_groups[0].group_list), len(ttl_groups[0].group_list))
    print()
    
    answer = input("Adjust stats? (y/n):")
    if answer == "y":
        for team_no in range(0, 2):
            print()
            print("Input Team", team_no, "New Stats")
            attack = int(input("attack: "))
            initiative = int(input("initiative: "))
            defense = int(input("defense: "))
            speed = int(input("speed: "))            
            for unit in ttl_groups[team_no].group_list:
                unit.attack = attack
                unit.initiative = initiative
                unit.defense = defense
                unit.speed = speed
        print()
        print("Units adjusted")
        print()

    if len(ttl_groups[0].group_list) < 1 and len(ttl_groups[1].group_list) < 1:
        battle_over_flag = True
    else:
        battle_over_flag = False
        
    round_no = 1
    while battle_over_flag == False:
        print("round #:", round_no)
        print()
        battle.do_group_melee()
        round_no += 1
        print()
        
        if len(ttl_groups[0].group_list) < 1 or len(ttl_groups[1].group_list) < 1 or round_no > 10001:
            battle_over_flag = True
    
    print("The score was" , ttl_groups[0].wins, ttl_groups[1].wins)
    print(  "Percent of wins: " +
            str(int(100*(ttl_groups[0].wins/(ttl_groups[0].wins + ttl_groups[1].wins)))) + 
            "% vs " +
            str(int(100*(ttl_groups[1].wins/(ttl_groups[0].wins + ttl_groups[1].wins)))) +
            "%")
    #print("lengths: ", len(ttl_groups[0].group_list), len(ttl_groups[1].group_list))
    print("Thanks")     
