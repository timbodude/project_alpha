import os, sys
from random import randint, choice
from math import sin, cos, radians

import pygame
from pygame import Rect, Color
from pygame.sprite import Sprite

from vec2d import vec2d
from simpleanimation import SimpleAnimation

# ------------------------------------------------------------------------------                
# GLOBALS

FIELD_RECT = Rect(50, 50, 300, 300)
creep_images = [
    ('images/bluecreep_0.png', 'images/bluecreep_45.png'),
    ('images/greencreep_0.png', 'images/greencreep_45.png'),
    ('images/yellowcreep_0.png', 'images/yellowcreep_45.png'),
    ('images/pinkcreep_0.png', 'images/pinkcreep_45.png') ] 
CREEP_FILENAMES = [
    ('images/bluecreep_0.png', 'images/bluecreep_45.png'),
    ('images/greencreep_0.png', 'images/greencreep_45.png'),
    ('images/yellowcreep_0.png', 'images/yellowcreep_45.png'),
    ('images/pinkcreep_0.png', 'images/pinkcreep_45.png') ] 

# ------------------------------------------------------------------------------                

class Unit(Sprite):
    """ Overall unit class """
    def __init__(self, screen, explosion_images):
        
        """ Create a new Unit.
        
            screen: 
                The screen on which the unit lives (must be a 
                pygame Surface object, such as pygame.display)
            
            creep_image: 
                Image (surface) object for the unit
            
            explosion_images:
                A list of image objects for the explosion 
                animation.
            
            field:
                A Rect specifying the 'playing field' boundaries.
                The unit will bounce off the 'walls' of this 
                field.
                
            init_position:
                A vec2d or a pair specifying the initial position
                of the unit on the screen.
            
            init_direction:
                A vec2d or a pair specifying the initial direction
                of the unit. Must have an angle that is a 
                multiple of 45 degres.
            
            speed: 
                unit speed, in pixels/millisecond (px/ms)"""
        Sprite.__init__(self)
        self.screen = screen
        self.speed = .03
        self.field=FIELD_RECT
        # base_image holds the original image, positioned to
        # angle 0.
        # image will be rotated.
        self.unit_type = 0
        
        self.image = [("images/bluecreep_0.png", "images/bluecreep_45.png")]
        self.image = creep_images[1]
        self.health = 10            
        self.base_image_0 = self.image[0]
        self.base_image_45 = self.image[1] 
 
        self.explosion_images = explosion_images
        self.init_position = ( randint(FIELD_RECT.left, FIELD_RECT.right), randint(FIELD_RECT.top, FIELD_RECT.bottom))
        self.init_direction = (choice([-1, 1]), choice([-1, 1]))        
        
        # A vector specifying the creep's position on the screen
        self.pos = vec2d(self.init_position)

        # The direction is a normalized vector
        self.direction = vec2d(self.init_direction).normalized()
        self.state = Unit.ALIVE
        
    def is_alive(self):
        return self.state in (Unit.ALIVE, Unit.EXPLODING)   
    
    def update(self, time_passed):
        """ Update the Unit.
            time_passed: The time passed (in ms) since the previous update. """
        if self.state == Unit.ALIVE:
            # Maybe it's time to change the direction ?
            self._change_direction(time_passed)
            
            # Make the Unit point in the correct direction.
            # Since our direction vector is in screen coordinates 
            # (i.e. right bottom is 1, 1), and rotate() rotates 
            # counter-clockwise, the angle must be inverted to 
            # work correctly.
            #
            #self.image = pygame.transform.rotate(self.base_image, -self.direction.angle) # --------------------------------->>>> LEFT OFF HERE
            if int(round(self.direction.angle)) % 90 == 45:
                self.image = pygame.transform.rotate(self.base_image_45, -(self.direction.angle + 45))
            elif int(round(self.direction.angle)) % 90 == 0:
                self.image = pygame.transform.rotate(self.base_image_0, -self.direction.angle)
            else:
                assert False            
            
            # Compute and apply the displacement to the position 
            # vector. The displacement is a vector, having the angle
            # of self.direction (which is normalized to not affect
            # the magnitude of the displacement)
            #
            displacement = vec2d(    
                self.direction.x * self.speed * time_passed,
                self.direction.y * self.speed * time_passed)
            
            self.pos += displacement
            
            # When the image is rotated, its size is changed.
            # We must take the size into account for detecting 
            # collisions with the walls.
            #
            self.image_w, self.image_h = self.image.get_size()
            bounds_rect = self.field.inflate(
                            -self.image_w, -self.image_h)
            
            if self.pos.x < bounds_rect.left:
                self.pos.x = bounds_rect.left
                self.direction.x *= -1
            elif self.pos.x > bounds_rect.right:
                self.pos.x = bounds_rect.right
                self.direction.x *= -1
            elif self.pos.y < bounds_rect.top:
                self.pos.y = bounds_rect.top
                self.direction.y *= -1
            elif self.pos.y > bounds_rect.bottom:
                self.pos.y = bounds_rect.bottom
                self.direction.y *= -1
                
        elif self.state == Unit.EXPLODING:
            if self.explode_animation.active:
                self.explode_animation.update(time_passed)
            else:
                self.state = Unit.DEAD
                self.kill()
        
        elif self.state == Unit.DEAD:
            pass    

    def draw(self):
        """ Blit the unit onto the screen that was provided in
            the constructor.
        """
        if self.state == Unit.ALIVE:
            # The Unit image is placed at self.pos. To allow for 
            # smooth movement even when the Unit rotates and the 
            # image size changes, its placement is always 
            # centered.
            #
            self.draw_rect = self.image.get_rect().move(
                self.pos.x - self.image_w / 2, 
                self.pos.y - self.image_h / 2)
            self.screen.blit(self.image, self.draw_rect)
            
            # The health bar is 15x4 px.
            #
            health_bar_x = self.pos.x - 7
            health_bar_y = self.pos.y - self.image_h / 2 - 6
            self.screen.fill(   Color('red'), 
                                (health_bar_x, health_bar_y, 15, 4))
            self.screen.fill(   Color('green'), 
                                (   health_bar_x, health_bar_y, 
                                    self.health, 4))
        
        elif self.state == Unit.EXPLODING:
            self.explode_animation.draw()
        
        elif self.state == Unit.DEAD:
            pass  
        
    def mouse_click_event(self, pos):
        """ The mouse was clicked in pos.
        """
        if self._point_is_inside(vec2d(pos)):
            self._decrease_health(3)
                
    #------------------ PRIVATE PARTS ------------------#
    # States the Unit can be in.
    #
    # ALIVE: The Unit is roaming around the screen
    # EXPLODING: 
    #   The Unit is now exploding, just a moment before dying.
    # DEAD: The Unit is dead and inactive
    #
    (ALIVE, EXPLODING, DEAD) = range(3)
    _counter = 0  
    
    def _change_direction(self, time_passed):
        """ Turn by 45 degrees in a random direction once per
            0.4 to 0.5 seconds.
        """
        self._counter += time_passed
        if self._counter > randint(400, 500):
            self.direction.rotate(45 * randint(-1, 1))
            self._counter = 0
    
    def _point_is_inside(self, point):
        """ Is the point (given as a vec2d) inside our Unit's body? """
        img_point = point - vec2d(  
            int(self.pos.x - self.image_w / 2),
            int(self.pos.y - self.image_h / 2))        
        try:
            pix = self.image.get_at(img_point)
            return pix[3] > 0
        except IndexError:
            return False
    
    def _decrease_health(self, n):
        """ Decrease my health by n (or to 0, if it's currently
            less than n)
        """
        self.health = max(0, self.health - n)
        if self.health == 0:
            self._explode()

    def _explode(self):
        """ Starts the explosion animation that ends the Unit's life. """
        self.state = Unit.EXPLODING
        pos = ( self.pos.x - self.explosion_images[0].get_width() / 2,
                self.pos.y - self.explosion_images[0].get_height() / 2)
        self.explode_animation = SimpleAnimation(
            self.screen, pos, self.explosion_images,
            100, 300)    
    
