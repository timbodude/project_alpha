################################################################################
## battle_grid revision 140725.0320
################################################################################

import pygame
from pygame import Rect, Color
from pygame.sprite import Sprite
import my_clock
import os, sys
#from simpleanimation import SimpleAnimation
from random import randint, choice
from vec2d import vec2d
import messages
from images_lib import Image_lib
import message_board
import main_board
import units
import unit_combat
import obstacle
from obstacle import Wall_group
import grid_map
from params import TURN_COUNT



################################################################################

def run_game():
    
    pygame.init()
    import params # Game parameters
    import combat # combat modules

    screen = pygame.display.set_mode((params.SCREEN_WIDTH, params.SCREEN_HEIGHT), 0, 32)
    #paused = False
    #won = False
    
    #grid_board = grid_map.Grid_map(screen) # pre_create all in grid_map class
    #new_alt = grid_map.Gml_altitude(screen, 5 , 5) # pre_create all in grid_map class
    
    
    grid_board = grid_map.Grid_map(screen) #                                    * REQUIRED CALL TO CREATE GRIDMAP
    grid_board.create_gml #                                                     * REQUIRED CALL TO CREATE GRIDMAP    

    image_lib = Image_lib() # setup all images from image library               * This must be added for images to appear
    
    #setup clock
    clock = pygame.time.Clock() #                                               * This line must be in the program for timer to run
    time = my_clock.Time_clock() #                                              * This line must be in the program for timer to run 
    my_clock.et_group = my_clock.Et_group() #                                   * This line must be in the program        
    
    ######################################################### from creep to test
    # Game parameters
    SCREEN_WIDTH = params.SCREEN_WIDTH
    SCREEN_HEIGHT = params.SCREEN_HEIGHT
    FIELD_RECT = params.FIELD_RECT
    MESSAGE_RECT = params.MESSAGE_RECT
    
    #bg_tile_img = image_lib.bg_tile_img
    bg_tile_img = image_lib.battle_grid_img
    time_count = 0
    
    paused = params.paused
    won = params.won
    
    #################################################### TEST lines for grid_map """ these should be taked care of within class """
    
    # TESTING THESE 
    gml_unit = grid_map.Gml_units(screen)
    gml_alt = grid_map.Gml_altitude(screen)
    gml_alt.print_alt_map() # TEST OUTPUT
    gml_color = grid_map.Gml_color(screen)
    for row in range(0, grid_board.nrows):
        for col in range(0, grid_board.ncols):
            gml_color.grid[row][col] = gml_color.adj_color(grid_board.grid[row][col], gml_alt.grid[row][col])
            #print("adjusted color:", gml_color.grid[row][col])  
    gml_event = grid_map.Gml_event(screen)     
    
   
    ######################################################## Test unit functions
    
    #units
    micro_units = units.Unit_group(screen)
    max_units = 0
    for unit_num in range(0, max_units):
        micro_units.add_unit(screen, "unit")
    for unit in micro_units.group_list:
        unit.base_image = image_lib.hat_pawn_img
    units.HERO_LIST.append(micro_units)
    
    #creeps    
    micro_creep = units.Creep_group(screen)
    max_creep = 1
    for unit_num in range(0, max_creep): 
        micro_creep.add_unit(screen, "creep")
    for unit in micro_creep.group_list:
        unit.base_image = image_lib.red_dot_img
        #unit.image = image_lib.red_dot_img
        #print("Name: ", unit.names.get("name"))
    units.ENEMY_LIST.append(micro_creep)
    
    #pawns
    micro_pawns = units.Pawn_group(screen)
    max_pawns = 1
    for unit_num in range(0, max_pawns):
        micro_pawns.add_unit(screen, "unit")
    for unit in micro_pawns.group_list:
        unit.base_image = image_lib.blue_pawn_img 
    units.HERO_LIST.append(micro_pawns)
    
    
    #big_pawns
    micro_big_pawns = units.Big_pawn_group(screen)
    max_pawns = 0
    for unit_num in range(0, max_pawns):
        micro_big_pawns.add_unit(screen, "big_pawn")
    for unit in micro_big_pawns.group_list:
        unit.base_image = image_lib.pawn_big_img 
    units.HERO_LIST.append(micro_big_pawns)
    
    ##obstacles
    micro_walls = Wall_group(screen)
    max_walls = 0
    for obstacle_num in range(0, max_walls):
        micro_walls.add_obstacle(screen, "wall")
    for obstacle in micro_walls.group_list:
        obstacle.base_image = image_lib.wall_img
            

    #for group in units.ALL_OBSTACLES_GROUPS:
        #print("Hey, there's an obsticle group")
        #for obstacle in group.group_list:
            #print("Found an obstacle.")

