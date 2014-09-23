import os, sys
import math
import pygame
from pygame import Color
from pygame.sprite import Sprite
from images_lib import Image_lib
from random import randint, choice
from vec2d import vec2d
import params
import unit_combat
import obstacle
import messages
import grid_map
#from obstacle import OBSTACLE_LIST

# ------------------------------------------------------------------------------
# Libraries & Lists

CREEP_FILENAMES = ["bluecreep.png", "pinkcreep.png", "graycreep.png"]
N_CREEPS = 5

STAT_NAMES = ["Attack", "Initiative", "Defense", "Speed"]

ENEMY_LIST = [] # list of enemy units
HERO_LIST = [] # list of hero units
MELEE_LIST = [] # list of unit pairs in melee
ALL_UNIT_GROUPS = [] # list of all unit groups for update purposes

ALL_OBSTACLES_GROUPS = []


################################################################################

class Unit(Sprite):
    """ generic class for all unit types """ # NOTE: calls to class must add screen
    def __init__(self, screen, is_hero = True, vector = (0,0)): # NEED: unit fighting image, unit dying image, unit stunned image
        Sprite.__init__(self)
        self.attack = 1 # unit stat for offensive combat capability
        self.initiative = 1 # unit stat for first swing advantage
        self.defense = 1 # unit stat for defensive combat capability
        self.speed = 2 # unit stat for dexterity advantage
        self.health = 15 # unit stat for current health points
        self.max_health = 15 # unit stat for max health
        self.gov_attack = 1.0 # governor to temp adjust a unit stat
        self.gov_initiative = 1.0 # governor to temp adjust a unit stat
        self.gov_defense = 1.0 # governor to temp adjust a unit stat
        self.gov_speed = 1.0 # governor to temp adjust a unit stat
        self.story = {} # library of character history
        self.skills = {} # library of studies
        self.inventory = {} # library of unit's stuff
        self.in_combat = False # bool to show if unit should be in melee or free to move
        self.move_form = 1 # 0: halt = 0 movement rate, 0.5: walk = half movement, 1: run = full movement ## now set to extra fast for testing
        self.stats = {  "melee_won": 0,
                        "swings": 0}
        self.targets = [(0,0)]
        self.names = {} # library to hold names: name = primary name, nic = nic-names given
        self.los = 500 # line-of-site for attacking enemy in combat (in pixels)
        self.turn_to_opp = 1
        self.wander = True # True = move in random direction / False = move in continual direction
        self.is_hero = is_hero
        
        
        self.screen = screen # screen in which unit's sprite appears
        self.field = params.FIELD_RECT # field in screen on which unit operates (bounces off border)
        
        #self.init_position = ( randint(0, hex_grid.Hex_grid.width), randint(0, hex_grid.Hex_grid.height)) # location in grid
        #self.init_position = ( randint(0, grid_map.Grid_map.nrows), randint(0, grid_map.Grid_map.ncols)) # location in grid
        self.init_position = (randint(0, int(params.GRID_SIZE[0])), int(randint(0, params.GRID_SIZE[1]))) # location in grid (measured in grids)
        print("original init_position", self.init_position)
        
        
        self.init_direction = (choice([-1, 1]), choice([-1, 1])) # starting direction
        #self.movement = .05 # unit travel speed, in pixels/millisecond (px/ms)
        pawn_image = pygame.image.load("images/bluepawn.png").convert_alpha()         
        self.base_image = pawn_image
        self.image = self.base_image
        # I added this line
        self.rect = self.base_image.get_rect()  
        self.image_w = self.rect[2]
        self.image_h = self.rect[3]
        
        #self.pos = vec2d(self.init_position) # current coordinates: [0]=x, [1]=y
        self.pos = self.init_position
        self.pos_to_rect()
        #self.direction = vec2d(self.init_direction).normalized() # velocity
        self.direction = (0,0) # intended x=change in row (-1, 0, 1) y=change in column (-1, 0, 1)
                
        self.state = Unit.ALIVE
        
    #------------------ PRIVATE PARTS ------------------#
    # States the unit can be in
    #
    # ALIVE: The creep is roaming around the screen
    # DYING: The creep is now dying, just a moment before death.
    # DEAD: The creep is dead and inactive
    (ALIVE, EXPLODING, DEAD) = range(3)
    _counter = 0 # timer counter for changes in unit's random movement or behavior
    

    ##################################################################### UPDATE
    def update(self, time_passed):
        """ Update the unit.
            time_passed: The time passed (in ms) since the previous update. """
        if self.state == Unit.ALIVE:
            
            #check that unit is in melee and thus not free to move
            if not self.in_combat:
                
                # Check to see if it's time to change the direction  - or take other action
                #if self.targets[0] == (0.0):
                if self.wander:
                    self.change_direction(time_passed) 
                    
                    if not unit_vs_obstacle_collision_check(self):
                        #print("pos:", self.pos, "   rect:", self.rect)
                        self.pos += self.direction[0], self.direction[1]
                        #self.pos[1] += self.direction[1]
                        self.rect[0] = self.pos[0]
                        self.rect[1] = self.pos[1]

                    self.pos_to_rect()
                        
                else: # if not wandering
                    # get direction from user input
                    dummy = False
                    
                # Check for out-of-bounds
                if self.pos[0] < 0:
                    self.pos[0] = 0
                    self.direction[0] *= -1
                elif self.pos[0] > params.GRID_SIZE[0]:
                    self.pos[0] = params.GRID_SIZE[1]
                    self.direction[0] *= -1
                if self.pos[1] < 0:
                    self.pos[1] = 0
                    self.direction[1] *= -1
                elif self.pos[1] > params.GRID_SIZE[0]:
                    self.pos[1] = params.GRID_SIZE[1]
                    self.direction[1] *= -1
            else:
                #print("unit is in melee")
                dummy = False
                
                FIELD_RECT = Rect(100, 50, 500, 450)
                
        
        elif self.state == Unit.EXPLODING:
            if self.explode_animation.active:
                self.explode_animation.update(time_passed)
            else:
                self.state = Unit.DEAD
                self.kill()
        
        elif self.state == Unit.DEAD:
            pass
    ################################################################## los
    def pos_to_rect(self):
        self.rect[0] = int(params.FIELD_RECT[0]/2) + self.pos[0] * params.TILE_SIZE
        self.rect[1] = int(params.FIELD_RECT[1]/2) + self.pos[1] * params.TILE_SIZE
    
    
    def unit_los_check(self,unit_group):
        print("I'm checking individual los.")
        check_enemy_list = ENEMY_LIST  # check to see if there are any enemies
        #print("enemy list:", check_enemy_list)
        print("LOS ================================================")
        if check_enemy_list: # WORKS
            #print("there are enemies.")
            self.unit_vs_group_los_check(unit_group, ENEMY_LIST)
            
    def unit_vs_group_los_check(self, unit_group, enemy_list):
        """ check to see if unit and group unit see each other """ 
        for enemy_group in enemy_list:
            #print("enemy_list: ", enemy_list, "   enemy_group:", enemy_group)
            #print("enemy_group.group_list check", enemy_group.group_list)
            for enemy_unit in enemy_group.group_list:
                #print("checking each individual in the group")
                self.unit_vs_unit_los_check(unit_group, enemy_unit, enemy_group, kill=False)  

    def unit_vs_unit_los_check(self, hero_group, enemy_unit, enemy_group, kill=False):
        """ self = hero unit
            hero_group = unit group name
            enemy_unit = opponent unit
            kill = (bool) remove opponent unit on collision """
        hero_coord = (self.rect.x, self.rect.y)
        enemy_coord = (enemy_unit.pos[0], enemy_unit.pos[1])
        if distance(hero_coord, enemy_coord) <= self.los:
            print("woohoo - enemy in los - distance =", distance(hero_coord, enemy_coord))
            print("self:", self.rect, self.los, self.pos)
            print("enemy:", enemy_unit.rect, enemy_unit.los, enemy_unit.pos)            
            #print("DA - self:", self.direction.angle, "  DA - enemy:", enemy_unit.direction.angle)
            self.wander = False
            a = self.rect.x - enemy_unit.pos[1]
            b = self.rect.y - enemy_unit.pos[1]
            a *= a
            b *= b
            d = int(math.sqrt(a + b))
            if self.rect[0] - enemy_unit.pos[0] == 0:
                self.rect[0] += .01
            m = (self.rect[0] - enemy_unit.pos[0]) / (self.rect[1] - enemy_unit.pos[1])
            r = math.atan(m)
            deg = int(math.atan(r)*100)
            
                    
            #print("sd angle = ", self.direction.angle)
            #print("===============================================OLD=", self.direction.x, self.direction.y)
            #x, y = self.pos
            x = self.pos[0]
            y = self.pos[1]
            xx, yy = self.targets[0]
            
            #if self.direction.angle - deg < 0:
                #self.direction.angle -= 1
            #elif self.direction.angle - deg > 0:
                #self.direction.angle *= -deg          
            
            #if x < xx and y < yy:
                #self.direction.angle += 1 * self.turn_to_opp  
            #elif x < xx and y > yy:
                #self.direction.angle -= 1 * self.turn_to_opp
            #elif x > xx and y < yy:
                #self.direction.angle += 1 * self.turn_to_opp
            #elif x > xx and y > yy:
                #self.direction.angle -= 1 * self.turn_to_opp
            
            #if x < xx:
                #self.direction.x += 1 * self.turn_to_opp  
            #elif x > xx:
                #self.direction.x -= 1 * self.turn_to_opp
            #if y < yy:
                #self.direction.y += 1 * self.turn_to_opp
            #elif y > yy:
                #self.direction.y -= 1 * self.turn_to_opp                    
            
            #print("===============================================NEW=", self.direction.x, self.direction.y)
                                
                    
                    
                
            #if deg - self.direction.angle > 180:
                #if deg > self.direction.angle:
                    #self.direction.angle += self.turn_to_opp
                #elif deg < self.direction.angle:
                    #self.direction.angle -= self.turn_to_opp
            #else:
                #if deg > self.direction.angle:
                    #self.direction.angle -= self.turn_to_opp
                #elif deg < self.direction.angle:
                    #self.direction.angle += self.turn_to_opp

            print("distance:", d, "  slope:", m, "  radians:", r, "  degrees:", deg)            
            #self.direction.angle += deg * self.turn_to_opp
            #self.direction.angle += deg_dif * self.turn_to_opp
            
            
            print("angle adjusted to self")
            #print("DA - self:", self.direction.angle, "  DA - enemy:", enemy_unit.direction.angle)
            
            self.image_w, self.image_h = self.image.get_size()
                    
            bounds_rect = self.field.inflate( -self.image_w, -self.image_h)
                                
            if self.pos[0] < bounds_rect.left:
                self.pos[0] = bounds_rect.left
                self.direction[0] *= -1
            elif self.pos[0] > bounds_rect.right:
                self.pos[0] = bounds_rect.right
                self.direction[0] *= -1
            elif self.pos[1] < bounds_rect.top:
                self.pos[1] = bounds_rect.top
                self.direction[1] *= -1
            elif self.pos[1] > bounds_rect.bottom:
                self.pos[1] = bounds_rect.bottom
                self.direction.y *= -1            
            
            return
        else:
            print("no los")
            self.wander = True
            return                
    
    ################################################################## collision    
    def unit_collision_check(self,unit_group):
        #print("I'm checking individual collisions.")
        check_enemy_list = ENEMY_LIST  # check to see if there are any enemies
        #print("enemy list:", check_enemy_list)
        #print()
        if check_enemy_list: # WORKS
            #print("there are enemies.")
            self.unit_vs_group_collision_check(unit_group, ENEMY_LIST)
        else: # no enemy units - test flag to pause program - WORKS
            #print("there are no enemies in the list")
            #print("< - Pausing Module - >")
            params.paused == True
            
    #def unit_vs_obstacle_collision_check(self):
        #""" check to see if unit runs into an obstacle object"""
        #print("I'm in obstacle collision")
        #for group in OBSTACLE_LIST:
            #print("Hey, there's an obsticle group")
            #for obstacle in group.group_list:
                #print("Found an obstacle.")
                
                ## test false - no collision - WORKS
                ## test true - collision - WORKS
        #return(False) 
    

    def unit_vs_group_collision_check(self, unit_group, enemy_list):
        """ check to see if unit and group unit collide """ 
        for enemy_group in enemy_list:
            #print("enemy_list: ", enemy_list, "   enemy_group:", enemy_group)
            #print("enemy_group.group_list check", enemy_group.group_list)
            for enemy_unit in enemy_group.group_list:
                #print("checking each individual in the group")
                self.unit_vs_unit_collision_check(unit_group, enemy_unit, enemy_group, kill=False)
                
    def unit_vs_unit_collision_check(self, hero_group, enemy_unit, enemy_group, kill=False):
        """ self = hero unit
            hero_group = unit group name
            enemy_unit = opponent unit
            kill = (bool) remove opponent unit on collision """
        #print("unit rect: ", self.rect, "   unit pos", self.pos)  
        #print("opp rect: ", enemy_unit.rect, "   opp pos", enemy_unit.pos) 
        
        if (  self.rect[0] + (self.rect[2]/2) >= enemy_unit.rect[0] - (enemy_unit.rect[2]/2) and 
              self.rect[0] - (self.rect[2]/2) <= enemy_unit.rect[0] + (enemy_unit.rect[2]/2)):
            if (  self.rect[1] + (self.rect[3]/2) >= enemy_unit.rect[1] - (enemy_unit.rect[3]/2) and 
                  self.rect[1] - (self.rect[3]/2) <= enemy_unit.rect[1] + (enemy_unit.rect[3]/2)):  
                #print("woohoo - collision between 2 units")
                #print("unit rect: ", self.rect, "   unit pos", self.pos)  
                #print("opp rect: ", enemy_unit.rect, "   opp pos", enemy_unit.pos)                
                #print("do something")
                #print()
                #print("melee list:", self, hero_group, enemy_unit, enemy_group)
                MELEE_LIST.append((self, hero_group, enemy_unit, enemy_group))
                #print("melee list: ", MELEE_LIST)                
                self.in_combat = True # flag as in_combat #### need to add to melee_list
                # do something: put pair in melee_group, add exp points, add hit unit to list, change image...
                if kill == True:
                    enemy_group.remove_unit(enemy_unit)             
                
            else:
                #print("no collision between 2 units")
                return
                        
    ####################################################################### draw   
    def draw(self): 
        """ Blit the unit onto the designated screen """
        if self.state == Unit.ALIVE:
            # The creep image is placed at self.pos. 
            # To allow for smooth movement even when ratating and changing direction
            # its placement is always centered.
            self.draw_rect = self.image.get_rect().move(
                self.pos[0] - self.image_w / 2, 
                self.pos[1] - self.image_h / 2)
            self.screen.blit(self.image, self.draw_rect)
            
            # The health bar is 15x4 px.
            #
            health_bar_x = self.pos[0] - 7
            health_bar_y = self.pos[1] - self.image_h / 2 - 6
            self.screen.fill(   Color('red'), 
                                (health_bar_x, health_bar_y, 15, 4))
            self.screen.fill(   Color('green'), 
                                (   health_bar_x, health_bar_y, 
                                    self.health_bar_len(self.health), 4))
        
        elif self.state == Creep.EXPLODING:
            self.explode_animation.draw()
        
        elif self.state == Creep.DEAD:
            pass  
    
    def health_bar_len(self, current_health):
        max_bar_len = 15 # maximum length of health bar regardless of health points
        current_health_bar = int(self.health/self.max_health * max_bar_len)
        if current_health_bar < 0:
            current_health_bar = 0
        return(current_health_bar)
        
    def change_direction(self, time_passed): # can be any specific timed event of behavior
        """ Turn by 45 degrees in a random direction once per 0.4 to 0.5 seconds. """
        self._counter += time_passed
        if self._counter > randint(400, 500):
            #self.direction.rotate(45 * randint(-1, 1))
            change = randint(0,6)
            if change == 1: # left, up
                if self.pos[0] % 2 == 0:
                    self.direction = (-1, -1) 
                else:
                    self.direction = (-1, 0)
            elif change == 2: # up
                self.direction = (0, -1)
            elif change == 3: # right, up
                if self.pos[0] % 2 == 0:
                    self.direction = (1, -1) 
                else:
                    self.direction = (1, 0)
            elif change == 4: # right, down
                if self.pos[0] % 2 == 0:
                    self.direction = (1, 1) 
                else:
                    self.direction = (1, 0)
            elif change == 5: # down
                self.direction = (0, 1)
            elif change == 6: # left, down
                if self.pos[0] % 2 == 0:
                    self.direction = (-1, 1) 
                else:
                    self.direction = (-1, 0)
            else: # change is not entered or is 0 (stay put)
                self.direction = (0,0)
            self._counter = 0 # reset counter until next direction change
            
            
    def mouse_click_event(self, pos): 
        """ The mouse was clicked in pos of unit """
        if self._point_is_inside(vec2d(self.pos)): # if unit is clicked on, do something
            #self._decrease_health(3)
            dummy = False
            
            
    def _point_is_inside(self, point):
        """ Is a point (given as a vec2d) inside unit body? """
        img_point = point - vec2d(  
            int(self.pos[0] - self.image_w / 2),
            int(self.pos[1] - self.image_h / 2))
        try:
            pix = self.image.get_at(img_point)
            return pix[3] > 0
        except IndexError:
            return False            
            
    def add_unit(self, screen, unit_type="unit"):
        if unit_type == "creep":
            Creep.add_creep()
        elif unit_type == "pawn":
            Pawn.add_pawn()
        else:
            Unit(screen) 
        
    def print_unit(self):
        print("attack:", self.attack)
        print("initiative:", self.initiative)
        print("defense:", self.defense)
        print("speed:", self.speed)
        print("health:", self.health)
        
    def start_loc_adj(self): 
        """ adjusts hero start position to bottom half of screen & others to top half """
        #print("orig position, pre adjustment", self.init_position)
        #print("unit is_hero status:", self.is_hero)
        if self.is_hero:
            self.init_position = (self.init_position[0], int(self.init_position[1]/2)+int(params.GRID_SIZE[1]/2)) # adjust to bottom half of grid
        else: 
            self.init_position = (self.init_position[0], int(self.init_position[1]/2)) # adjust to top half of grid
        #print("final position, post adjustment", self.init_position)
   
