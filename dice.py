from random import randint

# ------------------------------------------------------------------------------

# Defaults: diceroll(  die_no = 1,
#                      die_type = 10
#                      die_weight = 0
#                      die_tries = 1)

# Defaults: best_roll(  best_of = 2)

# ------------------------------------------------------------------------------

class Dice(object):
    """ dice roll handler """
    def __init__(self):
        dummy = False
    
    def diceroll(self, die_no = 1, die_type = 10, die_weight = 0, die_tries = 1):
        ttl_roll = 0
        for tries in range(0, die_tries):
            #print("try #:", tries)
            for roll in range(0, die_no):
                a_roll = randint(1, die_type + 1) + die_weight
                if a_roll > die_type:
                    a_roll = die_type
                ttl_roll += a_roll
                #print("roll: ", a_roll, "   subtotal:", ttl_roll)
            #print("total roll:", ttl_roll)
        ttl_roll = int(ttl_roll/die_tries)
        #print("total after all tries:", ttl_roll)
        #print()
        return(ttl_roll)  
    
    def best_roll(self, die_no = 1, die_type = 10, die_weight = 0, die_tries = 1, best_of = 2):
        roll_a = self.diceroll(die_no, die_type, die_weight, die_tries)
        #print("roll 1: ", roll_a)
        for roll in range(0, best_of):
            roll_b = self.diceroll(die_no, die_type, die_weight, die_tries)
            #print("next roll:", roll_b, "   (roll number:", roll, ")")
            if roll_b > roll_a:
                roll_a = roll_b
        return(roll_a)
    
    
################################################################################
## Unit Testing - Combat                                                      ##
################################################################################
if __name__ == "__main__":  
        
    print("diceroller test")
    print()
    dice = Dice()
    
    print("default die roll:", dice.diceroll())    
    print()
    print("2d10:", dice.diceroll(die_no = 2))
    print()
    print("2d10, weight = 1:", dice.diceroll(die_no = 2, die_weight = 1))
    print()     
    print("3d4, tries = 3:", dice.diceroll(  die_no = 3, 
                                             die_type = 4, 
                                             die_weight = 0, 
                                             die_tries = 3)) 
    print()
    print("3d6, best of 2: ", dice.best_roll(  die_no = 3, 
                                               die_type = 6,
                                               best_of = 2))
    print()    
    print("3d6, best of 10: ", dice.best_roll(  die_no = 3, 
                                               die_type = 6,
                                               best_of = 10))  
    print()    
    response = input("Roll your own? ")
    while response == "y":
        dno = int(input("# of dice to roll? "))
        dtype = int(input("# of sides on die? "))
        dweight = int(input("# to tweek die weight - use sparingly: "))
        dtries = int(input("times to try each roll (increases chances of getting an average score on roll: "))
        print("Result:", dice.diceroll(  die_no = dno, 
                                         die_type = dtype, 
                                         die_weight = dweight, 
                                         die_tries = dtries))
        print()
        response = input("Roll another set? ")
    else:
        print("bye bye")
    