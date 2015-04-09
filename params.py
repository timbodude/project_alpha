""" set global params for tests before parent window (Battle_grid) was built

    NOTE:
    This information will be moved to the my_main.py page and should be 
    drawn from there if needed.
    
    NOTE #2: I'm (Tim) still using this file occasionally for globals in test runs

"""
from pygame import Rect, font
from PygButton import Btn_grp


SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600

FIELD_RECT = Rect(0, 0, 600, 600)
MARGIN = 1
TILE_SIZE = 23 # planned so far
GRID_SIZE = (int(FIELD_RECT[2]/(TILE_SIZE + MARGIN)), 
             int(FIELD_RECT[3]/(TILE_SIZE + MARGIN)))

#MESSAGE_RECT = Rect(600, 0, 800, 600) #                                         Eliminated - moved to player_command
#MESSAGE_SIZE = (int(MESSAGE_RECT[2])-MESSAGE_RECT[0], int(MESSAGE_RECT[3])) #   Eliminated - moved to player_command
end_check = False
paused = False
won = False # flag for battle is over
TICK = 0
GAME_ROUND = 1
GAME_SPEED = 50 * GAME_ROUND
buttons = Btn_grp()
my_font = font.SysFont('arial', 24)

################################################################################
## Unit Testing                                                               ##
################################################################################
# if __name__ == "__main__":  
#     print("field rect:", FIELD_RECT, "  grid size:", GRID_SIZE)
#     print("message rect:", MESSAGE_RECT, "  area size:", MESSAGE_SIZE)
#     print("grid size:", int(FIELD_RECT[2]/(TILE_SIZE + MARGIN)), int(FIELD_RECT[3]/(TILE_SIZE + MARGIN)))
#     print("grid size:",GRID_SIZE)