class Creep(Unit):
    def __init__(self, screen):
        Unit.__init__(self, screen)
        self.names = {"name": choice(messages.creep_na)}
        self.is_hero = False
        self.start_loc_adj()
        #self.init_position = (self.init_position[0], int(self.init_position[1]/2)) # adjust to top half of grid
        #print("adjust init_position to top half of screen", self.init_position)
            
class Pawn(Unit):
    def __init__(self, screen):
        Unit.__init__(self, screen)
        self.fresh_orders = False # bool to flag if command for unit is new or old
        self.start_loc_adj()
        
class Big_pawn(Unit):
    def __init__(self, screen):
        Unit.__init__(self, screen)
        self.fresh_orders = False # bool to flag if command for unit is new or old
        self.attack = 1 # unit stat for offensive combat capability
        self.defense = 1 # unit stat for offensive combat capability
        self.initiative = 1.2 # unit stat for first swing advantage
        self.speed = 1 # unit stat for dexterity advantage     
        pawn_image = pygame.image.load("images/pawn_big.png").convert_alpha()         
        self.base_image = pawn_image
        # I added this line
        self.rect = self.base_image.get_rect()   
        self.start_loc_adj()
        
########################################################################  groups
class Unit_group(object):
    def __init__(self, screen):
        self.group_list = []
        self.wins = 0
        self.removal_list = []
        ALL_UNIT_GROUPS.append(self)
        
    def los_check(self, hero_group_name):
        for unit in self.group_list:
            if not unit.in_combat:
                print("let's take a look at hero vs enemies for LOS.")
                unit.unit_los_check(hero_group_name)
            else:
                #print("unit already in combat, moving on")
                dummy = False    
        
    def collision_check(self, hero_group_name):
        for unit in self.group_list:
            if not unit.in_combat:
                #print("let's take a look at hero vs enemies for collisions.")
                unit.unit_collision_check(hero_group_name)
            else:
                #print("unit already in combat, moving on")
                dummy = False
               
    def add_unit(self, screen, unit_type="unit"):
        if unit_type == "creep":
            self.add_creep(screen)
        elif unit_type == "pawn":
            self.add_pawn(screen)
        elif unit_type == "big_pawn":
            self.add_big_pawn(screen)            
        else:
            new_unit = Unit(screen)
            self.group_list.append(new_unit)
            
    def dump_removal_list(self):
        for unit in self.removal_list:
            self.remove_unit(unit)
        self.removal_list = []
            
    def remove_unit(self, unit):
        self.group_list.remove(unit)
            
    def print_group_units(self):
        unit_no = 0
        for unit in self.group_list:
            print("unit#:", unit_no)
            unit.print_unit()
            unit_no += 1
            print()      
        
