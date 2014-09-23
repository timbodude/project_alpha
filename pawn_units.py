# pawn_units

#import pygame
from pygame.sprite import Sprite
from pygame import Rect
import pygame
from random import randint, choice

#pawn_group = pygame.sprite.Group()



class Pawn(Sprite):
    def __init__(self):
        Sprite.__init__(self) # call parent class sprite constructor
        self.message = "I made a pawn" # test to verify pawn was created
        self.pawn_aids = [1, 1, 1, 1]
        self.width = 20
        self.height = 20
        PAWN_GREEN = (0, 200, 0)        
        color = PAWN_GREEN
        
        
        self.image = pygame.Surface([self.width, self.height]) # replace with sprite image
        #self.die_image = die image # connect with sprite image
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.pos = [10,10]                                
        self.speed = 0.05
        self.health = 5
        

    def draw(self, offset):
        pygame.draw.rect = (self.image.get_rect().move(self.pos[0] - self.width / 2, self.pos[1] - self.height / 2 + offset))
        pygame.screen.blit(self.image, self.draw_rect)    
        
        #pygame.draw.rect(DISPLAYSURF, self.fill, [self.pos[0], self.pos[1], START_SIZ, START_SIZ])  
        
        
class Pawn_group(Sprite):
    """ group of player pawns """
    def __init__(self):
        self.group_list = []
        self.gr_aids_names = ["Attack", "Initiative", "Defense", "Speed"]
        
    def make_group(self, qty):
        for dummy in range(qty):
            new_pawn = Pawn()
            self.group_list.append(new_pawn)
            print("I added a new pawn")
            
    def draw_group(self):
        offset = 0
        for pawn in self.group_list:
            offset += 40
            pawn.draw(40)
            
            
#class Block(pygame.sprite.Sprite):

    ## Constructor. Pass in the color of the block,
    ## and its x and y position
    #def __init__(self, color, width, height):
       ## Call the parent class (Sprite) constructor
       #pygame.sprite.Sprite.__init__(self)

       ## Create an image of the block, and fill it with a color.
       ## This could also be an image loaded from the disk.
       #self.image = pygame.Surface([width, height])
       #self.image.fill(color)

       ## Fetch the rectangle object that has the dimensions of the image
       ## Update the position of this object by setting the values of rect.x and rect.y
       #self.rect = self.image.get_rect()