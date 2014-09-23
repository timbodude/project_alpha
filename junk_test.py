import os, sys
import pygame
from pygame.sprite import Sprite

# ------------------------------------------------------------------------------

class Unit(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.messages = ["Unit used. "]
        self.element = 1
        
    def unit_method(self, element_two):
        self.messages.append("Unit.method used. ")
        self.element_two = element_two
        
class Sub_unit(Unit):
    def __init__(self):
        Unit.__init__(self)
        self.messages.append("Sub_unit used. ")
        
sprite_one = Unit()
print("parent: ", sprite_one.messages)

dummy = 3
sprite_one.unit_method(dummy)
print("parent: ", sprite_one.messages, sprite_one.element_two)

sprite_sub = Sub_unit()
sprite_sub.unit_method(element_two = 5)
print("child: ", sprite_sub.messages, sprite_sub.element, sprite_sub.element_two)

