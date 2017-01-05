import pygame
from pygame.locals import *
pygame.init()

import random
import os
import math


class Mouse(pygame.sprite.Sprite):
    def __init__(self):
        '''
        M.__init__()
        Initializes Mouse
        '''
        pygame.sprite.Sprite.__init__(self)
        self.x=0
        self.y=0
        self.image=pygame.Surface((1,1)).convert()
        self.image.fill((0,0,0))
        self.image.set_alpha(0)        
        self.rect=self.image.get_rect()

        
    def update(self):
        '''
        M.update() --> None
        This method is used to move this sprite around on screen.
        '''
        self.rect.left=self.x
        self.rect.top=self.y
        
        
        
class Button(pygame.sprite.Sprite):
    def __init__(self, text, x, y, font, img_dirr):  
        '''
        B.__init__(String, int, int, Font, String)
        Initializes Button
        
        Creates a basic button the player can click on.
        Takes 5 arguments. First argument is a string for the text that will be 
        diisplayed on the button.The second argument is the x corrdinate for 
        where the button will be displayed on screen. The third argument is the 
        y corrdinate for where the button will be displayed on screen. The forth
        argument if a pygame.Font for what font will be used for the button's 
        text. The final argument is a reference to the directory with the 
        image that will be used for the button.
        '''
        pygame.sprite.Sprite.__init__(self)   
        
        os.chdir(img_dirr)
        self.image=pygame.image.load("button.bmp").convert()
        
        self.text=font.render(text, True, (255,255,255))
        
        self.image.set_colorkey((255,0,255))
        self.rect=self.image.get_rect()
        self.rect.left=x
        self.rect.top=y
        self.image.blit(self.text, (int(self.image.get_size()[0]/2-self.text.get_size()[0]/2), int(self.image.get_size()[1]/2-self.text.get_size()[1]/2)))  
        


class Paddle(pygame.sprite.Sprite):
    paddles=[]
    def __init__(self, player, img_dirr):
        '''
        P.__init__(int, String)
        Initializes Paddle
        
        A player. Takes two arguments, the first is an int refering to if this 
        player is player 1 or player 2. The secoond argument is a String the 
        references the directory with the image that will be used for the 
        launching arrow at the start of the match.
        '''
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.Surface((80,15)).convert()
        if player==1:
            self.image.fill((0,0,255))        
        if player==2:
            self.image.fill((255,0,0))        
        self.rect=self.image.get_rect()
        if player==1:
            self.rect.top=465
        if player==2:
            self.rect.top=0
        self.rect.centerx=320
        self.player_num=player
        self.blocks_broken=[]
        
        
        self.ball_speed=3
        
        
        if player==1:
            self.launching_angle=24
        if player==2:
            self.launching_angle=58
            
                    
        os.chdir(img_dirr)        
        self.arrow_image=pygame.image.load("arrow.bmp").convert()
        self.arrow_image.set_colorkey((255,0,255))
        
        Paddle.paddles+=[self]
        
        
class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, block_type, img_dirr, hits_to_distroy=None):
        '''
        T.__init__(int, int, String, String, int)
        Initializes Tile
        
        A tile that the player can break. Takes 5 arguments. First argument is 
        the x corrdinate for where the tile will be displayed on screen. The 
        second argument is the y corrdinate for where the tile will be displayed
        on screen. The Third argument if a string refering to what kind of tile
        it is. The 4th argument is a string for the directory where the tile 
        images can be found The 5th argument is an int refering to how many 
        times this tile must be hit for it to break.
        '''
        pygame.sprite.Sprite.__init__(self)
        
        self.original_block_type=block_type   
        self.block_type=block_type
        
        
        
        os.chdir(img_dirr)
        if block_type=="None": 
            self.image=pygame.image.load("normal_block.bmp").convert()
        if block_type=="Speed_up": 
            self.image=pygame.image.load("speed_up_block.bmp").convert()
        if block_type=="Speed_down": 
            self.image=pygame.image.load("speed_down_block.bmp").convert()
        if block_type=="Paddle_grow": 
            self.image=pygame.image.load("paddle_grow_block.bmp").convert()
        if block_type=="Paddle_shrink": 
            self.image=pygame.image.load("paddle_shrink_block.bmp").convert()
        if block_type=="Multi_ball": 
            self.image=pygame.image.load("multi_ball_block.bmp").convert()
        if block_type=="Fire_5_balls": 
            self.image=pygame.image.load("fire_5_balls_block.bmp").convert()
        if block_type=="Metal": 
            self.image=pygame.image.load("metal_block.bmp").convert()
            self.original_hits_to_distroy=hits_to_distroy
            self.hits_to_distroy=hits_to_distroy
            
        self.image.set_alpha(255)
        self.original_image=self.image
        
        
        self.rect=self.image.get_rect()
        self.rect.left=x
        self.rect.top=y
        
        self.time_distroyed=None
        self.respawning=False
        self.respawn_timer=30
        
        