################################################################################        

# The main game loop

    while True:
        time_passed = clock.tick(50) # Limit frame speed to 50 FPS
        
        #if paused == False and len(creeps) != 0:
        if params.paused == False:    
            time.tick()
        
        # handle user events ###################################################  
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    params.paused = not params.paused
            #elif (  event.type == pygame.MOUSEBUTTONDOWN and
                    #pygame.mouse.get_pressed()[0] and
                    #params.paused != True):
                #dummy = False
                
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if (  pygame.mouse.get_pos()[0] >= params.FIELD_RECT[0] and
                      pygame.mouse.get_pos()[0] <= params.FIELD_RECT[2] + params.FIELD_RECT[0] and
                      pygame.mouse.get_pos()[1] >= params.FIELD_RECT[1] and
                      pygame.mouse.get_pos()[1] <= params.FIELD_RECT[3]) + params.FIELD_RECT[1] :
                    # if clicked within grid_map:
                    print("clicked in grid_map area!")
                    pos = pygame.mouse.get_pos()
                    print("mouse clicked:", pos)
                    grid_board.click_on_grid(pos)
                else:
                    print("click not in clickable area")
                
            
            # 
                #for creep in creeps:
                    #creep.mouse_click_event(pygame.mouse.get_pos())
                #for pawn in pawns:
                    #pawn.mouse_click_event(pygame.mouse.get_pos())                    
                    
        if not params.paused:
            #draw_background(screen, image_lib.bg_tile_img, FIELD_RECT) # Redraw the background
            #main_board.draw_background(screen, image_lib.bg_tile_img, params.FIELD_RECT) # Redraw the background
            main_board.draw_background(screen, image_lib.battle_grid_img, params.FIELD_RECT) # Redraw the background - WORKS
            #grid_board.update_grid() - worked
            grid_board.update_grid()
            
            # reset messages & update screen region ############################
            #msg1 = 'Creeps: %d' % len(creeps)
            msg1 = "Creeps: "
            
            #msg2 = 'You won!' if len(creeps) == 0 else ''
            #msg2 = 'You won!' if won == True else ''
            if time.time_count > 150 and params.end_check == False:
                params.won = True
                msg2 = choice(messages.win)
                params.end_check = True
            elif time.time_count <= 150 :
                params.won = False            
                msg2 = messages.playing
            
            #msg3 = post_clock(time_count)
            msg3 = time.post_clock()
            
            #draw_messageboard(screen, MESSAGE_RECT, msg1, msg2, msg3)
            message_board.draw_messageboard(screen, params.MESSAGE_RECT, msg1, msg2, msg3)
            
            #update and redraw elements
            
            ################################################ Update units

            #update units
            for group in units.ALL_UNIT_GROUPS:
                for unit in group.group_list:
                    unit.update(time_passed)
                    unit.draw() 
                    
            for group in units.ALL_OBSTACLES_GROUPS:
                for obstacle in group.group_list:
                    obstacle.update(time_passed)
                    obstacle.draw()         
            
            #check for collisions with units
            #for hero_group in units.HERO_LIST:
                #if hero_group: # make sure there is a hero group
                    #print("there is a group of heroes.")  
                    #hero_group.los_check(hero_group) # check for LOS
                    #hero_group.collision_check(hero_group)
            #for melee_pair in units.MELEE_LIST:
                #combat.melee(melee_pair)
                
            ##check for collisions between wall & units
            #for obstacle_group in obstacle.ALL_OBSTACLE_GROUPS:
                #if obstacle_group: # make sure there is an obstacle group
                    ##print("there are obstacles")  
                    #obstacle_group.collision_check(obstacle_group)
            
            #clear out empty opponent list
            units.unit_lists_empty_check() 
            #obstacle.obstacle_lists_empty_check()
        
        ################################################ Refresh screen
        pygame.display.flip() # Update and redraw everything


def exit_game():
    print()
    units.print_all_stats()
    print("-- Done --") 
    print()    
    pygame.quit()
    sys.exit()


run_game()