class Pawn_group(Unit_group):
    def __init__(self, screen):
        Unit_group.__init__(self, screen)
        self.data_2 = 2
        
    def add_pawn(self, screen):
        new_pawn = Pawn(screen)
        self.group_list.append(new_pawn)
        
class Big_pawn_group(Unit_group):
    def __init__(self, screen):
        Unit_group.__init__(self, screen)
        
    def add_big_pawn(self, screen):
        new_pawn = Big_pawn(screen)
        self.group_list.append(new_pawn)        

class Creep_group(Unit_group):
    def __init__(self, screen):
        Unit_group.__init__(self, screen)
        self.data_2 = 3
        
    def add_creep(self, screen):
        new_creep = Creep(screen)
        self.group_list.append(new_creep)
        
################################################################################
## utilities
################################################################################

def distance(unit_a, unit_b):
    """ determine distance between 2 unit coordinates = (1,1) (1,2) """
    a = unit_a[0] - unit_b[0]
    b = unit_a[1] - unit_b[1]
    a *= a
    b *= b
    c = int(math.sqrt(a + b))
    return(c)

def unit_lists_empty_check(): # WORKS
    for unit_group in ENEMY_LIST:
        if not unit_group.group_list:
            ENEMY_LIST.remove(unit_group)
            # add events when an enemy group is eliminated
            # add events when all enemy groups are eliminated

