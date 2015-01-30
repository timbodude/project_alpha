import pygame
import tile_grid
import params, player_command, move, melee
from images_lib import (  BLACK, WHITE,  DARKGRAY, GRAY, LIGHTGRAY )
from unit_simp import P_u_group
import PygButton

################################################################################

# Get things started
screen = pygame.display.set_mode((params.SCREEN_WIDTH, params.SCREEN_HEIGHT), 0, 32) # create screen area for tiles
grid_map = tile_grid.TileGrid(screen) # Create a grid of tiles
player_command = player_command.Player_command() # create player/unit interface area
players = P_u_group(screen) # create group of players, each with one team of units placed on map
buttons = PygButton.Btn_grp()
melee_engine = melee.Melee_engine(grid = grid_map, player_grp = players, ttl_players = players.ttl_players)
#dropping in a test image
test_img = "images/white_tank.png"
# try a PygButton - default listed below:
#button_1 = PygButton.PygButton(rect=(650,550,75,20), caption="btn_1", bgcolor=LIGHTGRAY, fgcolor=BLACK)
button_2 = buttons.new_btn(rect=(750,500,18,24), caption = "hi", normal = test_img)
button_4 = buttons.new_btn(rect = (650,500,18,24), normal = test_img)

B_rnd = {"green": "images/btn_green.png", "gray": "images/btn_gray.png", "red": "images/btn_red.png"}
button_colored = buttons.new_btn(  rect = (690,500,10,10), 
                                   caption = "B", 
                                   normal = B_rnd["gray"], 
                                   down = B_rnd["green"], 
                                   highlight = B_rnd["red"] )
button_move = buttons.new_btn(  rect = (625,550,150,20), 
                                caption = "MAKE IT SO!")

################################################################################

def usr_events(pos):
    """ determine action based upon mouse & kbd input 
        pos: mouse position coordinates
    """
    if grid_map.in_field(pos): # Check to see if click was in grid field for testing 
        #print("you hit the battle grid area")
        #print("you're clicked on:", pos)
        grid_map.grid_clicked(pos) # do whatever happens when something gets clicked on in battle area
        new_coord = grid_map.coord_to_grid(pos)
        players.assign_player_grp_targ_tile(new_coord)
        player_command.player_msg = ""
        
def button_events(event):
    """ check for user-related button events """
    for button in buttons.btn_list:
        if "click" in button.handleEvent(event):
            dummy = False
            #print("Woa Nellie, I'm a button after all.", button.rect) # do clicking sound or whatever is common to all buttons
            if button.caption == "B":
                player_command.player_msg = "That was the round button"
            if button.caption == "hi":
                player_command.player_msg = "Nothing here but us buttons."
            if button.caption == "MAKE IT SO!":
                move.movement(grid_map, players)
                player_command.player_msg = ""
                
    """ check for unit-related button events """
    for player in players.active_list:
        for group in player.units:
            for unit in group.group_list:
                for button in unit.unit_btns:
                    if "click" in button.handleEvent(event):
                        if button.caption == "B":
                            unit.active = "True"
                            unit.txt_status = "Targeting"
                            #print("This unit's Move button has been pressed.", button.rect)
                            player_command.player_msg = "Click on target tile."
                        elif button.caption == "A":
                            #print("This unit's Active button has been pressed.", button.rect)
                            unit.txt_status = "A Button"
                        else:
                            #print("an unidentified button for this player has been pressed.")
                            unit.txt_status = "Unidentified Button"
        
def update_all():
    """ update everything & put on screen """
    screen.fill(BLACK) # Set the screen background
    grid_map.update_grid() # Update the grid to screen
    player_command.draw_messageboard(screen) # update player_command area
    players.update_players(player_command, grid_map, melee_engine) # Update player groups, units to screen, melee groups
    #button_1._update()
    #button_1.draw(screen)
    #button_2._update()
    #button_2.draw(screen)
    buttons.btn_grp_update(screen)
    
def turn_check():
    """ if enough ticks pass, update all """
    params.TICK += 1
    player_command.tick_counter = str(params.TICK // params.GAME_SPEED)
    if params.TICK % params.GAME_SPEED == 0:
        move.movement(grid_map, players)
        player_command.player_msg = ""        
        
        
################################################################################

def main():
    # Initialise screen
    pygame.init()
    clock = pygame.time.Clock()
    pygame.display.set_caption('Project Alpha')
    #icon = pygame.image.load("test_icon.jpg").convert_alpha()        
    #pygame.display.set_icon(icon)  
    # Fill background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 0, 0))
    
    ttl_round = 0 # total rounds played
    turn = 0 # who's turn it is    
    
    # Event loop
    while 1:
        turn_check()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                #grid_map.print_test_grid()  # print test grid to shell              
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN: # User clicks the mouse. Get the position
                usr_events(pygame.mouse.get_pos())
            button_events(event) # check for clicks on a button (not in mousebuttondown to allow for mouseover highlight)
                    
        update_all()

        clock.tick(20) # Limit to 20 frames per second
        pygame.display.flip() # Go ahead and update the screen with what we've set to be drawn

if __name__ == '__main__': main()