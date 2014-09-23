################################################################################
## recruiting                                                             
################################################################################
import pygame
from random import randint, choice
import messages, units, dice

################################################################################

class Recruit(object):
    """ methods for recruiting new units or unit groups """
    def __init__(self):
        dummy = False

    def char_make(self, unit):
        var_pts = 6
        print("You have", var_pts, "to apply.")
        stat_check = False # flag to see if var_pts are all used
        if stat_check == False:
            stat_adj = [0,0,0,0]
            adj_ttl = 0
            for stat in range(0,4):
                print("stat:", stat)
                stat_adj[stat] = int(input("Points to apply to " + str(units.STAT_NAMES[stat]) + ":"))
                adj_ttl += stat_adj[stat]
                print("You adjusted by", stat_adj[stat])
            if var_pts == adj_ttl:
                stat_check = True
                unit.attack += stat_adj[0]
                unit.initiative += stat_adj[1]
                unit.defense += stat_adj[2]
                unit.speed += stat_adj[3]              
                print("Unit stats adjusted.")
                print("New stats: ")
                unit.print_unit()
                print()
            else:
                print("Error: stats don't add up. Redo.")
                print()
                self.char_make(unit)
            
    def group_make(self, pawn_group):
        for unit in pawn_group.group_list:
            self.char_make(unit)
        
class Training(object):
    """ methods for Academy & Arena skill & ability training """
    def __init__(self):
        dummy = False
        
    def start_out(self, unit):
        print()
        print(choice(messages.enter_school))
        school_name = choice(messages.school)
        unit.story["school"] = school_name
        school_studies = choice(messages.skills)
        
        old_studies = unit.skills.get(school_studies)
        self.update_skill(unit, school_studies, 1)

        print("You have been accepted by " + str(unit.story["school"]) + ".")
        print("There you studied " + str(school_studies) + ".")
        print()

    def academy(self, unit):
        #print("So you want to get more school.")
        print(choice(messages.enter_school_again))
        
        school_name = choice(messages.school)
        unit.story["school"] += ", " + school_name
        print("This time you attended " + str(school_name) + ".")
        school_studies = choice(messages.skills)
        print("You studied " + str(school_studies) + ".")
        old_studies = unit.skills.get(school_studies)
        
        if self.study_success(unit, school_studies):
            bonus = 1
        else:
            bonus = (randint(0,3) +1) * .25
            if bonus > .75:
                bonus = 1
                print("The teacher decided to let you slip by.")
            print(" reduced bonus:", bonus)
            
        self.update_skill(unit, school_studies, bonus)
        print()
        
    def update_skill(self, unit, skill, bonus):
        old_studies = unit.skills.get(skill)
        if not old_studies:
            unit.skills[skill] = bonus
        else: 
            unit.skills[skill] += bonus        
    
    def study_success(self, unit, skill):
        current_lvl = unit.skills.get(skill)
        difficulty = 0
        if current_lvl:
            difficulty = unit.skills.get(skill) + 1 * 10
        else: 
            difficuly = 1 * 10
        print("difficulty:", difficulty)
        pass_check = randint(0,100) + 1 - difficulty
        print("pass_check:", pass_check)
        if pass_check > 0:
            print("You passed!")
            return(True)
        else:
            print("You did not pass!")
            return(False)

    def ability(self):
        dummy = False
        
        

################################################################################
## Unit Testing                                                               
################################################################################

if __name__ == "__main__":   
    
    pygame.init()
    import params    
    pawn_group = units.Unit_group()    
    recruit = Recruit()
    training = Training()
    reader = messages.Reader()
    
    ##**************************************************************************
    
    ## Test: make a group of units and adjust starting stats individually ------WORKS
    #pawn_group.add_unit("unit")
    #pawn_group.add_unit("unit")
    #pawn_group.print_group_units()
    #print("length of group_list:", len(pawn_group.group_list))
    #print("unit test of a stat:", pawn_group.group_list[0].attack)
    #recruit.group_make(pawn_group)
    
    ## Test: make an individual unit and send to school ------------------------WORKS
    my_unit = units.Unit()
    training.start_out(my_unit)
    school_sem = int(input("Times back to school:"))
    for times in range(0, school_sem):
        training.academy(my_unit)
    reader.prt_unit_history(my_unit)
    
    
    
    print()
    print("-- Done --")