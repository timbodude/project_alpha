#Max Line Length(79)##########################################################
import pygame
from pygame import Color, Rect
from pygame.sprite import Sprite
import os
from params import DEFAULT_GAME_FONT, FIELD_RECT, \
                   TILE_SIZE, MARGIN, GRID_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT
from random import randint, choice
from images_lib import (  LT_GRAY , WHITE, GREEN, MDW_GREEN)
import PygButton
import dice
from messages import HERO_WINS, ENEMY_WINS

""" Things to consider and set: 
    - how far unit can move/turn
    - how likely it is for a unit to get initiative
    - how likely it is for a unit to have successful attack
    - how likely it is for a unit to have a successful defense
"""

# number of starting players (can go up to 8, but not beyond that as there 
# are only 8 color choices
players_start_qty = 2 
player_colors = ("red", "green", "blue", "gray", 
                 "yellow", "brown", "purple", "white") 
used_player_colors = []
player_unit_counter = 0
_image_library = {}
PAWN_IMG = "images/bluepawn.png"
player_unit = {  "red" : "images/red_tank.png", 
                 "green" : "images/green_tank.png", 
                 "blue" : "images/blue_tank.png",
                 "gray" : "images/gray_tank.png",
                 "yellow" : "images/yellow_tank.png",
                 "brown" : "images/brown_tank.png",
                 "purple" : "images/purple_tank.png",
                 "white": "images/white_tank.png"  }
B_rnd = {"green": "images/btn_green.png", 
         "gray": "images/btn_gray.png", 
         "red": "images/btn_red.png"}
dice = dice.Dice()
player_info_area = (605, 165, 20, 20)

unit_active_y = { 0: player_info_area[1] + 24*1,
                  1: player_info_area[1] + 24*2,
                  2: player_info_area[1] + 24*3,
                  3: player_info_area[1] + 24*4,
                  4: player_info_area[1] + 24*5,
                  5: player_info_area[1] + 24*6,
                  6: player_info_area[1] + 24*7,
                  7: player_info_area[1] + 24*8}




