################################################################################
## items
################################################################################

import pygame
from pygame.sprite import Sprite

################################################################################

inv_wpn = {  "sword": (1, 1, 1, 1, 0, False), 
             "hammer": (2, 1, 1, 1, 0, False)}
""" weight, cost, attack_bonus, damage_cap, init_bonus, two_hand """

#library - try #1
wpn_lib = { "sword": {  "name": "generic sword", 
                        "weight": 1,
                        "value": 1,
                        "attack_bonus": 1,
                        "damage_cap": 1,
                        "init_bonus": 1,
                        "two_hand": False },
            "hammer": { "name": "hammer",
                        "weight": 2,
                        "value": 1,
                        "attack_bonus": 1,
                        "damage_cap": 1,
                        "init_bonus": -1,
                        "two_hand": False } 
            }


################################################################################

class Items(Sprite):
    """ inventory items - equippable """
    def __init__(self):
        Sprite.__init__(self)
        self.equipped = False
        self.condition = 100 # percentage indicating condition of item
        self.data = {}
        
    def condition_check(self):
        print("This item is at " + str(self.condition) + "% capacity.")
        if self.condition < 0:
            print("This item is ruined - get another.")
        elif self.condition < 55:
            print("This item is damaged and at decreased capacity.")
        elif self.condition < 65:
            print("This item is in need of upkeep, but still servicable.")
        elif self.condition < 85:
            print("This item is in good shape, but needs maintenance.")
        elif self.condition < 95:
            print("This item is in excellent shape.")
        elif self.condition <= 100:
            print("This item is in mint condition.")
        else:
            print("This item is better quality than normal.")
        
class Weapon(Items):
    """ child class of Items for items with primarily offensive use """
    def __init__(self, wpn_type = "sword"):
        Items.__init__(self)
        self.wpn_type = wpn_type
        
        self.name = wpn_type.get[name]
        
        print("I'm making a " + self.wpn_type + ". It goes by the name " + self.name)
        
        #"name": "sword",
        #"weight": 1,
        #"value": 1,
        #"attack_bonus": 1,
        #"damage_cap": 1,
        #"init_bonus": 1,
        #"two_hand": False }        

        
        
class Armor(Items):
    """ child class of Items for items with primarily defensive use """
    def __init__(self):
        Items.__init__(self)        
        
class Container(Items):
    """ child class of Items for holding other items """
    def __init__(self):
        Items.__init__(self)
        self.contents = []
        self.slots = 8 # limitation on qty of items a container can carry
        self.weight_cap = 10 * self.slots # limitation on weight a container can carry
        
################################################################################
## Unit Testing                                                               ##
################################################################################
if __name__ == "__main__":
    
    #try to read from sword library
    print("sword", wpn_lib["sword"])
    
    #read embedded info from library
    print("sword name:", wpn_lib["sword"]["name"])
    print("hammer name:", wpn_lib["hammer"]["name"])
    
    look_for = "weight"
    equipped_weapon = "hammer"
    print("hammer weight:", wpn_lib[equipped_weapon][look_for])

     
    
    
    #try to make a sword
    
    
    print()
    print("Done.")