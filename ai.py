################################################################################
## ai
################################################################################
""" simple ai helper file for unit_simp """
import random
from random import randint
import params

################################################################################

def rnd_targ_tile():
    """ select a random target tile for movement for a single unit """
    x = random.randint(1, int(params.FIELD_RECT[2]/(params.TILE_SIZE + params.MARGIN))-1)
    y = random.randint(1, int(params.FIELD_RECT[3]/(params.TILE_SIZE + params.MARGIN))-1)
    return(x,y)