class Unit(Sprite):
    """ generic class for basic player unit types """ 
    def __init__(self, screen, unit_no):
        """ Notes:
        """
        Sprite.__init__(self)
         # location in grid (in coordinates)
        self.loc = ()
        self.txt_status = "Standing By"
        # can be replaced with image
        self.color = LT_GRAY 
        self.alt_color = WHITE
        # (bool) True: alive False: dead
        self.state = True 
        # True: unit has been clicked on by user
        self.active = False 
        self.place_unit()
        # tile unit is moving into (in coordinates) - default is current location
        self.targ_tile = self.loc
        # indicates a unit is clicked on by player   
        # NOTE: same variable as self.active!!!
        self.selected = False
        self.screen = screen
        self.health = 3
        self.max_health = 3
        self.image = PAWN_IMG
        self.image_h = 18
        self.image_w = 18
        # this string that will print out for the player containing unit type and name
        self.info_msg1 = "Unit: Warrior" 
        # this string that will print out for the player containing status 
        # info
        self.info_msg2 = "   3/3   " + str(self.loc) 
        self.unit_no = unit_no
        self.unit_btns = []
        # standard training = 1 offensive & 1 defense swing (interchangeable)
        self.max_swings = 2 
        self.swings_used = 0
        self.in_melee = False
        self.initiative = 1
        self.gov_initiative = 1
        self.speed = 1
        self.gov_speet = 1
        self.attack = 1
        self.gov_attack = 1
        self.defense = 1
        self.gov_defense = 1
        self.stats = {  "swings":    2, 
                        "melee_won": 0 }
    
    @staticmethod
    def move_to_target(grid, unit):
        """  Generates new position based upon target location and current 
             position. 
             unit: unit to be moved, can get current location and target 
                   location
             NOTE: don't forget to update grid contents at some point & 
                   verify new position is legal
             CONSIDER: if pass grid_map variable name, can update 
                    Tile_grid.matrix[x,y] contents
        """
        old_x = unit.loc[0]
        old_y = unit.loc[1]
        new_x = unit.loc[0]
        new_y = unit.loc[1]
        if new_x > unit.targ_tile[0]: new_x -= 1
        elif new_x < unit.targ_tile[0]: new_x += 1
        if new_y > unit.targ_tile[1]: new_y -= 1
        elif new_y < unit.targ_tile[1]: new_y += 1   
        next_loc = (new_x, new_y)
        if TileGrid.is_grid_empty(grid, next_loc, unit): 
            Unit.update_grid_pos(grid, unit, next_loc, old_x, old_y)
        return(next_loc)

    @staticmethod
    def movement(grid, player_grp):
        """ overall calculations for unit movement phase
            - currently activated by button event
            unit: unit to be moved, can get current location and target 
                  location
            grid: grid_map name to update Tile_grid.matrix[x,y] contents
        """
        
        for player in player_grp.players:
            #print("**************total_number_of_players", len(player_grp.players))
            for unit_group in player.units:
                for unit in unit_group.group_list:
                    if unit.loc != unit.targ_tile and not unit.in_melee:
                        unit.txt_status = "Moving"
                        #print("unit", unit.unit_no, ": loc, targ_tile", unit.loc, unit.targ_tile)
                        next_loc = Unit.move_to_target(grid, unit)
                        unit.loc = next_loc
                    else:
                        #print("Unit Arrived", "unit", unit.unit_no, ": loc, targ_tile", unit.loc, unit.targ_tile)
                        unit.txt_status = "Arrived"
                    
    def calc_move(self, now_coord, targ_coord):
        """ outputs next_step: next location to move into
            now_coord: current position (in coordinates)
            targ_coord: end location
            next_step: what this routine outputs
        """
        print("pre calc: now, then, next_step:", now_coord, targ_coord)
        horiz = now_coord[0]
        vert = now_coord[1]
        if now_coord[0] < targ_coord[0]:
            horiz += 1
        elif now_coord[0] > targ_coord[0]:
            horiz -= 1
        if now_coord[1] < targ_coord[1]:
            vert += 1
        elif now_coord[1] > targ_coord[1]:
            vert -= 1        
        next_step = (horiz, vert)   
        print("post calc: now, then, next_step:", now_coord, targ_coord, next_step)
        return(next_step)
    
    @staticmethod
    def update_grid_pos(grid, unit, next_loc, old_x, old_y):
        """ place unit position into matrix and remove from previous matrix 
            record 
            NOTE: check to see if spot taken first
        """ 
        tile = grid.matrix[unit.loc[0]][unit.loc[1]]
        if unit in grid.matrix[old_x][old_y].contents: 
            grid.matrix[old_x][old_y].contents.remove(unit)
        tile.contents.append(unit)


    def assign_unit_targ_tile(self, new_targ):
        """ update targ_tile to clicked location """
        self.active = False
        self.targ_tile = new_targ
        self.txt_status = "Target Acquired"
        
    def assign_unit_color_units(self, player_color):
        """ assign basic unit based upon player color and create activate 
            button 
        """
        self.image = player_unit[player_color]
        self.make_btn_row()
        #print("unit no:", self.unit_no)
        
    def make_btn_row(self):
        """ create a row of buttons for each unit """
        # assign activate button for display
        temp_btn = PygButton.PygButton(rect=(605,
                                             (170 + 48 * self.unit_no),
                                             15,
                                             20), 
                                       normal = self.image, 
                                       unit=self, caption="A") 
        self.unit_btns.append(temp_btn)
        # assign activate button for display  
        temp_btn = PygButton.PygButton(  rect=(700,(170 + 48 * self.unit_no),15,20),
                                         caption = "B",
                                         normal = B_rnd["gray"],
                                         down = B_rnd["green"],
                                         highlight = B_rnd["red"],
                                         unit=self) 
        self.unit_btns.append(temp_btn)

    def place_unit(self):
        """ set initial coordinates in tile_map during unit creation 
            Right now, I'm just picking a random tile with the hope of no 
            duplication
        """
        #self.loc = (randint(0, params.GRID_SIZE[0]), randint(0, params.GRID_SIZE[1])) # location in grid
        pixel_loc = (randint(0, FIELD_RECT[2]), randint(0, FIELD_RECT[3])) # location in pixels based on field size
        self.loc = self.coord_to_grid(pixel_loc) # convert to grid coordinates  
        
    def coord_to_grid(self, pos):
        """ returns grid location based on sprite pos(x,y) for test purposes 
            of clicked location 
        """
        coord = (  int((pos[0] - FIELD_RECT[0]) / (TILE_SIZE + MARGIN)),
                           int((pos[1] - FIELD_RECT[1]) / (TILE_SIZE + MARGIN)))
        #print(  "click pos:", pos, " grid pos:", self.selected)        
        return(coord)        
    
    def is_unit_selected(self, coord): 
        """ see if unit has been checked on 
            coord: grid tile position
            NOT WORKING PROPERLY - unit location not lining up with grid 
            coordinates
        """
        if coord == self.loc:
            #print("bingo, in tile #:", coord)
            self.active = True
            return True
        else:
            #print("not this one at:", coord)
            dummy = False #                                                      - do whatever happense when you don't click on a unit

