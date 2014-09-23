################################################################################
## obstacle
################################################################################

import os, sys
import pygame
from pygame import Color
from pygame.sprite import Sprite
from images_lib import Image_lib
from random import randint, choice
import my_clock
from vec2d import vec2d
import params
import units
import grid_map



# ------------------------------------------------------------------------------
# Libraries & Lists

#OBSTACLE_FILENAMES = ["gray_brick.png"]
N_OBSTACLE = 5




################################################################################

class Obstacle(Sprite):
    """ generic parent class for all obstacle types """ # NOTE: calls to class must add screen
    def __init__(self, screen, vector = (0,0)): # NEED: unit regular image, damaged image is damagable - vector only if it moves
        Sprite.__init__(self, screen)

        self.health = 15 # unit stat for current health points
        self.max_health = 15 # unit stat for max health
        self.use_health_bar = False # false=no health bar / true=use health bar

        #self.story = {} # library of character history
        self.traits = {} # library of traits

        self.screen = screen # screen in which unit's sprite appears
        self.field = params.FIELD_RECT # field in screen on which unit operates (bounces off border)
        
        #self.init_position = ( randint(self.field.left, self.field.right), randint(self.field.top, self.field.bottom)) # location on screen
        self.init_position = (randint(0, int(params.GRID_SIZE[0])), int(randint(0, params.GRID_SIZE[1]))) # location in grid (measured in grids)
        
        
        self.init_direction = (choice([-1, 1]), choice([-1, 1])) # starting direction
        self.movement = 0 # .05 # unit travel speed, in pixels/millisecond (px/ms)
        self.wander = True # True = move in random direction / False = move in continual direction

        obstacle_image = pygame.image.load("images/gray_brick.png").convert_alpha() # basic image 
        self.base_image = obstacle_image
        self.image = self.base_image

        # I added this line
        self.rect = self.base_image.get_rect()  
        
        # NOTE - set position and direction (if there is one)
        self.pos = self.init_position # current coordinates: [0]=x, [1]=y

        self.direction = (0,0) # intended x=change in row (-1, 0, 1) y=change in column (-1, 0, 1)  
        
        self.state = Obstacle.PASSIVE # set to do nothing but stay put
        
    #------------------ PRIVATE PARTS ------------------#
    # States the unit can be in
    #
    # ALIVE: The obstacle is active and capable of motion
    # PASSIVE: The obstacle is active but not capable of motion
    # DYING: The obstacle is now dying, just a moment before death.
    # DEAD: The obstacle is dead and inactive
    (ALIVE, PASSIVE, EXPLODING, DEAD) = range(4)
    _counter = 0 # timer counter for changes in unit's random movement or behavior
    
    ##################################################################### update
    def update(self, time_passed):
        """ Update the unit.
            time_passed: The time passed (in ms) since the previous update. """
        if self.state == Obstacle.ALIVE:
            
            # Check to see if it's time to change the direction  - or take other action
            
            if self.wander:
                self._change_direction(time_passed) 
                self.pos[0] += self.direction[0]
                self.pos[1] += self.direction[1]
                self.rect[0] = self.pos[0]
                self.rect[1] = self.pos[1]
                
                self.pos_to_rect()                
            
            # When the image is rotated, its size is changed.
            # We must take the size into account for detecting 
            # collisions with the walls.
            #
                self.image_w, self.image_h = self.image.get_size()
 
                bounds_rect = self.field.inflate(-self.image_w, -self.image_h)
            
                if self.pos[0] < 0:
                    self.pos[0] = 0
                    self.direction[0] *= -1
                elif self.pos[0] > grid_map.Grid_map.nrows:
                    self.pos[0] = grid_map.Grid_map.ncols
                    self.direction[0] *= -1
                if self.pos[1] < 0:
                    self.pos[1] = 0
                    self.direction[1]*= -1
                elif self.pos[1] > grid_map.Grid_map.nrows:
                    self.pos[1] = grid_map.Grid_map.ncols
                    self.direction[1] *= -1
        
        elif self.state == Obstacle.PASSIVE: 
            # just sit there doing nothing or doing whatever it does
            dummy = False
            #print("look, Ma, no hands!")
            #print("info: pos, direction", self.pos, self.direction)
            self.image_w, self.image_h = self.image.get_size()
            self.draw_rect = self.image.get_rect().move(
                            self.pos[0] - self.image_w / 2, 
                            self.pos[1] - self.image_h / 2)            
        
        elif self.state == Obstacle.EXPLODING:
            if self.explode_animation.active:
                self.explode_animation.update(time_passed)
            else:
                self.state = Obstacle.DEAD
                self.kill()
        
        elif self.state == Obstacle.DEAD:
            pass
    
    ################################################################## collision
    #def unit_collision_check(self,unit_group):
        ##print("I'm checking individual collisions.")
        #check_move_list = ALL_MOVING_GROUPS  # check to see if there are any enemies
        ##print("enemy list:", check_enemy_list)
        #print()
        #if check_move_list: # WORKS
            ##print("there are enemies.")
            #self.unit_vs_group_collision_check(unit_group, ALL_MOVING_GROUPS)
        #else: # no enemy units - test flag to pause program - WORKS
            ##print("there are no enemies in the list")
            ##print("< - Pausing Module - >")
            #params.paused == True
        
    #def unit_vs_group_collision_check(self, unit_group, moving_list):
        #""" check to see if unit and group unit collide """ 
        #for moving_group in moving_list:
            #for moving_unit in moving_group.group_list:
                #self.unit_vs_unit_collision_check(unit_group, moving_unit, moving_group, kill=False)
                
    #def unit_vs_unit_collision_check(self, unit_group, moving_unit, moving_group, kill=False):
        #""" self = hero unit
            #unit_group = unit group name
            #moving_unit = opponent unit
            #kill = (bool) remove opponent unit on collision """
        ##print("unit rect: ", self.rect, "   unit pos", self.pos)  
        ##print("opp rect: ", moving_unit.rect, "   opp pos", moving_unit.pos) 
        
        #if self.rect[0] + (self.rect[2]/2) >= moving_unit.rect[0] - (moving_unit.rect[2]/2) and self.rect[0] - (self.rect[2]/2) <= moving_unit.rect[0] + (moving_unit.rect[2]/2):
            #if self.rect[1] + (self.rect[3]/2) >= moving_unit.rect[1] - (moving_unit.rect[3]/2) and self.rect[1] - (self.rect[3]/2) <= moving_unit.rect[1] + (moving_unit.rect[3]/2):        
                #print("woohoo - collision between 2 units")
                #print("unit rect: ", self.rect, "   unit pos", self.pos)  
                #print("opp rect: ", moving_unit.rect, "   opp pos", moving_unit.pos)                
                #print("do something")
                #print()
                #print("melee list:", self, unit_group, moving_unit, moving_group)
                #MELEE_LIST.append((self, unit_group, moving_unit, moving_group))
                #print("melee list: ", MELEE_LIST)                
                #self.in_combat = True # flag as in_combat #### need to add to melee_list
                ## do something: put pair in melee_group, add exp points, add hit unit to list, change image...
                #if kill == True:
                    #moving_group.remove_unit(moving_unit)             
                
            #else:
                ##print("no collision between 2 units")
                #return
                        
    ####################################################################### draw   
    def draw(self): 
        """ Blit the unit onto the designated screen """
        if self.state == Obstacle.ALIVE or self.state == Obstacle.PASSIVE:
            # The obstacle image is placed at self.pos. 
            # To allow for smooth movement even when ratating and changing direction
            # its placement is always centered.
            if self.state == Obstacle.ALIVE:
                self.draw_rect = self.image.get_rect().move(
                    self.pos[0] - self.image_w / 2, 
                    self.pos[1] - self.image_h / 2)
            self.screen.blit(self.image, self.draw_rect)
            
            if self.use_health_bar:
                # The health bar is 15x4 px.
                #
                health_bar_x = self.pos[0] - 7
                health_bar_y = self.pos[1] - self.image_h / 2 - 6
                self.screen.fill(   Color('red'), 
                                    (health_bar_x, health_bar_y, 15, 4))
                self.screen.fill(   Color('green'), 
                                    (   health_bar_x, health_bar_y, 
                                        self.health_bar_len(self.health), 4))
        elif self.state == Obstacle.EXPLODING:
            self.explode_animation.draw()
        
        elif self.state == Obstacle.DEAD:
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
            
    def add_unit(self, screen, unit_type="obstacle"):
        if unit_type == "wall":
            Wall.add_wall()
        elif unit_type == "water":
            Water.add_water()
        else:
            Obstacle(screen) 
        
    def print_obstacle(self):
        print("health:", self.health)
        
