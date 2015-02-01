import pygame
from screens import GameScreen

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
    
    currentScreen = GameScreen()
    while 1:
#         turn_check()
        if not currentScreen.handle_events():
            return
        currentScreen.update_all()
        clock.tick(20) # Limit to 20 frames per second
        currentScreen.render()

if __name__ == '__main__': main()