def print_all_stats():
    """ prints stats for all units in combat """
    print()
    print("Final Stats of Surviving Units:")
    champion_average = 0
    fewest_hits = 0
    most_melee = 0
    for group in ALL_UNIT_GROUPS:
        for unit in group.group_list:
            if unit.stats["swings"] > 0 and unit.stats["melee_won"] > 0:
                batting_average = str(int(unit.stats["melee_won"] / unit.stats["swings"]*100))
            else:
                batting_average = str(0)
            print(unit, unit.stats, "batting average:", batting_average + "%")
            if int(unit.stats["melee_won"]) >= most_melee:
                champion = unit
                champion_average = int(batting_average)
                fewest_hits = int(unit.stats["swings"])
                most_melee = int(unit.stats["melee_won"])
    if unit.names.get("name"):  
        print("The Champion was: " + champion.names.get("name"), "  Melee Victories:", most_melee, "  Swings:", fewest_hits, "  Average:", champion_average)
    else:
        print("The Champion was some unnamed wretch. ", "   Melee Victories:", most_melee, "  Swings:", fewest_hits, "  Average:", champion_average)
            
def unit_vs_obstacle_collision_check(unit):
    """ check to see if unit runs into an obstacle object"""
    #print("I'm in obstacle collision on the obstacle page")
    #print("I'm checking a unit.", unit)
    
    for group in ALL_OBSTACLES_GROUPS:
        #print("Hey, there's an obsticle group")
        for obstacle in group.group_list:
            #print("Found an obstacle.")
            #print("obstacle info", obstacle.pos)
            # check obstacle rect with unit rect to detect overlap
            
            if (  unit.pos[0] + (unit.rect[2]/2) >= obstacle.pos[0] - (obstacle.rect[2]/2) and 
                  unit.pos[0] - (unit.rect[2]/2) <= obstacle.pos[0] + (obstacle.rect[2]/2)):
                if (  unit.pos[1] + (unit.rect[3]/2) >= obstacle.pos[1] - (obstacle.rect[3]/2) and 
                      unit.pos[1] - (unit.rect[3]/2) <= obstacle.pos[1] + (obstacle.rect[3]/2)):  
                    #print("boing!")
                    return(True)

            # test false - no collision - WORKS
            # test true - collision - WORKS
    return(False)              
        