#     def move_unit(self): #                                                       - should be called from gridmap updating area to see if melee occurs
#         """ move unit into next square if empty """
#         #print("moving unit")
#         if self.active == True and self.loc != self.targ_tile:
#             #print("i should move", self.loc, self.targ_tile)
#             calc_move(self.loc, self.targ_tile)
#             #print("i didn't really move, I just though about where to go")
#         else:
#             print("I'm at my target location")
            
    def update_unit(self):
        """ update unit and print to screen """
        #print("printing a unit to screen")
        if self.selected == False: #check to see if unit is active or not to determine color and assign to curser_color
            curser_color = self.color
        else: 
            curser_color = self.alt_color
        #print("selected, curser color:", self.matrix[row][col].selected, curser_color)
        
        ## THIS WORKS TO PRINT A BLOCK - currently replaced with printing a stick figure
        #pygame.draw.rect(  self.screen,
                           #curser_color,
                           #[(params.FIELD_RECT[0] + self.loc[0] * (params.TILE_SIZE + params.MARGIN)),
                            #(params.FIELD_RECT[1] + self.loc[1] * (params.TILE_SIZE + params.MARGIN)),
                            #params.TILE_SIZE,
                            #params.TILE_SIZE] )
        self.draw()
        
    def prep_unit_text_info(self):
        """ creates message for unit output to player_command window """
        if self.state == True:
            self.info_msg2 = "   " + str(self.health) + "/" + str(self.max_health) + "   " + str(self.loc)
        else:
            self.info_msg2 = "    -/" + str(self.max_health) + "   " + str(self.loc)
    
    def draw(self):
        """ Blit the unit onto the designated screen 
            Example:
            screen.blit(img,(0,0))
        """
        if self.state == True:
            self.screen.blit(self.get_image(self.image), (self.loc[0]*24 + 4, self.loc[1]*24 + 4)) # 4 is x & y offset
            self.health_bar()
        
    def health_bar(self):
        # The health bar is 15x4 px.
        #
        health_bar_x = self.loc[0]*24 + 0 # 0 is x-offset
        health_bar_y = self.loc[1]*24 + self.image_h / 2 - 11 # 11 is y-offset
        self.screen.fill(   Color('red'), 
                            (health_bar_x, health_bar_y, 15, 2))
        self.screen.fill(   Color('green'), 
                            (   health_bar_x, health_bar_y, 
                                self.health_bar_len(self.health), 2))    
    
    def health_bar_len(self, current_health):
        max_bar_len = 15 # maximum length of health bar regardless of health points
        current_health_bar = int(self.health/self.max_health * max_bar_len)
        if current_health_bar < 0:
            current_health_bar = 0
        return(current_health_bar)
    
    def get_image(self,path):
        global _image_library
        image = _image_library.get(path)
        if image == None:
                canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
                image = pygame.image.load(canonicalized_path)
                _image_library[path] = image
        return image
       

class Tile:
    """ - terrain class of sprite objects to populate grid 
        - created by Tile_grid group object 
        - eventually add additional terrain types
    """
    def __init__(self):
        self.terrain_type = "grass"
        self.color = MDW_GREEN
        self.alt_color = GREEN
        self.selected = False
        self.contents = []
        self.passable = True
        self.altitude = 3 # 0: lowest 3: sealevel 6: highest
        self.movement_cost = 2

################################################################################
class TileGrid:
    """ class for constructing gamespace of tiles terrain in a 2d grid """
    def __init__(self, screen):
        """ screen: screen window for display
        """
        self.nrows = int(FIELD_RECT[2]/TILE_SIZE) # number of horizontal grid spaces in grid map
        self.ncols = int(FIELD_RECT[3]/TILE_SIZE) # number of vertical grid spaces in grid map
        self.matrix = [[0 for i in range(self.ncols)] for i in range(self.nrows)] # 2-d array of tiles
        self.screen = screen
        self.last_clicked =(-1,-1)# coord for last tile clicked 
        self.fill_grid() # fill matrix with individual tiles
        self.pawn_group = UnitGroup(screen) # adds group of units from unit_simp
    
    @staticmethod
    def rnd_targ_tile():
        """ select a random target tile for movement for a single unit """
        x = randint(1, int(FIELD_RECT[2]/(TILE_SIZE + MARGIN))-1)
        y = randint(1, int(FIELD_RECT[3]/(TILE_SIZE + MARGIN))-1)
        print(x,y)
        return(x,y)
        
    def fill_grid(self): 
        """ fill up space in grid with an individual tile """
        for row in range(0, self.nrows):
            for col in range(0, self.ncols):
                self.matrix[row][col] = Tile()            
    
    @staticmethod
    def is_grid_empty(grid, next_loc, unit):
        """ returns True if next_loc is populated """
        tile = grid.matrix[unit.loc[0]][unit.loc[1]]
        new_tile = grid.matrix[unit.loc[0]][unit.loc[1]]
        if new_tile.contents == [] or new_tile.contents == unit or new_tile == unit.loc:
            #print("unit", unit.unit_no, ": tile empty")
            dummy = False
            return(True)
        else:
            #print("unit", unit.unit_no, ": space not free, waiting until later to move")
            dummy = False        
            for element in new_tile.contents:
                #print("unit", unit.unit_no, ": space contains:", element.loc, element.unit_no)
                dummy = False
            return(False)
    