class Ball(pygame.sprite.Sprite):
    def __init__(self, first, player_num, img_dirr):
        '''
        B.__init__(bool, int, String)
        Initializes Ball
        
        A ball. Takes 3 arguments. The first is a boolean for if this is the 
        first ball the player has at the start of the game. The second is an int
        refering to which player owns this ball. The third argument is a string
        for the path to the directory with the ball's images in it.
        '''
        pygame.sprite.Sprite.__init__(self)
        
        self.player_num=player_num
        
        os.chdir(img_dirr)
        if player_num==1:
            self.image=pygame.image.load("blue_ball.bmp")
        if player_num==2:
            self.image=pygame.image.load("red_ball.bmp")
        self.rect=self.image.get_rect()
        self.image.set_colorkey(self.image.get_at((0,0)))
        
        
        if player_num==1:
            self.rect.top=455
        if player_num==2:
            self.rect.top=15
            
        self.rect.centerx=320
            
            
        self.left_prev=self.rect.left
        self.top_prev=self.rect.top
        self.left_unrounded=self.rect.left
        self.top_unrounded=self.rect.top
        
        self.flipped=False
        self.launched=True
        self.out=False
        
        self.passed_paddle=False
        
        if first==True:
            self.launched=False
            
            
    def update(self):
        '''
        B.update() --> None
        Moved the ball around on the screen. Handles Physics if it hits a wall.
        '''
        if self.launched==True:
            self.top_prev=self.top_unrounded
            self.left_prev=self.left_unrounded
                      
            
            if self.top_unrounded<=0 and self.player_num==1:
                self.top=0
                self.top_unrounded=0
                self.pi_direction-=(self.pi_direction)*2
                
            if self.top_unrounded<=-10 and self.player_num==2:  
                self.kill()
                self.out=True
                
            if self.top_unrounded>=470 and self.player_num==2:
                self.bottom=480
                self.top_unrounded=470
                self.pi_direction-=(self.pi_direction-math.pi)*2
                
            if self.top_unrounded>=480 and self.player_num==1:
                self.kill()
                self.out=True
                
                
            if self.left_unrounded<=0:
                self.rect.left=0
                self.left_unrounded=0
                self.pi_direction-=(self.pi_direction-(math.pi/2))*2
                
            if self.left_unrounded>=630:
                self.rect.right=640
                self.left_unrounded=630
                self.pi_direction+=((math.pi/2)-self.pi_direction)*2
                
                
            if self.pi_direction<0:
                self.pi_direction+=2*math.pi
            if self.pi_direction>2*math.pi:
                self.pi_direction-=2*math.pi
                
                
            self.top_unrounded-=math.sin(self.pi_direction)*Paddle.paddles[self.player_num-1].ball_speed
            self.left_unrounded+=math.cos(self.pi_direction)*Paddle.paddles[self.player_num-1].ball_speed
            
            self.rect.top=self.top_unrounded
            self.rect.left=self.left_unrounded
            
            
            if self.player_num==1 and self.rect.centery>Paddle.paddles[0].rect.top:
                self.passed_paddle=True
            if self.player_num==2 and self.rect.centery<Paddle.paddles[1].rect.bottom:
                self.passed_paddle=True
            
            
            
class PowerUp(pygame.sprite.Sprite):
    def __init__(self, power_up_type, player, top, left, img_dirr):
        '''
        P.__init__(String, int, int, int, String)
        Initializes PowerUp
        
        A power-up that falls towards a player. It takes 5 arguments. The first
        argument is a string that describes what this power-up will do when 
        picked-up. The second argument is an int refering to which player the 
        power up should move towards. The third argument is the y corrdinate for
        where the tile will be displayed on screen. The forth argument is 
        the x corrdinate for where the tile will be displayed on screen. Final
        argument is a reference to the directory with the nessesary 
        images in it.
        '''
        
        
        pygame.sprite.Sprite.__init__(self)
        
        self.power_up_type=power_up_type
        
        
        if player==1:
            self.y_change=3
        if player==2:
            self.y_change=-3
            
        os.chdir(img_dirr)
        if power_up_type=="None":
            self.image=pygame.image.load("power_up.bmp")
        if power_up_type=="Speed_up": 
            self.image=pygame.image.load("speed_up_power_up.bmp").convert()
        if power_up_type=="Speed_down": 
            self.image=pygame.image.load("speed_down_power_up.bmp").convert()
        if power_up_type=="Paddle_grow": 
            self.image=pygame.image.load("paddle_grow_power_up.bmp").convert()
        if power_up_type=="Paddle_shrink": 
            self.image=pygame.image.load("paddle_shrink_power_up.bmp").convert()
        if power_up_type=="Multi_ball": 
            self.image=pygame.image.load("multi_ball_power_up.bmp").convert()
        if power_up_type=="Fire_5_balls": 
            self.image=pygame.image.load("fire_5_balls_power_up.bmp").convert()
            
            
            
        self.image.set_colorkey((255,255,255))
            
        self.rect=self.image.get_rect()
        self.rect.top=top
        self.rect.left=left
        
        self.gone=False
        
    def update(self):
        '''
        P.update() --> None
        Moved a powerup towards the player who broke its block.
        '''
        self.rect.top+=self.y_change
        
        if self.rect.top>480 or self.rect.bottom<0:
            self.gone=True
            self.kill()