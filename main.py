import pygame
from pygame.locals import *

def main():
    # Initialise screen
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('Project Alpha')
    icon = pygame.image.load("test_icon.jpg").convert_alpha()        
    pygame.display.set_icon(icon)

    # Fill background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 0, 0))

    # Display some text
    spriteSheet = pygame.image.load("terminal12x12_gs_ro.png")
    background.blit(spriteSheet, spriteSheet.get_rect())

    # Blit everything to the screen
    screen.blit(background, (0, 0))
    pygame.display.flip()

    # Event loop
    while 1:
        for event in pygame.event.get():
            if event.type == QUIT:
                return

        screen.blit(background, (0, 0))
        pygame.display.flip()


if __name__ == '__main__': main()