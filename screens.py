#Max Line Length(79)##########################################################
import pygame
from params import SCREEN_HEIGHT, SCREEN_WIDTH, DEFAULT_GAME_FONT
from unit import TileGrid, PlayerUnitGroup, MeleeEngine, PlayerCommand, Unit
from images_lib import BLACK
from PygButton import Btn_grp

class GameFrame:
    def __init__(self):
        self.currentScreen = 0
class Screen:        
    def __init__(self):
        # create screen area for tiles
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 
                                              0, 32) 
        return
    
    def handle_events(self): 
        print("abstract method: handle_events")
        
    def render(self):
        # Go ahead and update the screen 
        # with what we've set to be drawn
        pygame.display.flip() 
        
class GameScreen(Screen):
    def __init__(self):
        Screen.__init__(self)
        
        # Fill background
        background = pygame.Surface(self.screen.get_size())
        background = background.convert()
        background.fill((0, 0, 0))
        
        # Create a grid of tiles
        self.grid_map = TileGrid(self.screen)
        # create group of players, 
        # each with one team of units placed on map
        self.players = PlayerUnitGroup(self.screen)
        self.melee_engine = MeleeEngine(self.grid_map, 
                                        self.players, 
                                        self.players.ttl_players)
        # create player/unit interface area
        self.player_command = PlayerCommand() 
        
        self.buttons = Btn_grp()
        
        test_img = "images/white_tank.png"
        B_rnd = {"green": "images/btn_green.png", 
                 "gray": "images/btn_gray.png", 
                 "red": "images/btn_red.png"}
        
        self.buttons.new_btn(rect = (750,500,18,24), 
                             caption = "hi", 
                             normal = test_img)
        self.buttons.new_btn(rect =(650,500,18,24), normal = test_img)
        self.buttons.new_btn( rect = (690,500,10,10), 
                              caption = "B", 
                              normal = B_rnd["gray"], 
                              down = B_rnd["green"], 
                              highlight = B_rnd["red"] )
        self.buttons.new_btn(rect = (625,550,150,20),  
                             caption = "MAKE IT SO!")
    
    def update_all(self):
        """ update everything & put on screen """
        # Set the screen background
        self.screen.fill(BLACK) 
        # Update the grid to screen
        self.grid_map.update_grid() 
        # update player_command area
        self.player_command.draw_messageboard(self.screen) 
        # Update player groups, units to screen, melee groups
        self.players.update_players(self.player_command, 
                                    self.grid_map, 
                                    self.melee_engine) 
        self.buttons.btn_grp_update(self.screen)
    
    def usr_events(self, pos):
        """ determine action based upon mouse & keyboard input 
            pos: mouse position coordinates
        """
        # Check to see if click was in grid field for testing 
        if self.grid_map.in_field(pos): 
            #print("you're clicked on:", pos)
            
            # do whatever happens when something 
            # gets clicked on in battle area
            self.grid_map.grid_clicked(pos) 
            new_coord = self.grid_map.coord_to_grid(pos)
            self.players.assign_player_grp_targ_tile(new_coord)
            self.player_command.player_msg = ""
    
    def button_events(self, event):
        # check for clicks on a button 
        # (not in mousebuttondown to allow for mouseover highlight)         
        for button in self.buttons.btn_list:
            if "click" in button.handleEvent(event):
                if button.caption == "B":
                    self.player_command.player_msg = \
                        "That was the round button"
                if button.caption == "hi":
                    self.player_command.player_msg = \
                        "Nothing here but us buttons."
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
                                self.player_command.player_msg = \
                                    "Click on target tile."
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
            # User clicks the mouse. Get the position
            elif event.type == pygame.MOUSEBUTTONDOWN: 
                GameScreen.usr_events(self,pygame.mouse.get_pos())
            """ check for user-related button events """
            GameScreen.button_events(self,event)     
        return True
    
class TitleScreen(Screen):
    def __init__(self):
        # create screen area
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 
                                              0, 32) 
        # Fill background
        background = pygame.Surface(self.screen.get_size())
        background = background.convert()
        background.fill((0, 0, 0))
        self.buttons = Btn_grp()
        
        
    def update_all(self):
        """ update & put on screen """
        self.screen.fill(BLACK) # Set the screen background
        #print("update done") #TEST: works
        
    def render(self):
        message1_sf = DEFAULT_GAME_FONT.render("TITLE SCREEN", 
                                               True, 
                                               pygame.Color('white'))
        self.screen.blit(message1_sf, (300, 250, SCREEN_WIDTH, SCREEN_HEIGHT))
        # Go ahead and update the screen with what we've set to be drawn
        pygame.display.flip() 
        
    def handle_events(self):
        """ returns true if the program should continue execution
            returns false if the program should halt
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    global currentScreen
                    currentScreen = GameScreen()
                    return True
        return True

currentScreen = TitleScreen()

# def turn_check():
#     """ if enough ticks pass, update all """
#     params.TICK += 1
#     player_command.tick_counter = str(params.TICK // params.GAME_SPEED)
#     if params.TICK % params.GAME_SPEED == 0:
#         Unit.movement(grid_map, players)
#         player_command.player_msg = ""    

def main():
    pygame.init()
    clock = pygame.time.Clock()
    pygame.display.set_caption('Project Alpha')
    #icon = pygame.image.load("test_icon.jpg").convert_alpha()        
    #pygame.display.set_icon(icon)  
    
    while 1:
#         turn_check()
        if not currentScreen.handle_events():
            return
        currentScreen.update_all()
         # Limit to 20 frames per second
        clock.tick(20)
        currentScreen.render()

if __name__ == '__main__': main()