#     def is_grid_passable(self,grid, next_loc):
#         """ returns True if next_location is passable 
#             grid: name of Tile_grid
#             next_loc: target location
#         """
#         return(True)
    
        
    def update_grid(self): 
        ''' primary grid update method '''
        self.update_unit_pos()
        for row in range(self.nrows):
            for col in range(self.ncols):
                #check to see if tile is active or not to determine color and assign
                # to curser_color
                if self.matrix[row][col].selected == False: 
                    curser_color = self.matrix[row][col].color
                else: 
                    curser_color = self.matrix[row][col].alt_color
                pygame.draw.rect(  self.screen,
                                   curser_color,
                                   [(FIELD_RECT[0] + row * (TILE_SIZE + MARGIN)),
                                    (FIELD_RECT[1] + col * (TILE_SIZE + MARGIN)),
                                    TILE_SIZE,
                                    TILE_SIZE] )
        
    def update_unit_pos(self): 
        # reconfigure grid with new unit locations
        dummy = False
        
    #### Grid Helper Utilities   
    
    def coord_to_grid(self, pos):
        """ returns grid location based on sprite pos(x,y) for test purposes of 
            clicked location 
        """
        coord = (  int((pos[0] - FIELD_RECT[0]) / (TILE_SIZE + MARGIN)),
                           int((pos[1] - FIELD_RECT[1]) / (TILE_SIZE + MARGIN)))
        #print(  "click pos:", pos, " grid pos:", self.selected)        
        return(coord)
    
    def in_field(self, pos):
        """ verify if clicked pos is in playable grid area  - returns True/False """
        loc = self.coord_to_grid(pos)
        if loc[0] < 0 or loc[0] >= GRID_SIZE[0] or \
           loc[1] < 0 or loc[1] >= GRID_SIZE[1]:
            #print("you missed the grid")
            return(False)
        else:
            return(True)
        
    def grid_clicked(self, pos):
        """ tells what grid was clicked on and reports for testing purposes 
            pos: the passed mouse coordinates variable passed through 
        """
        if self.in_field(pos):
            #print("click is in field")
            #print("pos clicked:", pos)
            loc = self.coord_to_grid(pos)
            if self.pawn_group.is_unit_in_grp_selected(self.coord_to_grid(pos)): # NOT WORKING - does not correctly identify tile location with mouse click
                #print("someone in this group was clicked on")
                dummy = False #                                                  - ADD things when a unit gets clicked on
            elif self.matrix[loc[0]][loc[1]].selected == False: #toggles selected to True
                self.matrix[loc[0]][loc[1]].selected = True
                #print("toggled tile from false to true at this loc", loc)
            else: #toggles selected to True
                self.matrix[loc[0]][loc[1]].selected = False
                #print("toggled tile from true to false")
                                
    def print_grid(self):
        """ prints text version of grid to shell """
        self.matrix[1][1].selected = True
        for row in range(0, self.nrows):
            col_output = ""
            for col in range(0, self.ncols):
                if self.matrix[row][col].contents != []:
                    col_output += " u"
                elif not self.matrix[row][col].contents and \
                         self.matrix[row][col].terrain_type == "water":
                    col_output += " -"
                else: #default is grass
                    if self.matrix[row][col].selected == True:
                        col_output += " S"
                    else:
                        col_output += " ."
            print(col_output)
            print()      
        
    #def is_adjacent(self,new_coord): #NOTE: not currently using - old parameters
        #if new_coord[0] < self.coord[0] - 1 or new_coord[0] > self.coord[0] + 1 or new_coord[1] < self.coord[1] - 1 or new_coord[1] > self.coord[1] + 1:
            #print("not adjacent")
            #return(False)
        #elif new_coord  == self.coord:
            #print("already there")
            #return(False)
        #else:
            #return(True)
       