# ------------------------------------------------------------------------------

class Creep(Unit):
    """ child class of unit for opponents """
    def __init__(self, screen, explosion_images):
        Unit.__init__(self, screen, explosion_images)
        self.screen = screen
        self.explosion_images = explosion_images
        self.field=FIELD_RECT
        self.init_position = (randint(FIELD_RECT.left, FIELD_RECT.right), randint(FIELD_RECT.top, FIELD_RECT.bottom))
        self.init_direction = (choice([-1, 1]), choice([-1, 1]))    
        self.unit_type = randint(0,2)
        
        if self.unit_type == 0:
            self.image = creep_images[0]
            self.health = 5
        elif self.unit_type == 1:
            self.image = creep_images[1]
            self.health = 10
        elif self.unit_type == 2:
            self.image = creep_images[2]
            self.health = 15            
        else:
            self.image = creep_images[3]
            self.health = 20 
            
        self.base_image_0 = self.image[0]
        self.base_image_45 = self.image[1] 
        
        print(self.screen, self.explosion_images, self.field, self.init_position, self.init_direction, self.health, self.speed, self.unit_type)
            
            
            #STILL NEED TO: add attribute self.unit_type from instance call, remove elements to unit_type-if tree that can be assigned to unit_type
  
        
class Pawn(Unit):
    """ child class of unit for player """
    def __init(self, screen, explosion_images):
        Unit.__init__(self)
        self.screen = screen
        self.explosion_images = explosion_images
        self.field=FIELD_RECT
        self.init_position = (randint(FIELD_RECT.left, FIELD_RECT.right), randint(FIELD_RECT.top, FIELD_RECT.bottom))
        self.init_direction = (choice([-1, 1]), choice([-1, 1])) 
        self.unit_type = 0
        if self.unit_type == 0:
            self.health = 15 
            self.speed = .05
            self.image = "images/bluepawn.png"
            
        print(self.screen, self.explosion_images, self.field, self.init_position, self.init_direction, self.health, self.speed, self.unit_type)
  
