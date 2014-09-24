################################################################################
##  NOTES Alpha copy
################################################################################
"""
Primary pages:

battle_grid.py
    Run this. This page will run the battle sequences and make calls to other pages/classes/methods. Right now it has mostly a dummy background
    and files for testing purposes.
    
units.py
    This file contains the parent and child classes for all units and unit groups, both hero and enemy (which can swap sides, by the way).
    
obstacle.py
    Parent and child classes for passable and non-passable non-player/npc objects

messages.py
    Contains lists of messages and responses for various situations, including academy/training names, player name generation, town name
    generation.

images_lib.py
    Contains calls to images for the game. Most of the images are currently fpo, but the real ones will reside here as well.
    
grid_map.py
    Contains the terrain grid class, which tracks specific terrain type, altitude, (adjusts terrain color by altitude), contents, and so on.
    
params.py
    Contains a short bit of code that most files need in their testing code

dice.py
    Utility for rolling various combinations of straight and weighted random rolls


Utilities to consider implementing or developing:

    makes dragable surfaces for buttons and such - example
    http://pygame.org/project-planes-2392-.html
    
    tile map generator example
    http://pygame.org/project-pyMap+-+2D+Tile+Mapping-2769-.html
    
    popup menu creator - example
    http://pygame.org/project-Simple+Pygame+Menu-1709-.html
    
    a text button class - example
    http://pygame.org/project-TextWidget-897-.html
    
    simple forms creator - example
    http://pygame.org/project-Pygame+Forms-1042-.html
    
    clickable menu and buttons class - example
    http://pygame.org/project-MenuClass-1260-.html
    
    font manager - example
    http://www.pygame.org/wiki/SimpleFontManager?parent=CookBook
    
    astar - pathfinding algorithm
    http://www.pygame.org/project-AStar-195-.html
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
"""    