class UnitGroup(object):
    """ a group of units """
    
    UNIT_START_QTY = 2 # number of starting army units under player control
    
    def __init__(self, screen, total = UNIT_START_QTY):
        """ total: number of units in group to be created (default is variable)
        """
        self.group_list = [] # create container to hold individual units for player's group
        self.Simp_unit_group_fill(screen, total) # create units
        
    def assign_unit_g_targ_tile(self, new_targ):
        """ pass units to be adjusted for targ_tile """
        for unit in self.group_list:
            if unit.active:
                unit.assign_unit_targ_tile(new_targ)
    
    def Simp_unit_group_fill(self, screen, total = UNIT_START_QTY):
        """ fill unit group with initial units 
            total: number of units in group to be created (default is variable)
        """
        for i in range(0, UnitGroup.UNIT_START_QTY):
            new = Unit(screen, unit_no = i)
            self.group_list.append(new)
        #print("group:", self.group_list)
        
    def assign_group_color_units(self, player_color):
        for unit in self.group_list:
            unit.assign_unit_color_units(player_color)
            #print("unit: ", unit)
        #print("group:", self.group_list)

    def is_unit_in_grp_selected(self, coord):
        """ check to see if any unit in group was clicked to make active 
            coord: mouse click coordinates
        """
        for unit in self.group_list:
            if unit.is_unit_selected(coord): 
                #print("hey, you got one!")
                return(True)
            
    def update_group(self): # Not using this at this point
        """ updating a group and outputing to screen """
        #print("Updating a group of units")
        
    def player_window_group_update(self, player_command_window):
        """ update unit group info to player_command window for active player """
        for unit in self.group_list:
            unit.prep_unit_text_info()
        player_command_window.draw_player_units(unit.screen, self.group_list) # send self.group_list to player_command for window outpu
        
class PlayerUnitGroup(object):
    """ Container class to hold unit groups for each player """
    
    def __init__(self, screen, ttl_players = players_start_qty):
        self.players = [] # list of players
        self.active_list = []
        self.create_player_group(screen, ttl_players)
        self.acquire_targ_tile()
        self.ttl_players = ttl_players
        
    def acquire_targ_tile(self):
        """get random targ_tile for units"""
        for player in self.players:
            if not player.active:
                for group_list in player.units:
                    for unit in group_list.group_list:
                        if unit.targ_tile == unit.loc:
                            unit.targ_tile = TileGrid.rnd_targ_tile()
                #print("here's a player not in the active list", player)    
    
    def assign_player_grp_targ_tile(self, new_targ): 
        """ pass player to be adjusted for targ_tile """
        for player in self.active_list:
            player.assign_player_targ_tile(new_targ)
    
    def create_player_group(self, screen, ttl_players):
        """ method for creating all players """
        make_player_active = False
        for player in range(0,ttl_players):
            #print("here's a player")
            new = Player(screen)
            self.players.append(new)
        self.players[0].active = True # mark which group units go to output window - TEMP ONLY - works for 1st player only
        self.players[0].side = True # mark 1st player as True = side_a (all else default to side_b)
        self.active_list.append(self.players[0]) # add player to active player list
        #print("player active check. player 1:", self.players[0].active, "   player 2:", self.players[1].active)

    def print_all_player_units(self):
        """ test to print to shell all units of all teams """
        for player in self.players:
            player.print_player_units()
            
    def update_players(self, player_command_window, grid, melee_engine):
        """ update players and print to screen """
        melee_engine.update_melee()
        for player in self.players:
            player.update_player()
            if player.active == True:
                """ print unit status to player_command window """
                for unit_group in player.units:
                    unit_group.player_window_group_update(player_command_window)
                    



################################################################################

class MeleeEngine():
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