# ------------------------------------------------------------------------------

      
def post_clock(time_count):
    d_min = int(time_count/50/60)
    d_sec = int(time_count/50 %60)
    if d_sec > 59:
        d_sec = 0
    dt_min = str(d_min)
    dt_sec = str(d_sec)
    if len(dt_sec) < 2:
        dt_sec = "0" + dt_sec
    return("clock: " + dt_min + ":" + dt_sec)

def draw_messageboard(screen, rect, message1, message2, message3):
    draw_rimmed_box(screen, rect, (50, 20, 0), 4, Color('black'))
    
    my_font = pygame.font.SysFont('arial', 20)
    message1_sf = my_font.render(message1, True, Color('white'))
    message2_sf = my_font.render(message2, True, Color('white'))
    message3_sf = my_font.render(message3, True, Color('white'))
    
    screen.blit(message3_sf, rect)
    screen.blit(message1_sf, rect.move(0, message1_sf.get_height()))
    screen.blit(message2_sf, rect.move(0, message2_sf.get_height()*2))

def draw_rimmed_box(screen, box_rect, box_color, 
                    rim_width=0, 
                    rim_color=Color('black')):
    """ Draw a rimmed box on the given surface. 
        The rim is drawn outside the box rect.
    """
    if rim_width:
        rim_rect = Rect(box_rect.left - rim_width,
                        box_rect.top - rim_width,
                        box_rect.width + rim_width * 2,
                        box_rect.height + rim_width * 2)
        pygame.draw.rect(screen, rim_color, rim_rect)
    
    pygame.draw.rect(screen, box_color, box_rect)
    