################################################################################
## Unit Testing                                                               ##
################################################################################
if __name__ == "__main__":   
    
    import params
    screen = pygame.display.set_mode((params.SCREEN_WIDTH, params.SCREEN_HEIGHT), 0, 32)
    image_lib = Image_lib()
    
    #TEST make groups
    micro_pawns = Pawn_group(screen)
    micro_creeps = Creep_group(screen)
    ENEMY_LIST.append(micro_creeps)
    
    #TEST make grid
    grid = grid_map.Grid_map(screen)
    
    micro_units = Unit_group(screen)
    
    micro_units.add_unit(screen, "unit")
    micro_units.add_unit(screen)
    
    micro_pawns.add_unit(screen, "pawn")
    micro_pawns.add_unit(screen, "pawn")
    micro_pawns.add_unit(screen, "pawn")
    
    for unit_no in range(1,5):
        micro_creeps.add_unit(screen, "creep")
        
    micro_pawns.wins +=1
    
    #print()
    #print("total pawns before removal:", len(micro_pawns.group_list))
    micro_pawns.group_list[1].attack = 8
    #print("attack of pawn to be removed:", micro_pawns.group_list[1].attack)
    unit = micro_pawns.group_list[1]
    micro_pawns.remove_unit(unit)
    
    print()
    print("total pawns in pawn group_list:", len(micro_pawns.group_list))
    print("total creep in creeps group_list:", len(micro_creeps.group_list))
    print("total units in units group_list:", len(micro_units.group_list))
    print("wins (units, pawns, creeps):", micro_units.wins, micro_pawns.wins, micro_creeps.wins)
    
    micro_pawns.group_list[1].attack = 3
        
    #print()
    #print("micro_pawns content:")

    print()
    print("Pawns:")
    micro_pawns.print_group_units()
    print("Creeps:")
    micro_creeps.print_group_units()
    print("Generic Units:")
    micro_units.print_group_units()   
    
    #for unit in micro_units.group_list:
        #print("unit rect: ", unit.rect, "   unit pos", unit.pos)
    

    print()
    print("-- TEST DONE --")
    print()
    pygame.quit()
    sys.exit()  