import pygame, os
from pygame.locals import *
from grid import Tile_grid
import params, player_command, move
from images_lib import (  BLACK, WHITE,  DARKGRAY, GRAY, LIGHTGRAY )
from unit_simp import P_u_group
import pygbutton

################################################################################

# Get things started
screen = pygame.display.set_mode((params.SCREEN_WIDTH, params.SCREEN_HEIGHT), 0, 32) # create screen area for tiles
grid_map = Tile_grid(screen) # Create a grid of tiles
player_command = player_command.Player_command() # create player/unit interface area
players = P_u_group(screen) # create group of players
buttons = pygbutton.Btn_grp()

#dropping in a test image
test_img = "images/white_tank.png"

# try a pygbutton - default listed below:
#button_1 = pygbutton.PygButton(rect=(650,550,75,20), caption="btn_1", bgcolor=LIGHTGRAY, fgcolor=BLACK)
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
        
def button_events(event):
    """ check for user-related button events """
    #if "click" in button_1.handleEvent(event):
        #print("Hey, I was clicked.")
    #if "click" in button_2.handleEvent(event):
        #print("Nothing here but us buttons.")
    for button in buttons.btn_list:
        if "click" in button.handleEvent(event):
            dummy = False
            #print("Woa Nellie, I'm a button after all.", button.rect) # do clicking sound or whatever is common to all buttons
            if button.caption == "B":
                print("That was the round button")
            if button.caption == "hi":
                print("Nothing here but us buttons.")
            if button.caption == "MAKE IT SO!":
                print("Movement phase done, calculate moves & combat resolution - no combat yet, but getting close...")
                move.movement(grid_map, players)
                
    """ check for unit-related button events """
    for player in players.active_list:
        for group in player.units:
            for unit in group.group_list:
                for button in unit.unit_btns:
                    if "click" in button.handleEvent(event):
                        if button.caption == "B":
                            print("This unit's Move button has been pressed.", button.rect)                     
                        elif button.caption == "A":
                            print("This unit's Active button has been pressed.", button.rect)
                        else:
                            print("an unidentified button for this player has been pressed.")
        
def update_all():
    """ update everything & put on screen """
    screen.fill(BLACK) # Set the screen background
    grid_map.update_grid() # Update the grid to screen
    player_command.draw_messageboard(screen) # update player_command area
    players.update_players(player_command) # Update player groups & units to screen    
    #button_1._update()
    #button_1.draw(screen)
    #button_2._update()
    #button_2.draw(screen)
    buttons.btn_grp_update(screen)
        
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
        for event in pygame.event.get():
            if event.type == QUIT:
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