#     def melee(melee_pair):
#         """ computes battle between 2 units """
#         side1 = melee_pair[0]
#         side1_team = melee_pair[1]
#         side2 = melee_pair[2]
#         side2_team = melee_pair[3]
#         print("melee pairs:", side1, side2)
#         # determine initiative
#         initiative_roll_a = initiative_roll(side1)
#         initiative_roll_b = initiative_roll(side2)
#         print("innitiative rolls:", initiative_roll_a, initiative_roll_b)
#         
#         if initiative_roll_a > initiative_roll_b:
#             print("side a opponent receives initiative")
#             attack_round_pair(  melee_pair, 
#                                 attacker = side1, 
#                                 attacker_group = side1_team, 
#                                 defender = side2, 
#                                 defender_group = side2_team,
#                                 hero_is_attacker = True)
#             
#         elif initiative_roll_b > initiative_roll_a:
#             print("side b opponent receives initiative")
#             attack_round_pair(  melee_pair, 
#                                 attacker = side2, 
#                                 attacker_group = side2_team, 
#                                 defender = side1, 
#                                 defender_group = side1_team, 
#                                 hero_is_attacker = False)
#         else:
#             print("no one prevails but peace... life finds a way...")

            
#     def attack_round_pair(self,melee_pair, attacker, attacker_group, defender, defender_group, hero_is_attacker):   
#         attacker_roll_a = attacker_roll(attacker) # determine attack bonus & roll
#         defender_roll_b = defender_roll(defender) # determine defense bonus & roll
#         attacker.stats["swings"] +=1
#         print("attack & defense rolls:", attacker_roll_a, defender_roll_b)
#         # determine winner/loser and consequences
#         if attacker_roll_a > defender_roll_b: # attacker wins
#             print("attacker is victorious")
#             attacker_group.wins += 1
#             attacker.stats["melee_won"] += 1
#             attacker.in_melee = False
#             units.MELEE_LIST.remove(melee_pair) 
#             if defender in defender_group.group_list: # verify that defender has not already been removed
#                 defender_group.group_list.remove(defender)
#             if hero_is_attacker:
#                 messages.HERO_WINS += 1
#             else:
#                 messages.ENEMY_WINS += 1
#                 
#         else: #defender wins tie
#             print("defender stops the attack and counters")
#             # do counter attack
#             attacker_roll_a = attacker_roll(defender)
#             defender_roll_b = defender_roll(attacker)
#             defender.stats["swings"] +=1
#             
#             
#             
#             ######################################################################## LEFT OFF HERE #########################################################################3
#             units.MELEE_LIST.remove(melee_pair)
#             if attacker_roll_a > defender_roll_b: # counterattack wins
#                 print("defender's counterattack overcomes attacker")
#                 defender_group.wins += 1
#                 #attacker_group.removal_list.append(attacker)
#                 #attacker_group.remove_unit(attacker)
#                 if attacker in attacker_group.group_list: # verify that attacker has not already been removed
#                     attacker_group.group_list.remove(attacker)            
#                 defender.stats["melee_won"] += 1
#                 defender.in_melee = False
#                 if not hero_is_attacker:
#                     messages.ENEMY_WINS += 1
#                 else:
#                     messages.HERO_WINS += 1
#                     
#             else: # defender vs counterattack wins - including tie
#                 print("counterattack failed - they live to fight again")
#                 attacker.in_melee = False
#                 defender.in_melee = False
#                 
#         #print() 
#         print("attacker_wins:", attacker_group.wins, "   defender wins:", defender_group.wins)
#         
#         #print("Hero:", win_score.hero_wins, "  Enemy:", win_score.enemy_wins)
#         #print()

    def do_melee(self, melee_pair):
        """ process single round of melee of melee_groups pairs """
        print("melee_pair from do_melee", melee_pair)
        self.prep_melee(melee_pair)
        
        # NOTE: remove winning unit from inactive status so can move again
        # NOTE: set defeated units to dead so can't move or do anything & update image file
        # NOTE: only let unit swing the number of attack swings they have - after that they can only defend swing        
        for unit in melee_pair:
            unit.in_melee = False
        
    def prep_melee(self, melee_pair):
        """ set up initiative & sides variables """
        side_1 = melee_pair[0]
        side_2 = melee_pair[1]
        print("melee pairs:", melee_pair, side_1, side_2)
        
        for thing in side_1: 
            print("side_1 thing", thing)
        print("melee_pair len:", len(melee_pair))

        
        # determine initiative
        initiative_roll_a = MeleeEngine.initiative_roll(side_1)
        initiative_roll_b = MeleeEngine.initiative_roll(side_2)
        print("innitiative rolls:", initiative_roll_a, initiative_roll_b)
        
        if initiative_roll_a > initiative_roll_b:
            print("side a opponent receives initiative")
            MeleeEngine.attack_round_pair(  melee_pair, 
                                            attacker = side_1, 
                                            #attacker_group = side1_team, 
                                            defender = side_2, 
                                            #defender_group = side2_team,
                                            hero_is_attacker = True)
            
        elif initiative_roll_b > initiative_roll_a:
            print("side b opponent receives initiative")
            MeleeEngine.attack_round_pair(  melee_pair, 
                                            attacker = side_2, 
                                            #attacker_group = side2_team, 
                                            defender = side_1, 
                                            #defender_group = side1_team, 
                                            hero_is_attacker = False)
        else:
            print("no one prevails but peace... life finds a way...")  
            

    def attack_round_pair(self,melee_pair, attacker, defender, hero_is_attacker):  
        # determine attack bonus & roll
        attacker_roll_a = MeleeEngine.attacker_roll(attacker)
        # determine defense bonus & roll
        defender_roll_b = MeleeEngine.defender_roll(defender)
        attacker.stats["swings"] +=1
        print("attack & defense rolls:", attacker_roll_a, defender_roll_b)
        # determine winner/loser and consequences
        if attacker_roll_a > defender_roll_b: # attacker wins
            print("attacker is victorious")
            #attacker_group.wins += 1
            attacker.stats["melee_won"] += 1
            attacker.in_melee = False
            #units.MELEE_LIST.remove(melee_pair) 
            #if defender in defender_group.group_list: # verify that defender has not already been removed
                #defender_group.group_list.remove(defender)
