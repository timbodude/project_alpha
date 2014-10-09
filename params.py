################################################################################
## params
################################################################################
""" sets params and globals """

################################################################################
from pygame import Rect

################################################################################

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
FIELD_RECT = Rect(0, 0, 600, 600)
MARGIN = 0
TILE_SIZE = 12
GRID_SIZE = (int(FIELD_RECT[2]/(TILE_SIZE + MARGIN)), int(FIELD_RECT[3]/(TILE_SIZE + MARGIN)))
MESSAGE_RECT = Rect(600, 0, 800, 600)
MESSAGE_SIZE = (int(MESSAGE_RECT[2])-MESSAGE_RECT[0], int(MESSAGE_RECT[3]))
end_check = False
paused = False
won = False # flag for battel is over
TURN_COUNT = 0

################################################################################
## Unit Testing                                                               ##
################################################################################
if __name__ == "__main__":  
    print("field rect:", FIELD_RECT, "  grid size:", GRID_SIZE)
    print("message rect:", MESSAGE_RECT, "  area size:", MESSAGE_SIZE)
    print("grid size:", int(FIELD_RECT[2]/(TILE_SIZE + MARGIN)), int(FIELD_RECT[3]/(TILE_SIZE + MARGIN)))
    print("grid size:",GRID_SIZE)