################################################################################        
    
class Wall(Obstacle):
    def __init__(self, screen):
        Obstacle.__init__(self, screen)
        
class Water(Obstacle):
    def __init__(self, screen):
        Obstacle.__init__(self, screen)
        
################################################################################

########################################################################  groups
class Obstacle_group(object):
    def __init__(self, screen):
        self.group_list = []
        self.removal_list = []
        units.ALL_OBSTACLES_GROUPS.append(self)
         
    def add_obstacle(self, screen, unit_type="obstacle"):
        if unit_type == "wall":
            self.add_wall(screen)
        elif unit_type == "water":
            self.add_water(screen)
        else:
            new_obstacle = Obstacle(screen)
            self.group_list.append(new_obstacle)
            
    def dump_removal_list(self):
        for obstacle in self.removal_list:
            self.remove_obstacle(obstacle)
        self.removal_list = []
            
    def remove_obstacle(self, obstacle):
        self.group_list.remove(obstacle)
            
    def print_group_units(self):
        unit_no = 0
        for unit in self.group_list:
            print("unit#:", unit_no)
            unit.print_unit()
            unit_no += 1
            print()      
        
class Wall_group(Obstacle_group):
    def __init__(self, screen):
        Obstacle_group.__init__(self, screen)
        
    def add_wall(self, screen):
        new_wall = Wall(screen)
        self.group_list.append(new_wall)
        