#             if hero_is_attacker:
#                 messages.HERO_WINS += 1
#             else:
#                 messages.ENEMY_WINS += 1
                 
        else: #defender wins tie
            print("defender stops the attack and counters")
            # do counter attack
            attacker_roll_a = MeleeEngine.attacker_roll(self,defender)
            defender_roll_b = MeleeEngine.defender_roll(self,attacker)
            defender.stats["swings"] +=1    

    def attacker_roll(self, unit):
        roll = dice.diceroll(die_tries = 3)
        bonus = (unit.attack * unit.gov_attack) + (unit.speed/2*unit.gov_speed)
        roll += bonus
        return(roll)
#         
    def defender_roll(self, unit):
        #roll = ((randint(0,10) + randint(0,10) + randint(0,10))/3)
        roll = dice.diceroll(die_tries = 3)
        bonus = (unit.defense * unit.gov_defense) + (unit.speed/2 * unit.gov_speed)
        roll += bonus
        return(roll)
    
    @staticmethod  
    def initiative_roll(unit):
        roll = dice.diceroll()
        #bonus = unit.gov_initiative + (unit.speed/2* unit.gov_initiative)
        bonus = 1
        roll += bonus
        return(roll)
       


class Player:
	
    """ Player class """
    def __init__(self, screen):
        self.name = "Player Name"
        self.units = [] # list in which each element is a group of units
        self.create_player_units(screen)
        self.color = choice(player_colors)
        while self.color_been_picked():
            self.color = choice(player_colors)
        self.assign_player_color_units()
        self.active = False # connects player's team with the player controlling the game computer (only 1 player is active to a computer station)
        self.side = False # False: non-player, True: player's team
        self.score = 0

    def assign_player_targ_tile(self, new_targ):  
        """ pass player to be adjusted for targ_tile """
        for unit_group_list in self.units:
            unit_group_list.assign_unit_g_targ_tile(new_targ)
    
    def assign_player_color_units(self):
        """ set unit icons to player color """
        for group in self.units:
            group.assign_group_color_units(self.color)
        
    def color_been_picked(self):
        """ see if color is already used, if so, return True else return False """
        for used_color in used_player_colors:
            if self.color == used_color:
                return(True)
        used_player_colors.append(self.color)
        return(False)
        
    def create_player_units(self, screen):
        #new = Simp_unit_group(screen, self) # create a group of units #         NOTE: This line doesn't seem to need self in parameters.
        new = UnitGroup(screen) # create a group of units
        self.units.append(new)
        
    def print_player_units(self):
        print("Player:", self.name)
        for group in self.units:
            for unit in group.group_list:
                print("unit loc:", unit.loc)
                
    def update_player(self):
        """ update player """
        # do whatever is necessary to update the player
        #print("updating player")
        for group in self.units:
            for unit in group.group_list:
                unit.update_unit()
                
# class UserEvents:
#     def __init__(self, screen):
#         """ screen: screen  """
#         self.screen = screen
#         
#     def do_usr_input(self, pos):
#         """ determine action based upon mouse & kbd input 
#             pos: mouse position coordinates
#         """
#         dummy = False
#         #print("usr_events is connected.") # - works
#         #if grid_map.in_field(pos): # Check to see if click was in grid field for testing 
#             #grid_map.grid_clicked(pos)
#         if grid.in_field(pos): # Check to see if click was in grid field for testing 
#             grid.grid_clicked(pos)      