def draw_background(screen, tile_img, field_rect):
    img_rect = tile_img.get_rect()
    
    nrows = int(screen.get_height() / img_rect.height) + 1
    ncols = int(screen.get_width() / img_rect.width) + 1
    
    for y in range(nrows):
        for x in range(ncols):
            img_rect.topleft = (x * img_rect.width, 
                                y * img_rect.height)
            screen.blit(tile_img, img_rect)
    
    field_color = (109, 41, 1)
    draw_rimmed_box(screen, field_rect, field_color, 4, Color('black'))

# ------------------------------------------------------------------------------        

def run_game():
    
    # Game parameters
    SCREEN_WIDTH, SCREEN_HEIGHT = 500, 400
    #FIELD_RECT = Rect(50, 50, 300, 300)
    MESSAGE_RECT = Rect(360, 50, 130, 200)
    BG_TILE_IMG = 'images/brick_tile.png'
    time_count = 0
    
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
    clock = pygame.time.Clock()
    paused = False    
    
           
    
    creep_images = [
            (   pygame.image.load(f1).convert_alpha(),
                pygame.image.load(f2).convert_alpha())
            for (f1, f2) in CREEP_FILENAMES]   
    
    N_CREEPS = 10
    
    PAWN_FILENAMES = ["images/bluepawn.png"]
    N_PAWNS = 3



    #creep_images = [pygame.image.load(filename).convert_alpha() for filename in CREEP_FILENAMES]
    #pawn_images = [pygame.image.load(filename).convert_alpha() for filename in PAWN_FILENAMES]
    
    explosion_img = pygame.image.load('images/explosion1.png').convert_alpha()
    explosion_images = [explosion_img, pygame.transform.rotate(explosion_img, 90)]

    bg_tile_img = pygame.image.load(BG_TILE_IMG).convert_alpha()

    # Create N_CREEPS random creeps.
    creeps = pygame.sprite.Group()
    for i in range(N_CREEPS):
        creeps.add(Creep(screen, explosion_images)) 
        
    #Create N_PAWNS random Pawns.
    #pawns = pygame.sprite.Group()
    #for i in range(N_PAWNS):
        #pawns.add(Pawn(screen=screen, explosion_images=explosion_images, field=FIELD_RECT, init_position=( randint(FIELD_RECT.left, FIELD_RECT.right), randint(FIELD_RECT.top, FIELD_RECT.bottom)), init_direction=(choice([-1, 1]), choice([-1, 1])))        
        
    # The main game loop
    #
    while True:
        # Limit frame speed to 50 FPS
        #
        time_passed = clock.tick(50)
        
        if paused == False and len(creeps) != 0:
            time_count += 1
        #~ time_passed = clock.tick()
        #~ print time_passed
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused
            elif (  event.type == pygame.MOUSEBUTTONDOWN and
                    pygame.mouse.get_pressed()[0] and
                    paused != True):
                for creep in creeps:
                    creep.mouse_click_event(pygame.mouse.get_pos())
                #for pawn in pawns:
                    #pawn.mouse_click_event(pygame.mouse.get_pos())                    
                    
        
        if not paused:
            # Redraw the background
            draw_background(screen, bg_tile_img, FIELD_RECT)
            
            msg1 = 'Creeps: %d' % len(creeps)
            msg2 = 'You won!' if len(creeps) == 0 else ''
            msg3 = post_clock(time_count)
            draw_messageboard(screen, MESSAGE_RECT, msg1, msg2, msg3)
            
            # Update and redraw all creeps
            for creep in creeps:
                creep.update(time_passed)
                creep.draw()
                
            #for pawn in pawns:
                #pawn.update(time_passed)
                #pawn.draw()

        pygame.display.flip()


def exit_game():
    pygame.quit()
    sys.exit()


run_game()
