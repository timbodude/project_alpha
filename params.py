################################################################################
## params
################################################################################
""" sets params and globals """

################################################################################
from pygame import Rect

################################################################################

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
FIELD_RECT = Rect(100, 50, 500, 450)
MARGIN = 1
TILE_SIZE = 32
GRID_SIZE = (int(FIELD_RECT[2]/(TILE_SIZE + MARGIN)), int(FIELD_RECT[3]/(TILE_SIZE + MARGIN)))
MESSAGE_RECT = Rect(625, 50, 150, 200)
end_check = False
paused = False
won = False # flag for battel is over
TURN_COUNT = 0

################################################################################
## Unit Testing                                                               ##
################################################################################
if __name__ == "__main__":  
    print("field rect:", FIELD_RECT, "  grid size:", GRID_SIZE)
    
    print(int(FIELD_RECT[2]/(TILE_SIZE + MARGIN)), int(FIELD_RECT[3]/(TILE_SIZE + MARGIN)))
    print(GRID_SIZE)