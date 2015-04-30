#Max Line Length(79)##########################################################
import pygame
import socket
from params import SCREEN_HEIGHT, SCREEN_WIDTH, DEFAULT_GAME_FONT
from unit import TileGrid, PlayerUnitGroup, MeleeEngine, PlayerCommand, Unit
from images_lib import BLACK
from PygButton import Btn_grp


WELCOME_SCREEN_BACKGROUND = "images/WelcomeScreen_color.jpg"
TITLE_SCREEN_BUTTON_TEXT = "Start the Strategery!"

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

class OptionsScreen(Screen):
    def __init__(self):
        # create screen area
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 
                                              0, 32) 
        # Fill background
        background = pygame.Surface(self.screen.get_size())
        background = background.convert()
        background.fill((0, 0, 0))
        self.buttons = Btn_grp()
        self.buttons.new_btn( rect = (250,350,120,20), 
                              caption = "Create Server" )
        self.buttons.new_btn( rect = (400,350,160,20), 
                              caption = "Connect to Server" )
        
    def update_all(self):
        """ update & put on screen """
        self.screen.fill(BLACK) # Set the screen background
        self.buttons.btn_grp_update(self.screen)
        
    def render(self): 
        message1_sf = DEFAULT_GAME_FONT.render("OPTIONS SCREEN", 
                                               True, 
                                               pygame.Color('white'))
        self.screen.blit(message1_sf, (300, 250, SCREEN_WIDTH, SCREEN_HEIGHT))
        IPaddr = ask(self.screen, "IP Address")
        
        ################################################ Server Code####################################
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serversocket.bind(('localhost', 8089))
        serversocket.listen(5) # become a server socket, maximum 5 connections
          
        while True:
            connection, address = serversocket.accept()
            buf = connection.recv(64)
            if len(buf) > 0:
                print buf
                break
        ###############################################################################################
        
#         ################################### Client Code#################################################
#         clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         clientsocket.connect((IPaddr, 8089))
#         clientsocket.send('If this is printed, the socket works!')
        ################################################################################################
        
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
    
class TitleScreen(Screen):
    def __init__(self):
        # create screen area
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 
                                              0, 32) 
        # Fill background
        background = pygame.Surface(self.screen.get_size())
        background = background.convert()
        background.fill((0, 0, 0))
        self.background_image = pygame.image.load(WELCOME_SCREEN_BACKGROUND).convert_alpha()
        
        self.buttons = Btn_grp()
        self.buttons.new_btn(rect = (560,480,175,20),  caption = TITLE_SCREEN_BUTTON_TEXT)
        
    def update_all(self):
        """ update & put on screen """
        self.buttons.btn_grp_update(self.screen)
        #print("update done") #TEST: works
        
    def render(self):
        # Go ahead and update the screen with what we've set to be drawn
        self.screen.blit(self.background_image, [0,0]) # Set the screen backgroundd
        pygame.display.flip() 
        
    def handle_events(self):
        """ returns true if the program should continue execution
            returns false if the program should halt
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("quitting...")
                pygame.quit()
                return False 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    global currentScreen
                    currentScreen = OptionsScreen()
                    return True
        return True
    
    def button_events(self, event):
        for button in self.buttons.btn_list:
            if "click" in button.handleEvent(event):
                if button.caption == TITLE_SCREEN_BUTTON_TEXT:
                    #do something 
                    print("I made it so")
                    
def get_key():
    while 1:
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            pygame.quit()
            return False 
        elif event.type == pygame.KEYDOWN:
            return event.key
        else:
            pass

def display_box(screen, message):
    "Print a message in a box in the middle of the screen"
    fontobject = pygame.font.Font(None,18)
    pygame.draw.rect(screen, (0,0,0),
                       ((screen.get_width() / 2) - 100,
                        (screen.get_height() / 2) - 10,
                        200,20), 0)
    pygame.draw.rect(screen, (255,255,255),
                       ((screen.get_width() / 2) - 102,
                        (screen.get_height() / 2) - 12,
                        204,24), 1)
    if len(message) != 0:
        screen.blit(fontobject.render(message, 1, (255,255,255)),
                    ((screen.get_width() / 2) - 100, (screen.get_height() / 2) - 10))
    pygame.display.flip()

def ask(screen, question):
    "ask(screen, question) -> answer"
    pygame.font.init()
    current_string = []
    display_box(screen, question + ": " + pygame.string.join(current_string,""))
    while 1:
        inkey = get_key()
        if inkey == pygame.K_BACKSPACE:
            current_string = current_string[0:-1]
        elif inkey == pygame.K_RETURN:
            global currentScreen
            currentScreen = GameScreen()
            break
        elif inkey == pygame.K_MINUS:
            current_string.append("_")
        elif inkey <= 127:
            current_string.append(chr(inkey))
        display_box(screen, question + ": " + pygame.string.join(current_string,""))
    return pygame.string.join(current_string,"")

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
#        turn_check()
        if not currentScreen.handle_events():
            return
        currentScreen.update_all()
        # Limit to 20 frames per second
        clock.tick(20)
        currentScreen.render()

if __name__ == '__main__': main()

