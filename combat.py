################################################################################
## combat
################################################################################

import units
import dice
from random import randint
import messages

dice = dice.Dice()

################################################################################

# ------------------------------------------------------------------------------
# Add Stat Governor - A = .55 | I = .91 | D = .95 | S = .79
# ------------------------------------------------------------------------------

def melee(melee_pair):
    """ computes battle between 2 units """
    side1 = melee_pair[0]
    side1_team = melee_pair[1]
    side2 = melee_pair[2]
    side2_team = melee_pair[3]
    print("melee pairs:", side1, side2)
    # determine initiative
    initiative_roll_a = initiative_roll(side1)
    initiative_roll_b = initiative_roll(side2)
    print("innitiative rolls:", initiative_roll_a, initiative_roll_b)
    
    if initiative_roll_a > initiative_roll_b:
        print("side a opponent receives initiative")
        attack_round_pair(  melee_pair, 
                            attacker = side1, 
                            attacker_group = side1_team, 
                            defender = side2, 
                            defender_group = side2_team,
                            hero_is_attacker = True)
        
    elif initiative_roll_b > initiative_roll_a:
        print("side b opponent receives initiative")
        attack_round_pair(  melee_pair, 
                            attacker = side2, 
                            attacker_group = side2_team, 
                            defender = side1, 
                            defender_group = side1_team, 
                            hero_is_attacker = False)
    else:
        print("no one prevails but peace... life finds a way...")

            
def attack_round_pair(melee_pair, attacker, attacker_group, defender, defender_group, hero_is_attacker):   
    attacker_roll_a = attacker_roll(attacker) # determine attack bonus & roll
    defender_roll_b = defender_roll(defender) # determine defense bonus & roll
    attacker.stats["swings"] +=1
    print("attack & defense rolls:", attacker_roll_a, defender_roll_b)
    # determine winner/loser and consequences
    if attacker_roll_a > defender_roll_b: # attacker wins
        print("attacker is victorious")
        attacker_group.wins += 1
        attacker.stats["melee_won"] += 1
        attacker.in_combat = False
        units.MELEE_LIST.remove(melee_pair) 
        if defender in defender_group.group_list: # verify that defender has not already been removed
            defender_group.group_list.remove(defender)
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
        units.MELEE_LIST.remove(melee_pair)
        if attacker_roll_a > defender_roll_b: # counterattack wins
            print("defender's counterattack overcomes attacker")
            defender_group.wins += 1
            #attacker_group.removal_list.append(attacker)
            #attacker_group.remove_unit(attacker)
            if attacker in attacker_group.group_list: # verify that attacker has not already been removed
                attacker_group.group_list.remove(attacker)            
            defender.stats["melee_won"] += 1
            defender.in_combat = False
            if not hero_is_attacker:
                messages.ENEMY_WINS += 1
            else:
                messages.HERO_WINS += 1
                
        else: # defender vs counterattack wins - including tie
            print("counterattack failed - they live to fight again")
            attacker.in_combat = False
            defender.in_combat = False
            
    #print() 
    print("attacker_wins:", attacker_group.wins, "   defender wins:", defender_group.wins)
    
    #print("Hero:", win_score.hero_wins, "  Enemy:", win_score.enemy_wins)
    #print()

############################################################################
## combat formulas
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


