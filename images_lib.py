################################################################################
## images_lib
################################################################################

import pygame

################################################################################
## Colors

BLACK     = (   0,   0,   0)
LT_GRAY   = ( 214, 214, 214) # road
WHITE     = ( 255, 255, 255)
GREEN     = (   0, 255,   0)
RED       = ( 255,   0,   0)
MDW_GREEN = (   0, 128,   0) # meadow
MDW_BROWN = ( 212, 181, 116) # woods
MDW_BLUE  = ( 124, 147, 252) # water

GRASS     = (   0, 128,   0) # grass color & terrain type

"""
NOTE: for grid purposes, use terrain type name as the corresponding color name

"""

################################################################################


class Image_lib(object):
    def __init__(self):
        """ lists and converts all images for game """
        #main screen background tile
        #self.BG_TILE_IMG = "images/brick_tile.png"
        
        self.BATTLE_GRID_IMG = "images/Background-Image.png"
        self.battle_grid_img = pygame.image.load(self.BATTLE_GRID_IMG).convert_alpha() 
        
        self.BG_TILE_IMG = "images/blue_tile.png"
        self.bg_tile_img = pygame.image.load(self.BG_TILE_IMG).convert_alpha()
        
        self.MSG_TILE_IMG = "images/brown_tile.png"
        self.msg_tile_img = pygame.image.load(self.MSG_TILE_IMG).convert_alpha()
        
        self.BLUE_CREEP_IMG = "images/bluecreep.png"
        self.blue_creep_img = pygame.image.load(self.BLUE_CREEP_IMG).convert_alpha()
        
        self.BLUE_PAWN_IMG = "images/bluepawn.png"
        self.blue_pawn_img = pygame.image.load(self.BLUE_PAWN_IMG).convert_alpha()
        
        self.HAT_PAWN_IMG = "images/pawn_6b.png"
        self.hat_pawn_img = pygame.image.load(self.HAT_PAWN_IMG).convert_alpha()        
        
        self.RED_DOT_IMG = "images/red_dot.png"
        self.red_dot_img = pygame.image.load(self.RED_DOT_IMG).convert_alpha()
        
        self.PAWN_BIG_IMG = "images/pawn_big.png"
        self.pawn_big_img = pygame.image.load(self.PAWN_BIG_IMG).convert_alpha()   
        
        self.WALL_IMG = "images/gray_brick.png"
        self.wall_img = pygame.image.load(self.WALL_IMG).convert_alpha()    
        
        self.TERRAIN_PLAINS_IMG = "images/terrain_plains.png"
        self.terrain_plains_img = pygame.image.load(self.TERRAIN_PLAINS_IMG).convert_alpha()  
        
        self.TERRAIN_WATER_IMG = "images/terrain_water.png"
        self.terrain_water_img = pygame.image.load(self.TERRAIN_WATER_IMG).convert_alpha()  
        
        self.TERRAIN_WOODS_IMG = "images/terrain_water.png"
        self.terrain_woods_img = pygame.image.load(self.TERRAIN_WOODS_IMG).convert_alpha()   
        