class PlayerCommand:
    """ Display pannel for player input/output
        Controls display area for player input/output """
    
    def __init__(self):
        self.msg1 = "text area 1"
        self.msg2 = "text area 2"
        self.msg3 = "text area 3"
        self.x = 50
        self.width = 20
        self.offset = 0
        self.back_color = "black"
        self.message_rect = Rect(600, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
        self.message_size = (int(self.message_rect[2])-self.message_rect[0], int(self.message_rect[3]))
        self.unit_group_rect = Rect(630, 150, 15, 15)
        self.player_msg = "Player message here"
        self.tick_counter = "Ticks here"
        
    def msg_to_player(self, screen):
        """ tracks and handles messages to player """
        message1_sf = DEFAULT_GAME_FONT.render(self.player_msg, True, Color('white'))
        screen.blit(message1_sf, (20, 550, SCREEN_WIDTH, SCREEN_HEIGHT))
        """ tick counter """
        message2_sf = DEFAULT_GAME_FONT.render(self.tick_counter, True, Color('white'))
        screen.blit(message2_sf, (20, 20, SCREEN_WIDTH, SCREEN_HEIGHT))        
        
    def draw_messageboard(self, screen):
        self.draw_rimmed_box(screen, self.message_rect, (self.x, self.width, self.offset), 4, Color(self.back_color))
        DEFAULT_GAME_FONT = pygame.font.SysFont('arial', 18)
        message1_sf = DEFAULT_GAME_FONT.render(self.msg1, True, Color('white'))
        message2_sf = DEFAULT_GAME_FONT.render(self.msg2, True, Color('white'))
        message3_sf = DEFAULT_GAME_FONT.render(self.msg3, True, Color('white'))
        message4 = "Heroes: " + str(HERO_WINS)
        message4_sf = DEFAULT_GAME_FONT.render(message4, True, Color('white'))
        message5 = "Enemies: " + str(ENEMY_WINS)  
        message5_sf = DEFAULT_GAME_FONT.render(message5, True, Color('white'))
        screen.blit(message1_sf, self.message_rect.move(0, message1_sf.get_height()))
        screen.blit(message2_sf, self.message_rect.move(0, message2_sf.get_height()*2))  
        screen.blit(message3_sf, self.message_rect.move(0, message2_sf.get_height()*3))  
        screen.blit(message4_sf, self.message_rect.move(0, message4_sf.get_height()*4))  
        screen.blit(message5_sf, self.message_rect.move(0, message5_sf.get_height()*5))  
        self.msg_to_player(screen)
        
    def draw_player_units(self, screen, unit_group):
        """ blits player unit text to output display window """
        self.draw_rimmed_box(screen, Rect(600, 150, 
                            SCREEN_WIDTH, SCREEN_HEIGHT), 
                             (self.x, self.width, self.offset), 
                             4, 
                             Color(self.back_color))
        DEFAULT_GAME_FONT = pygame.font.SysFont('arial', 12)
        offset = 0
        for unit in unit_group:
            message1_sf = DEFAULT_GAME_FONT.render(unit.info_msg1, True, Color('white'))
            message1_status = DEFAULT_GAME_FONT.render(unit.txt_status, True, Color('white'))
            message2_sf = DEFAULT_GAME_FONT.render(unit.info_msg2, True, Color('white'))
            screen.blit(message1_sf, self.unit_group_rect.move(0, message1_sf.get_height()*1 + offset*24))
            screen.blit(message1_status, self.unit_group_rect.move(100, message1_status.get_height()*1 + offset*24))
            screen.blit(message2_sf, self.unit_group_rect.move(0, message2_sf.get_height()*2 + offset*24))
            for button in unit.unit_btns:
                button.draw(screen)
            offset += 2
        
    def draw_rimmed_box(self, screen, box_rect, box_color, 
                        rim_width=0, 
                        rim_color=Color('black')):
        """ Draw a rimmed box on the given surface. 
            The rim is drawn outside the box rect. 
        """
        if rim_width:
            rim_rect = Rect(box_rect.left - rim_width,
                            box_rect.top - rim_width,
                            box_rect.width + rim_width * 2,
                            box_rect.height + rim_width * 2)
            pygame.draw.rect(screen, rim_color, rim_rect)
        pygame.draw.rect(screen, box_color, box_rect)
   
    def in_field(self, pos):
        """ verify if clicked pos is in playable grid area  - returns True/False """
        loc = self.coord_to_grid(pos)
        if loc[0] < 0 or loc[0] >= self.x or loc[1] < 0 or \
           loc[1] >= GRID_SIZE[1]:
            #print("you missed the player_command grid")
            return(False)
        else:
            return(True)
    
    def grid_clicked(self, pos):
        """ tells what grid was clicked on and reports for testing purposes 
            pos: the passed mouse coordinates variable passed through 
        """
        if self.in_field(pos):
            #print("click is in player_command field")
            #print("pos clicked:", pos)
            dummy = False

################################################################################
## TEST
################################################################################
# 
# if __name__ == "__main__":  
#     
#     screen = pygame.display.set_mode((params.SCREEN_WIDTH, params.SCREEN_HEIGHT), 0, 32) # create screen area for tiles
# 
#     #pawn = SimpleUnit() 
#     pawn_group = SimpleUnitGroup(screen)
#     for unit in pawn_group.group_list:
#         print("unit loc:", unit.loc)
#     #test loop to give coords to units
#     for unit in pawn_group.group_list:  
#         unit.targ_tile = (25,25)
#         unit.active = True
#         print("status:") # test of status message update
#         print(unit.info_msg1) # test of status message update
#         print(unit.info_msg2) # test of status message update
#     #test loop to move units    
#         unit.move_unit()
#     for unit in pawn_group.group_list: # check locations again to see if moved
#         print("unit loc:", unit.loc)     
#         
#     # test player groups - test works #
#     all_players = PlayerUnitGroup(screen) #                         - These lines are the lines to call/create the players & units for a game
#     
#     all_players.print_all_player_units() # Test to print all player units to shell - works
#     
#     all_players.update_players() # Test of update logic path
#     
#     print()
#     print("-- TEST DONE --")
#     print()
#     pygame.quit()
#     sys.exit()