class Water_group(Obstacle_group):
    def __init__(self, screen):
        Obstacle_group.__init__(self, screen)
        
    def add_water(self, screen):
        new_water = Water(screen)
        self.group_list.append(new_water)        
        
################################################################################
## utilities
################################################################################
 
def exit_game():
    #print()
    #for group in units.ALL_OBSTACLES_GROUPS:
        #print("Hey, there's still an obsticle group")
        #for obstacle in group.group_list:
            #print("Found an end-of-game obstacle.")
    #print("-- Done --") 
    #print()    
    pygame.quit()
    sys.exit()
    
################################################################################
## test
################################################################################
if __name__ == "__main__":  
    pygame.init()
    import params
    import main_board
    
    screen = pygame.display.set_mode((params.SCREEN_WIDTH, params.SCREEN_HEIGHT), 0, 32)
    image_lib = Image_lib()  
    
    # Game parameters
    SCREEN_WIDTH = params.SCREEN_WIDTH
    SCREEN_HEIGHT = params.SCREEN_HEIGHT
    FIELD_RECT = params.FIELD_RECT
    MESSAGE_RECT = params.MESSAGE_RECT
    
    bg_tile_img = image_lib.bg_tile_img
    time_count = 0
    
    paused = params.paused
    won = params.won 
    grid_map = grid_map.Grid_map(screen)
    
    #setup clock
    clock = pygame.time.Clock() #                                               This line must be in the program for timer to run
    time = my_clock.Time_clock() #                                              This line must be in the program for timer to run 
    my_clock.et_group = my_clock.Et_group() #     
    
    test_pawn  = units.Pawn(screen)
    test_pawn.base_image = image_lib.pawn_big_img
    #ALL_MOVING_GROUPS.append(test_pawn)
    
    micro_walls = Wall_group(screen)
    max_walls = 5
    for obstacle_num in range(0, max_walls):
        micro_walls.add_obstacle(screen, "wall")
    for obstacle in micro_walls.group_list:
        obstacle.base_image = image_lib.wall_img
            

    #for group in units.ALL_OBSTACLES_GROUPS:
        #print("Hey, there's an obsticle group")
        #for obstacle in group.group_list:
            #print("Found an obstacle.")

    #print("units page test", units.ALL_OBSTACLES_GROUPS[0])
    ######################################################################## RUN
    while True or time_passed < 500:
        time_passed = clock.tick(50) # Limit frame speed to 50 FPS
        time.tick()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game()  
                
                
        main_board.draw_background(screen, image_lib.bg_tile_img, params.FIELD_RECT)
                         
        

        for group in units.ALL_OBSTACLES_GROUPS:
            for obstacle in group.group_list:
                obstacle.update(time_passed)
                obstacle.draw()          
        
        #print("state:", test_wall.state)
        test_pawn.update(time_passed)
        test_pawn.draw()
        
        
        
        ################################################ Refresh screen
        pygame.display.flip() # Update and redraw everything        
        
    
    
    
    
