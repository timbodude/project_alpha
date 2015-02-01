import pygame
from params import buttons, SCREEN_HEIGHT, SCREEN_WIDTH
from unit import TileGrid, PlayerUnitGroup, MeleeEngine, PlayerCommand, Unit
from images_lib import BLACK
from PygButton import Btn_grp

class Screen:
    def render(self): 
        print("abstract method")
        
    def handle_events(self): 
        print("abstract method")   
        
class GameScreen(Screen):
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32) # create screen area for tiles
        # Fill background
        background = pygame.Surface(self.screen.get_size())
        background = background.convert()
        background.fill((0, 0, 0))
        
        self.grid_map = TileGrid(self.screen) # Create a grid of tiles
        self.players = PlayerUnitGroup(self.screen) # create group of players, each with one team of units placed on map
        self.melee_engine = MeleeEngine(self.grid_map, self.players, self.players.ttl_players)
        self.player_command = PlayerCommand() # create player/unit interface area
        

        self.buttons = Btn_grp()
        
        test_img = "images/white_tank.png"
        B_rnd = {"green": "images/btn_green.png", "gray": "images/btn_gray.png", "red": "images/btn_red.png"}
        
        self.buttons.new_btn(rect = (750,500,18,24), caption = "hi", normal = test_img)
        self.buttons.new_btn(rect =(650,500,18,24), normal = test_img)
        self.buttons.new_btn( rect = (690,500,10,10), 
                              caption = "B", 
                              normal = B_rnd["gray"], 
                              down = B_rnd["green"], 
                              highlight = B_rnd["red"] )
        self.buttons.new_btn(rect = (625,550,150,20),  caption = "MAKE IT SO!")
    
    def update_all(self):
        """ update everything & put on screen """
        self.screen.fill(BLACK) # Set the screen background
        self.grid_map.update_grid() # Update the grid to screen
        self.player_command.draw_messageboard(self.screen) # update player_command area
        self.players.update_players(self.player_command, self.grid_map, self.melee_engine) # Update player groups, units to screen, melee groups
        self.buttons.btn_grp_update(self.screen)
    
    def render(self):
        pygame.display.flip() # Go ahead and update the screen with what we've set to be drawn
    
    def usr_events(self, pos):
        """ determine action based upon mouse & keyboard input 
            pos: mouse position coordinates
        """
        if self.grid_map.in_field(pos): # Check to see if click was in grid field for testing 
            #print("you hit the battle grid area")
            #print("you're clicked on:", pos)
            self.grid_map.grid_clicked(pos) # do whatever happens when something gets clicked on in battle area
            new_coord = self.grid_map.coord_to_grid(pos)
            self.players.assign_player_grp_targ_tile(new_coord)
            self.player_command.player_msg = ""
    
    def button_events(self, event):
        # check for clicks on a button (not in mousebuttondown to allow for mouseover highlight)#         
        for button in self.buttons.btn_list:
            if "click" in button.handleEvent(event):
                if button.caption == "B":
                    self.player_command.player_msg = "That was the round button"
                if button.caption == "hi":
                    self.player_command.player_msg = "Nothing here but us buttons."
                if button.caption == "MAKE IT SO!":
                    Unit.movement(self.grid_map, self.players)
                    self.player_command.player_msg = ""
        """ check for unit-related button events """
        for player in self.players.active_list:
            for group in player.units:
                for unit in group.group_list:
                    for button in unit.unit_btns:
                        if "click" in button.handleEvent(event):
                            if button.caption == "B":
                                unit.active = "True"
                                unit.txt_status = "Targeting"
                                self.player_command.player_msg = "Click on target tile."
                            elif button.caption == "A":
                                unit.txt_status = "A Button"
                            else:
                                unit.txt_status = "Unidentified Button"
        
    def handle_events(self):
        """ returns true if program should continue execution
            returns false if program should halt
        """
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:           
                pygame.quit()
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN: # User clicks the mouse. Get the position
                GameScreen.usr_events(self,pygame.mouse.get_pos())
            """ check for user-related button events """
            GameScreen.button_events(self,event)     
        return True