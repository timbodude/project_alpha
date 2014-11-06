import pygame

################################################################################
## helper_apps
################################################################################
""" contains useful little widgets or apps used throughout program """

def calc_move(now_coord, targ_coord):
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
        
