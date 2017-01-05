import pygame
from pygame.locals import *
pygame.init()

import math
import random
import os

import classes

size=(640, 480)
screen=pygame.display.set_mode(size)
pygame.display.set_caption("Brick Break Vs")

base_dirr=os.getcwd()
img_dirr=base_dirr+"/images"
os.chdir(img_dirr)

pygame.key.set_repeat(1, 30)

background=pygame.Surface(size)
background=background.convert()

background.fill((255, 255, 255))

background_image=pygame.image.load("background_image.bmp").convert()

mouse=classes.Mouse()
m_group=pygame.sprite.Group(mouse)

helvet=pygame.font.match_font("Helvetica", True, False)

eracer=pygame.Surface(size).convert()
eracer.fill((255,255,255))

player_1=classes.Paddle(1, img_dirr)
player_2=classes.Paddle(2, img_dirr)

player_group=pygame.sprite.OrderedUpdates([player_1, player_2])

start_ball_1=classes.Ball(True, 1, img_dirr)
start_ball_2=classes.Ball(True, 2, img_dirr)

balls=[start_ball_1, start_ball_2]
ball_group=pygame.sprite.OrderedUpdates(balls)

power_ups=[]
power_up_group=pygame.sprite.OrderedUpdates(power_ups)

map_outline=pygame.Surface((516, 388)).convert()
map_outline.fill((124,124,124))   

maps=[]
for i in range(1,4):
    new_map_img=pygame.image.load("map_{}.bmp".format(i)).convert()
    maps+=[new_map_img]

p1_left=False
p1_right=False
p2_left=False
p2_right=False

p1_left_key=97
p1_right_key=100
p2_left_key=276
p2_right_key=275

balls_launched=False
timer_to_launch=90
go_word_timer=20

#Defines Misc menu things
menu_font=pygame.font.Font(helvet, 16)

back_text=menu_font.render("Back", True, (255,255,255))
back_button=pygame.image.load("button.bmp").convert()
back_button.set_colorkey((255,0,255))
back_button=pygame.transform.scale(back_button, (90, 25))
back_button.blit(back_text, (5, 5))

left_arrow=pygame.image.load("arrow_left.bmp").convert()
left_arrow.set_colorkey((255,0,255))
left_arrow=pygame.transform.scale(left_arrow, (10, 15))

right_arrow=pygame.image.load("arrow_right.bmp").convert()
right_arrow.set_colorkey((255,0,255))
right_arrow=pygame.transform.scale(right_arrow, (10, 15))

button_expanded_box=pygame.image.load("time_amount_box.bmp").convert()
button_expanded_box.set_colorkey((255,0,255))


#Defines main menu variables
rules_button=classes.Button("Rules", 530, 50, menu_font, img_dirr)
map_button=classes.Button("Map", 530, 100, menu_font, img_dirr)
time_button=classes.Button("Time", 530, 150, menu_font, img_dirr)
controls_button=classes.Button("Controls", 530, 200, menu_font, img_dirr)
advanced_button=classes.Button("Advanced", 530, 250, menu_font, img_dirr)
start_game_button=classes.Button("Start Game", 530, 300, menu_font, img_dirr)
map_num=0
match_time=180

less_time_arrow_rect=left_arrow.get_rect()
less_time_arrow_rect.left=time_button.rect.left+5
less_time_arrow_rect.top=time_button.rect.top+5

more_time_arrow_rect=right_arrow.get_rect()
more_time_arrow_rect.left=time_button.rect.right-15
more_time_arrow_rect.top=time_button.rect.top+5



#Defines rules menu objects

##
rules_text_1=menu_font.render("This is a 2 player game where the goal is to outlast the other player. ", True, (0,0,0))
rules_text_2=menu_font.render("To stay alive, a player must keep at least 1 of their balls in play at all times. ", True, (0,0,0))
rules_text_3=menu_font.render("If a friendly ball passes your paddle, it is considered out of play.", True, (0,0,0))
rules_text_4=menu_font.render("If a Block is hit with a ball, it will break. When broken, some Blocks ", True, (0,0,0))
rules_text_5=menu_font.render("will drop a Power-Up. Power-Ups will fall towards whoever broke their Block.", True, (0,0,0))
rules_text_6=menu_font.render("The colour of a ball will show which player controls it. ", True, (0,0,0))
rules_text_7=menu_font.render("If a player hits an enemy ball, they will be eliminated.", True, (0,0,0))

rules_back_button_rect=back_button.get_rect()
rules_back_button_rect.left=530
rules_back_button_rect.top=440




#Defines controls menu objects
player_1_text=menu_font.render("Player 1:", True, (0,0,0))

player_1_left_control_text=menu_font.render("a", True, (255,255,255))
player_1_left_control_button=pygame.image.load("button.bmp").convert()
player_1_left_control_button.set_colorkey((255,0,255))
player_1_left_control_button=pygame.transform.scale(player_1_left_control_button, (90, 25))
player_1_left_control_button_rect=player_1_left_control_button.get_rect()
player_1_left_control_button_rect.left=210
player_1_left_control_button_rect.top=80

player_1_right_control_text=menu_font.render("d", True, (255,255,255))
player_1_right_control_button=pygame.image.load("button.bmp").convert()
player_1_right_control_button.set_colorkey((255,0,255))
player_1_right_control_button=pygame.transform.scale(player_1_right_control_button, (90, 25))
player_1_right_control_button_rect=player_1_right_control_button.get_rect()
player_1_right_control_button_rect.left=210
player_1_right_control_button_rect.top=120

player_2_text=menu_font.render("Player 2:", True, (0,0,0))

player_2_left_control_text=menu_font.render("left", True, (255,255,255))
player_2_left_control_button=pygame.image.load("button.bmp").convert()
player_2_left_control_button.set_colorkey((255,0,255))
player_2_left_control_button=pygame.transform.scale(player_2_left_control_button, (90, 25))
player_2_left_control_button_rect=player_2_left_control_button.get_rect()
player_2_left_control_button_rect.left=210
player_2_left_control_button_rect.top=280

player_2_right_control_text=menu_font.render("right", True, (255,255,255))
player_2_right_control_button=pygame.image.load("button.bmp").convert()
player_2_right_control_button.set_colorkey((255,0,255))
player_2_right_control_button=pygame.transform.scale(player_2_right_control_button, (90, 25))
player_2_right_control_button_rect=player_2_right_control_button.get_rect()
player_2_right_control_button_rect.left=210
player_2_right_control_button_rect.top=320

move_left_text=menu_font.render("Move Left:", True, (0,0,0))
move_right_text=menu_font.render("Move Right:", True, (0,0,0))

controls_back_button_rect=back_button.get_rect()
controls_back_button_rect.left=530
controls_back_button_rect.top=440

enter_key_font=pygame.font.Font(helvet, 40)
press_a_key_text=enter_key_font.render("Press Any Key", True, (255,255,255))
entering_key_filter=pygame.Surface(size).convert()
entering_key_filter.fill((0,0,0)) 
entering_key_filter.set_alpha(150) 

entering_key=False
bound_keys=[97, 100, 276, 275, -1]


#Defines advanced options menu objects
tie_breaker_text=menu_font.render("Time Limit:", True, (0,0,0))
tie_breaker=False
tie_breaker_box_unchecked=pygame.image.load("check_box_empty.bmp").convert()
tie_breaker_box_unchecked.set_colorkey((255,0,255))
tie_breaker_box_checked=pygame.image.load("check_box_checked.bmp").convert()
tie_breaker_box_checked.set_colorkey((255,0,255))
tie_breaker_box_rect=tie_breaker_box_unchecked.get_rect()
tie_breaker_box_rect.centerx=170
tie_breaker_box_rect.centery=100

tie_breaker_menu=pygame.image.load("advanced_extra_options_menu.bmp").convert()
tie_breaker_menu.set_colorkey((255,0,255))

tie_breaker_type_text=menu_font.render("Tie Breaker:", True, (0,0,0))

blocks_broken_text=menu_font.render("Most Blocks Broken", True, (0,0,0))
blocks_broken_box_unchecked=pygame.image.load("check_box_empty.bmp").convert()
blocks_broken_box_unchecked.set_colorkey((255,0,255))
blocks_broken_box_checked=pygame.image.load("check_box_checked.bmp").convert()
blocks_broken_box_checked.set_colorkey((255,0,255))
blocks_broken_box_rect=blocks_broken_box_unchecked.get_rect()
blocks_broken_box_rect.left=180
blocks_broken_box_rect.top=200

most_balls_text=menu_font.render("Most Balls", True, (0,0,0))
most_balls_box_unchecked=pygame.image.load("check_box_empty.bmp").convert()
most_balls_box_unchecked.set_colorkey((255,0,255))
most_balls_box_checked=pygame.image.load("check_box_checked.bmp").convert()
most_balls_box_checked.set_colorkey((255,0,255))
most_balls_box_rect=most_balls_box_unchecked.get_rect()
most_balls_box_rect.left=180
most_balls_box_rect.top=250

least_balls_dropped_text=menu_font.render("Least Balls Dropped", True, (0,0,0))
least_balls_dropped_box_unchecked=pygame.image.load("check_box_empty.bmp").convert()
least_balls_dropped_box_unchecked.set_colorkey((255,0,255))
least_balls_dropped_box_checked=pygame.image.load("check_box_checked.bmp").convert()
least_balls_dropped_box_checked.set_colorkey((255,0,255))
least_balls_dropped_box_rect=least_balls_dropped_box_unchecked.get_rect()
least_balls_dropped_box_rect.left=180
least_balls_dropped_box_rect.top=300

tie_breaker_type="blocks_broken"

blocks_respawn_text=menu_font.render("Blocks Respawn:", True, (0,0,0))
blocks_respawn=False
blocks_respawn_box_unchecked=pygame.image.load("check_box_empty.bmp").convert()
blocks_respawn_box_unchecked.set_colorkey((255,0,255))
blocks_respawn_box_checked=pygame.image.load("check_box_checked.bmp").convert()
blocks_respawn_box_checked.set_colorkey((255,0,255))
blocks_respawn_box_rect=blocks_respawn_box_unchecked.get_rect()
blocks_respawn_box_rect.centerx=470
blocks_respawn_box_rect.centery=100

respawn_options_text=menu_font.render("Respawn Options:", True, (0,0,0))

blocks_respawn_menu=pygame.image.load("advanced_extra_options_menu.bmp").convert()
blocks_respawn_menu.set_colorkey((255,0,255))

respawn_frequency_text=menu_font.render("Respawn Frequency:", True, (0,0,0))

lower_respawn_frequency_arrow_rect=right_arrow.get_rect()
lower_respawn_frequency_arrow_rect.centerx=460
lower_respawn_frequency_arrow_rect.centery=200

higher_respawn_frequency_arrow_rect=right_arrow.get_rect()
higher_respawn_frequency_arrow_rect.centerx=530
higher_respawn_frequency_arrow_rect.centery=200

high_frequency_text=menu_font.render("High", True, (0,0,0))
medium_frequency_text=menu_font.render("Medium", True, (0,0,0))
low_frequency_text=menu_font.render("Low", True, (0,0,0))

respawn_frequency_level=2

random_types_text=menu_font.render("Respawn As Random Blocks:", True, (0,0,0))
random_types_box_unchecked=pygame.image.load("check_box_empty.bmp").convert()
random_types_box_unchecked.set_colorkey((255,0,255))
random_types_box_checked=pygame.image.load("check_box_checked.bmp").convert()
random_types_box_checked.set_colorkey((255,0,255))
random_types_box_rect=random_types_box_unchecked.get_rect()
random_types_box_rect.left=520
random_types_box_rect.top=250
random_respawn_types=False

advanced_back_button_rect=back_button.get_rect()
advanced_back_button_rect.left=530
advanced_back_button_rect.top=440


#Creates the box that displays the winner
win_menu_box=pygame.image.load("win_menu_box.bmp").convert()
win_menu_box.set_colorkey((255,0,255))
win_menu_box=pygame.transform.scale(win_menu_box, (250, 300))
winner_font=pygame.font.Font(helvet, 20)
win_screen_img=pygame.Surface(size).convert()
play_again_button=classes.Button("Play Again", 275, 230, menu_font, img_dirr)
setup_from_win_button=classes.Button("Setup Game", 275, 270, menu_font, img_dirr)


update_time_left_counter=0

clicked=False

in_game=False
create_map=False

current_menu="setup_match_multi"
game_over=False


clock=pygame.time.Clock()
keep_going=True

while keep_going:
    
    clock.tick(30)
    
    background.blit(eracer, (0,0)) 
    background.blit(background_image, (0,0))
    clicked=False
    
    for ev in pygame.event.get():
        
        if ev.type==QUIT:
            keep_going=False
            
        if ev.type==KEYDOWN:
            if entering_key==True:
                if ev.key in bound_keys:
                    bound_keys[bound_keys.index(ev.key)]=bound_keys[action_to_rebind_pos]
                bound_keys[4]=ev.key
            
            if ev.key==K_ESCAPE:
                keep_going=False
                
            if ev.key==p1_left_key:
                p1_left=True
            if ev.key==p1_right_key:
                p1_right=True
                
            if ev.key==p2_left_key:
                p2_left=True
            if ev.key==p2_right_key:
                p2_right=True
                
        if ev.type==KEYUP:
            if ev.key==p1_left_key:
                p1_left=False
            if ev.key==p1_right_key:
                p1_right=False
                
            if ev.key==p2_left_key:
                p2_left=False
            if ev.key==p2_right_key:
                p2_right=False
                
        if ev.type==MOUSEMOTION:
            mouse.x=ev.pos[0]
            mouse.y=ev.pos[1]
            
        if ev.type==MOUSEBUTTONUP:
            clicked=True
                
                
    if in_game==False:   
        
        #If the player is currently seting up the match
        if current_menu=="setup_match_multi":
            
            collisions=mouse.rect.colliderect(rules_button.rect)
            if collisions==1 and clicked==True:
                current_menu="rules_menu"
                clicked=False
            
            collisions=mouse.rect.colliderect(map_button.rect)
            if collisions==1 and clicked==True:
                map_num+=1
                if map_num==len(maps):
                    map_num=0
                clicked=False
                
            collisions=mouse.rect.colliderect(less_time_arrow_rect)
            if collisions==1 and clicked==True:
                match_time=max(60, match_time-30)
                clicked=False
                
            collisions=mouse.rect.colliderect(more_time_arrow_rect)
            if collisions==1 and clicked==True:
                match_time=min(600, match_time+30)
                clicked=False
                
            collisions=mouse.rect.colliderect(controls_button.rect)
            if collisions==1 and clicked==True:
                clicked=False
                current_menu="controls_rebind_2_players"
                
            collisions=mouse.rect.colliderect(advanced_button.rect)
            if collisions==1 and clicked==True:
                clicked=False
                current_menu="advanced_setup"
                
            collisions=mouse.rect.colliderect(start_game_button.rect)
            if collisions==1 and clicked==True:
                create_map=True
                clicked=False
                
            match_time_text=menu_font.render("{}:{:0>2}".format(int(match_time/60), int(match_time)-(int(match_time/60)*60)), True, (0,0,0))
            
            background.blit(rules_button.image, rules_button.rect)             
            background.blit(map_button.image, map_button.rect) 
            background.blit(time_button.image, time_button.rect)
            background.blit(left_arrow, less_time_arrow_rect)
            background.blit(right_arrow, more_time_arrow_rect)         
            background.blit(button_expanded_box, (time_button.rect.left+10, time_button.rect.bottom))
            background.blit(match_time_text, (time_button.rect.left+32, time_button.rect.bottom))
            background.blit(controls_button.image, controls_button.rect)  
            background.blit(advanced_button.image, advanced_button.rect)  
            background.blit(start_game_button.image, start_game_button.rect) 
            background.blit(map_outline, (3,3))       
            background.blit(maps[map_num], (5,5))
            
            
        ##
        #If the player is in the rules menu
        if current_menu=="rules_menu":
            
            
            collisions=mouse.rect.colliderect(rules_back_button_rect)
            if collisions==1 and clicked==True:
                current_menu="setup_match_multi"
            
            
            
            
            
            background.blit(back_button, rules_back_button_rect) 
            background.blit(rules_text_1, (40, 50)) 
            background.blit(rules_text_2, (40, 80)) 
            background.blit(rules_text_3, (40, 100)) 
            background.blit(rules_text_4, (40, 130)) 
            background.blit(rules_text_5, (40, 150)) 
            background.blit(rules_text_6, (40, 180)) 
            background.blit(rules_text_7, (40, 210)) 
            
            
            
            
            
            
        #If the player is in the controls menu
        if current_menu=="controls_rebind_2_players":
            if entering_key==True and bound_keys[4]!=-1:
                
                bound_keys[action_to_rebind_pos]=bound_keys[4]
                
                p1_left_key=bound_keys[0]
                p1_right_key=bound_keys[1]
                p2_left_key=bound_keys[2]
                p2_right_key=bound_keys[3]
                player_1_left_control_text=menu_font.render(pygame.key.name(p1_left_key), True, (255,255,255))
                player_1_right_control_text=menu_font.render(pygame.key.name(p1_right_key), True, (255,255,255))
                player_2_left_control_text=menu_font.render(pygame.key.name(p2_left_key), True, (255,255,255))
                player_2_right_control_text=menu_font.render(pygame.key.name(p2_right_key), True, (255,255,255))
                
                entering_key=False
                bound_keys[4]=-1
                    
            collisions=mouse.rect.colliderect(player_1_left_control_button_rect)
            if collisions==1 and clicked==True and entering_key==False:
                action_to_rebind_pos=0
                entering_key=True
                clicked=False
                
            collisions=mouse.rect.colliderect(player_1_right_control_button_rect)
            if collisions==1 and clicked==True and entering_key==False:
                action_to_rebind_pos=1
                entering_key=True
                clicked=False
                
            collisions=mouse.rect.colliderect(player_2_left_control_button_rect)
            if collisions==1 and clicked==True and entering_key==False:
                action_to_rebind_pos=2
                entering_key=True
                clicked=False
                
            collisions=mouse.rect.colliderect(player_2_right_control_button_rect)
            if collisions==1 and clicked==True and entering_key==False:
                action_to_rebind_pos=3
                entering_key=True
                clicked=False
                
            collisions=mouse.rect.colliderect(controls_back_button_rect)
            if collisions==1 and clicked==True and entering_key==False:
                current_menu="setup_match_multi"
                clicked=False
            
            
            background.blit(player_1_text, (50, 100))   
            background.blit(move_left_text, (200-move_left_text.get_size()[0], 80))   
            background.blit(move_right_text, (200-move_right_text.get_size()[0], 120))  
            background.blit(player_1_left_control_button, player_1_left_control_button_rect)  
            background.blit(player_1_left_control_text, (player_1_left_control_button_rect.left+5, player_1_left_control_button_rect.top+5))
            background.blit(player_1_right_control_button, player_1_right_control_button_rect)  
            background.blit(player_1_right_control_text, (player_1_right_control_button_rect.left+5, player_1_right_control_button_rect.top+5))
            background.blit(player_2_text, (50, 300))    
            background.blit(move_left_text, (200-move_left_text.get_size()[0], 280))   
            background.blit(move_right_text, (200-move_right_text.get_size()[0], 320))  
            background.blit(player_2_left_control_button, player_2_left_control_button_rect)  
            background.blit(player_2_left_control_text, (player_2_left_control_button_rect.left+5, player_2_left_control_button_rect.top+5))
            background.blit(player_2_right_control_button, player_2_right_control_button_rect)  
            background.blit(player_2_right_control_text, (player_2_right_control_button_rect.left+5, player_2_right_control_button_rect.top+5))  
            background.blit(back_button, controls_back_button_rect) 
            
            if entering_key==True:
                background.blit(entering_key_filter, (0, 0))   
                background.blit(press_a_key_text, (int(size[0]/2-press_a_key_text.get_size()[0]/2), int(size[1]/2-press_a_key_text.get_size()[1]/2)))   
                
        #If the player is in the advanced options menu
        if current_menu=="advanced_setup":
            
            collisions=mouse.rect.colliderect(tie_breaker_box_rect)
            if collisions==1 and clicked==True:
                if tie_breaker==True:
                    tie_breaker=False
                elif tie_breaker==False:
                    tie_breaker=True
                clicked=False
                
            #Handles Tie-breaker related things
            collisions=mouse.rect.colliderect(blocks_broken_box_rect)
            if collisions==1 and clicked==True and tie_breaker==True:
                tie_breaker_type="blocks_broken"
                clicked=False
            collisions=mouse.rect.colliderect(most_balls_box_rect)
            if collisions==1 and clicked==True and tie_breaker==True:
                tie_breaker_type="most_balls"
                clicked=False
            collisions=mouse.rect.colliderect(least_balls_dropped_box_rect)
            if collisions==1 and clicked==True and tie_breaker==True:
                tie_breaker_type="least_balls_dropped"
                clicked=False
            collisions=mouse.rect.colliderect(blocks_respawn_box_rect)
            if collisions==1 and clicked==True:
                if blocks_respawn==True:
                    blocks_respawn=False
                elif blocks_respawn==False:
                    blocks_respawn=True
                clicked=False
                
            #Handles things related to respawnings blocks
            collisions=mouse.rect.colliderect(lower_respawn_frequency_arrow_rect)
            if collisions==1 and clicked==True:
                respawn_frequency_level=max(1, respawn_frequency_level-1)
                clicked=False
            collisions=mouse.rect.colliderect(higher_respawn_frequency_arrow_rect)
            if collisions==1 and clicked==True:
                respawn_frequency_level=min(3, respawn_frequency_level+1)
                clicked=False
            collisions=mouse.rect.colliderect(random_types_box_rect)
            if collisions==1 and clicked==True and blocks_respawn==True:
                if random_respawn_types==True:
                    random_respawn_types=False
                elif random_respawn_types==False:
                    random_respawn_types=True
                clicked=False
                
            #Returns the player to the setup match menu
            collisions=mouse.rect.colliderect(advanced_back_button_rect)
            if collisions==1 and clicked==True:
                current_menu="setup_match_multi"
                clicked=False
            
            background.blit(tie_breaker_text, (tie_breaker_box_rect.left-tie_breaker_text.get_size()[0]-7, tie_breaker_box_rect.top-4))
            if tie_breaker==True:
                background.blit(tie_breaker_box_checked, tie_breaker_box_rect)
                background.blit(tie_breaker_menu, (5, 120))
                background.blit(tie_breaker_type_text, (50, 130))
                background.blit(blocks_broken_text, (blocks_broken_box_rect.left-blocks_broken_text.get_size()[0]-7, blocks_broken_box_rect.top-4))
                background.blit(most_balls_text, (most_balls_box_rect.left-most_balls_text.get_size()[0]-7, most_balls_box_rect.top-4))
                background.blit(least_balls_dropped_text, (least_balls_dropped_box_rect.left-least_balls_dropped_text.get_size()[0]-7, least_balls_dropped_box_rect.top-4))
                if tie_breaker_type=="blocks_broken":
                    background.blit(blocks_broken_box_checked, blocks_broken_box_rect)
                    background.blit(most_balls_box_unchecked, most_balls_box_rect)
                    background.blit(least_balls_dropped_box_unchecked, least_balls_dropped_box_rect)
                if tie_breaker_type=="most_balls":
                    background.blit(blocks_broken_box_unchecked, blocks_broken_box_rect)
                    background.blit(most_balls_box_checked, most_balls_box_rect)
                    background.blit(least_balls_dropped_box_unchecked, least_balls_dropped_box_rect)
                if tie_breaker_type=="least_balls_dropped":
                    background.blit(blocks_broken_box_unchecked, blocks_broken_box_rect)
                    background.blit(most_balls_box_unchecked, most_balls_box_rect)
                    background.blit(least_balls_dropped_box_checked, least_balls_dropped_box_rect)
                    
                
            if tie_breaker==False:
                background.blit(tie_breaker_box_unchecked, tie_breaker_box_rect)
                
            background.blit(blocks_respawn_text, (blocks_respawn_box_rect.left-blocks_respawn_text.get_size()[0]-7, blocks_respawn_box_rect.top-4))
            if blocks_respawn==True:
                background.blit(blocks_respawn_box_checked, blocks_respawn_box_rect)
                background.blit(blocks_respawn_menu, (305, 120))
                background.blit(respawn_options_text, (350, 130))
                background.blit(respawn_frequency_text, (lower_respawn_frequency_arrow_rect.left-respawn_frequency_text.get_size()[0]-7, lower_respawn_frequency_arrow_rect.top-4))
                if respawn_frequency_level==1:
                    background.blit(low_frequency_text, (int(lower_respawn_frequency_arrow_rect.centerx+(higher_respawn_frequency_arrow_rect.centerx-lower_respawn_frequency_arrow_rect.centerx)/2-low_frequency_text.get_size()[0]/2), lower_respawn_frequency_arrow_rect.top-2))
                    background.blit(right_arrow, higher_respawn_frequency_arrow_rect)
                if respawn_frequency_level==2:
                    background.blit(medium_frequency_text, (int(lower_respawn_frequency_arrow_rect.centerx+(higher_respawn_frequency_arrow_rect.centerx-lower_respawn_frequency_arrow_rect.centerx)/2-medium_frequency_text.get_size()[0]/2), lower_respawn_frequency_arrow_rect.top-2))
                    background.blit(left_arrow, lower_respawn_frequency_arrow_rect)
                    background.blit(right_arrow, higher_respawn_frequency_arrow_rect)
                if respawn_frequency_level==3:
                    background.blit(high_frequency_text, (int(lower_respawn_frequency_arrow_rect.centerx+(higher_respawn_frequency_arrow_rect.centerx-lower_respawn_frequency_arrow_rect.centerx)/2-high_frequency_text.get_size()[0]/2), lower_respawn_frequency_arrow_rect.top-2))
                    background.blit(left_arrow, lower_respawn_frequency_arrow_rect)
                background.blit(random_types_text, (random_types_box_rect.left-random_types_text.get_size()[0]-18, random_types_box_rect.top-4))
                if random_respawn_types==False:
                    background.blit(random_types_box_unchecked, random_types_box_rect)
                if random_respawn_types==True:
                    background.blit(random_types_box_checked, random_types_box_rect)
                    
                
            if blocks_respawn==False:
                background.blit(blocks_respawn_box_unchecked, blocks_respawn_box_rect)
                
            background.blit(back_button, advanced_back_button_rect)
                
                
        #If the player is currently looking at You Win screen
        if current_menu=="win_screen":
            
            collisions=mouse.rect.colliderect(play_again_button.rect)
            if collisions==1 and clicked==True:
                create_map=True              
                clicked=False
                
            collisions=mouse.rect.colliderect(setup_from_win_button.rect)
            if collisions==1 and clicked==True:
                current_menu="setup_match_multi"
                clicked=False
            
            
            background.blit(win_screen_img, (0,0))
            background.blit(win_menu_box, (320-win_menu_box.get_size()[0]/2, 240-win_menu_box.get_size()[1]/2))
            background.blit(winner_text_line_1, (320-winner_text_line_1.get_size()[0]/2, 95))
            if winner_text_line_2!=None:
                background.blit(winner_text_line_2, (320-winner_text_line_2.get_size()[0]/2,120))
            if winner_text_line_3!=None:
                background.blit(winner_text_line_3, (320-winner_text_line_3.get_size()[0]/2,145))
            if winner_text_line_4!=None:
                background.blit(winner_text_line_4, (320-winner_text_line_4.get_size()[0]/2,170))
                
            background.blit(play_again_button.image, play_again_button.rect)
            background.blit(setup_from_win_button.image, setup_from_win_button.rect)
         
    if create_map==True:
        in_game=True
        time_left=match_time
        
        #Sets time for respawning blocks
        if respawn_frequency_level==1:
            respawn_frequency_time=50
        if respawn_frequency_level==2:
            respawn_frequency_time=30
        if respawn_frequency_level==3:
            respawn_frequency_time=20
        
        #Creates the chosen map
        create_map=False
        tiles=[]
            
        if map_num==0:
            for i in range(0,112):
                if i<16 or i>=96:
                    tile_type="None"
                if i>=16 and i<24:
                    tile_type="Multi_ball"
                if i>=24 and i<32:
                    tile_type="Paddle_shrink"
                if i>=32 and i<40:
                    tile_type="Speed_down"
                if i>=40 and i<48:
                    tile_type="Paddle_grow"
                if i>=48 and i<64:
                    tile_type="Speed_up"
                if i>=64 and i<72:
                    tile_type="Speed_down"
                if i>=72 and i<80:
                    tile_type="Paddle_grow"
                if i>=80 and i<88:
                    tile_type="Multi_ball"
                if i>=88 and i<96:
                    tile_type="Paddle_shrink"
                if tile_type!="Metal":
                    tiles+=[classes.Tile(i*40-int(i/16)*640, int(i/16)*15+188, tile_type, img_dirr)]
                if tile_type=="Metal":
                    tiles+=[classes.Tile(i*40-int(i/16)*640, int(i/16)*15+188, tile_type, hits_to_distroy, img_dirr)]
                
        if map_num==1:
            for i in range(0,176):
                if i<16 or i>=160:
                    tile_type="None"
                if i>=16 and i<32:
                    tile_type="Speed_up"
                if i>=32 and i<48:
                    tile_type="Paddle_shrink"
                if i>=48 and i<64:
                    tile_type="Speed_down"
                if i>=64 and i<80:
                    tile_type="Paddle_grow"
                if i>=80 and i<96:
                    tile_type="Multi_ball"
                if i>=96 and i<112:
                    tile_type="Paddle_grow"
                if i>=112 and i<128:
                    tile_type="Speed_down"
                if i>=128 and i<144:
                    tile_type="Paddle_shrink"
                if i>=144 and i<160:
                    tile_type="Speed_up"
                if tile_type!="Metal":
                    tiles+=[classes.Tile(i*40-int(i/16)*640, int(i/16)*15+157, tile_type, img_dirr)]
                if tile_type=="Metal":
                    tiles+=[classes.Tile(i*40-int(i/16)*640, int(i/16)*15+157, tile_type, hits_to_distroy, img_dirr)]
                
        if map_num==2:
            for i in range(0,176):
                if i<80 or i>=96:
                    tile_type="Fire_5_balls"
                if i>=80 and i<96:
                    tile_type="Metal"
                    hits_to_distroy=15
                    
                if tile_type!="Metal":
                    tiles+=[classes.Tile(i*40-int(i/16)*640, int(i/16)*15+157, tile_type, img_dirr)]
                if tile_type=="Metal":
                    tiles+=[classes.Tile(i*40-int(i/16)*640, int(i/16)*15+157, tile_type, hits_to_distroy, img_dirr)]
                
        tile_group=pygame.sprite.Group(tiles)      
        
    if in_game==True:
        
        if balls_launched==True:
            #Update match timer
            update_time_left_counter+=1
            if update_time_left_counter==30:
                time_left-=1
                update_time_left_counter=0
                if time_left==0:
                    in_game=False
                    
            #move players
            if p1_left==True:
                player_1.rect.left-=5
            if p1_right==True:
                player_1.rect.left+=5
            if player_1.rect.left<0:
                player_1.rect.left=0
            if player_1.rect.right>size[0]:
                player_1.rect.right=size[0]
                
            if p2_left==True:
                player_2.rect.left-=5
            if p2_right==True:
                player_2.rect.left+=5
            if player_2.rect.left<0:
                player_2.rect.left=0
            if player_2.rect.right>size[0]:
                player_2.rect.right=size[0]
                
        if balls_launched==False:
            timer_to_launch-=1
            
            #If a player adjusts their launching angle
            if p1_left==True:
                if player_1.launching_angle<29:
                    player_1.launching_angle+=1
                elif not player_1.launching_angle<29:
                    player_1.launching_angle=29
            if p1_right==True:
                if player_1.launching_angle>2:
                    player_1.launching_angle-=1
                if not player_1.launching_angle>2:
                    player_1.launching_angle=2
            
            if p2_left==True:
                if player_2.launching_angle>34:
                    player_2.launching_angle-=1
                if not player_2.launching_angle>34:
                    player_2.launching_angle=34
            if p2_right==True:
                if player_2.launching_angle<60:
                    player_2.launching_angle+=1
                elif not player_2.launching_angle<60:
                    player_2.launching_angle=60
            
            if timer_to_launch==0:
                balls_launched=True
                start_ball_1.launched=True
                start_ball_2.launched=True
                
                start_ball_1.pi_direction=player_1.launching_angle*.1   
                start_ball_2.pi_direction=player_2.launching_angle*.1         
                
        #Check which balls are still in play, and update them
        player_1_alive=False
        player_2_alive=False
        for i in ball_group:
            
            if i.player_num==1 and i.out==False:
                player_1_alive=True
            if i.player_num==2 and i.out==False:
                player_2_alive=True
            
            #Checks is a ball has hit a block
            collisions=pygame.sprite.spritecollide(i, tile_group, False)
            
            #If a player breaks a block
            if i.player_num==1:
                for ii in collisions:
                    if ii.block_type!="Metal" and ii not in player_1.blocks_broken:
                        player_1.blocks_broken+=[ii]
            if i.player_num==2:
                for ii in collisions:
                    if ii.block_type!="Metal" and ii not in player_2.blocks_broken:
                        player_2.blocks_broken+=[ii]
                        
                        
            #Handles the physics if a ball hits 3 blocks
            if len(collisions)==3:
                i.pi_direction+=math.pi
                
            #Handles the physics if a ball hits 2 blocks            
            if len(collisions)==2:
                if i.rect.top>collisions[0].rect.top and i.rect.top>collisions[1].rect.top:
                    i.pi_direction-=(i.pi_direction)*2
                    
                if i.rect.bottom<collisions[0].rect.bottom and i.rect.bottom<collisions[1].rect.bottom:
                    i.pi_direction-=(i.pi_direction-math.pi)*2
                    
                if i.rect.left>collisions[0].rect.left and i.rect.left>collisions[1].rect.left:
                    i.pi_direction-=(i.pi_direction-(math.pi/2))*2
                    
                if i.rect.right<collisions[0].rect.right and i.rect.right<collisions[1].rect.right:
                    i.pi_direction+=((math.pi/2)-i.pi_direction)*2
                    
            #Handles the physics if a ball hits 1 block
            if len(collisions)==1:
                if i.pi_direction>=0 and i.pi_direction<math.pi/2:
                    if collisions[0].rect.bottom-i.rect.top>i.rect.right-collisions[0].rect.left:
                        i.pi_direction+=((math.pi/2)-i.pi_direction)*2
                    if collisions[0].rect.bottom-i.rect.top<i.rect.right-collisions[0].rect.left:
                        i.pi_direction-=(i.pi_direction)*2
                        
                elif i.pi_direction>=math.pi/2 and i.pi_direction<math.pi:
                    if collisions[0].rect.bottom-i.rect.top>collisions[0].rect.right-i.rect.left:
                        i.pi_direction-=(i.pi_direction-(math.pi/2))*2
                    if collisions[0].rect.bottom-i.rect.top<collisions[0].rect.right-i.rect.left:
                        i.pi_direction-=(i.pi_direction)*2
                        
                elif i.pi_direction>=math.pi and i.pi_direction<3*math.pi/2:
                    if i.rect.bottom-collisions[0].rect.top>collisions[0].rect.right-i.rect.left:
                        i.pi_direction-=(i.pi_direction-(math.pi/2))*2
                    if i.rect.bottom-collisions[0].rect.top<collisions[0].rect.right-i.rect.left:
                        i.pi_direction-=(i.pi_direction-math.pi)*2
                        
                        
                elif i.pi_direction>=3*math.pi/2 and i.pi_direction<math.pi*2:
                    if i.rect.bottom-collisions[0].rect.top>i.rect.right-collisions[0].rect.left:
                        i.pi_direction+=((math.pi/2)-i.pi_direction)*2
                    if i.rect.bottom-collisions[0].rect.top<i.rect.right-collisions[0].rect.left:
                        i.pi_direction-=(i.pi_direction-math.pi)*2
                        
                if i.pi_direction<0:
                    i.pi_direction+=2*math.pi
                if i.pi_direction>2*math.pi:
                    i.pi_direction-=2*math.pi
                    
            #Drops powerups is a special block is broken
            for ii in collisions:
                if ii.block_type!="Metal":
                    if ii.block_type!="None":
                        power_ups+=[classes.PowerUp(ii.block_type, i.player_num, ii.rect.top, ii.rect.left+5, img_dirr)]
                        
                    power_up_group=pygame.sprite.OrderedUpdates(power_ups)
                    for iii in power_ups:
                        if iii.gone==True:
                            iii.kill()
                                             
                    ii.time_distroyed=time_left
                    ii.kill()
                    
                #If a block is metal, this will strat breaking it
                if ii.block_type=="Metal":
                    ii.hits_to_distroy-=1
                    if ii.hits_to_distroy==1:
                        ii.block_type="None"
                        ii.image=pygame.image.load("normal_block.bmp").convert()
                    
            #Checks if any balls hit a paddle
            collisions=pygame.sprite.spritecollide(i, player_group, False)
            
            for ii in collisions:
                
                #Handles if a ball hits its player's paddle. The ball will go 
                #off at different angles depending on where it hits the paddle.
                if i.player_num==ii.player_num:
                    if i.player_num==1:
                        if i.passed_paddle==False:
                            i.pi_direction-=((i.pi_direction)*2)
                            while i.pi_direction<0:
                                i.pi_direction+=(math.pi)*2
                            if i.rect.centerx<ii.rect.centerx:
                                i.pi_direction+=(math.pi/6)*((ii.rect.left-i.rect.centerx+(ii.rect.size[0]/2))/(ii.rect.size[0]/2))
                            if ii.rect.centerx<i.rect.centerx:
                                i.pi_direction-=(math.pi/6)*((i.rect.centerx-ii.rect.left-(ii.rect.size[0]/2))/(ii.rect.size[0]/2))
                            i.rect.bottom=ii.rect.top
                            i.top_unrounded=i.rect.top
                        
                    if i.player_num==2:
                        if i.passed_paddle==False:
                            i.pi_direction-=((i.pi_direction-math.pi)*2)
                            while i.pi_direction<0:
                                i.pi_direction+=(math.pi)*2
                            if i.rect.centerx<ii.rect.centerx:
                                i.pi_direction-=(math.pi/6)*((ii.rect.left-i.rect.centerx+(ii.rect.size[0]/2))/(ii.rect.size[0]/2))
                            if ii.rect.centerx<i.rect.centerx:
                                i.pi_direction+=(math.pi/6)*((i.rect.centerx-ii.rect.left-(ii.rect.size[0]/2))/(ii.rect.size[0]/2))
                            i.rect.top=ii.rect.bottom
                            i.top_unrounded=i.rect.top
                        
                    while i.pi_direction<0:
                        i.pi_direction+=(math.pi)*2
                    while i.pi_direction>2*math.pi:
                        i.pi_direction-=(math.pi)*2
                        
                
                #Handles if a ball hits the opponents paddle
                if i.player_num!=ii.player_num:
                    winner=i.player_num
                    in_game=False
                    ii.kill()
                
              
        for i in player_group:
            #Checks to see if a player has gotten a power-up
            collisions=pygame.sprite.spritecollide(i, power_up_group, True)
            for ii in collisions:
                ii.gone=True
                if ii.power_up_type=="Multi_ball":
                    new_balls=[]
                    for iii in balls:
                        if iii.out==False:
                            if iii.player_num==i.player_num:
                                new_ball=classes.Ball(False, i.player_num, img_dirr)
                                new_ball.rect.top=iii.rect.top
                                new_ball.top_unrounded=new_ball.rect.top
                                new_ball.rect.left=iii.rect.left
                                new_ball.left_unrounded=new_ball.rect.left
                                new_ball.pi_direction=iii.pi_direction+(math.pi/2)+(random.randrange(0,314))/100 
                                new_balls+=[new_ball]
                                
                    balls+=new_balls
                    ball_group=pygame.sprite.OrderedUpdates(balls)
                if ii.power_up_type=="Speed_up":
                    i.ball_speed+=1
                if ii.power_up_type=="Speed_down":
                    i.ball_speed=max([1,i.ball_speed-1])
                if ii.power_up_type=="Paddle_grow":
                    i.image=pygame.Surface((min(i.image.get_size()[0]+10, 200),15)).convert()
                    if i.player_num==1:
                        i.image.fill((0,0,255))        
                    if i.player_num==2:
                        i.image.fill((255,0,0))     
                    old_left=i.rect.left
                    old_top=i.rect.top
                    i.rect=i.image.get_rect()
                    i.rect.left=old_left-5
                    i.rect.top=old_top
                if ii.power_up_type=="Paddle_shrink":
                    i.image=pygame.Surface((max(i.image.get_size()[0]-10, 40),15)).convert()
                    if i.player_num==1:
                        i.image.fill((0,0,255))        
                    if i.player_num==2:
                        i.image.fill((255,0,0))     
                    old_left=i.rect.left
                    old_top=i.rect.top
                    i.rect=i.image.get_rect()
                    i.rect.left=old_left+5
                    i.rect.top=old_top
                if ii.power_up_type=="Fire_5_balls":
                    new_balls=[]
                    for iii in range (0,5):
                        new_ball=classes.Ball(False, i.player_num, img_dirr)
                        if i.player_num==1:
                            new_ball.rect.bottom=i.rect.top
                        if i.player_num==2:
                            new_ball.rect.top=i.rect.bottom
                        new_ball.top_unrounded=new_ball.rect.top
                        new_ball.rect.centerx=i.rect.centerx
                        new_ball.left_unrounded=new_ball.rect.left
                        new_ball.pi_direction=math.pi*(iii+1)/6
                        if i.player_num==2:
                            new_ball.pi_direction+=math.pi
                            
                        new_balls+=[new_ball]
                    balls+=new_balls
                    ball_group=pygame.sprite.OrderedUpdates(balls)
                    
        #If blocks are allowed to respawn
        if blocks_respawn==True:
            respawning_blocks=[]
            for i in tiles:
                if i.time_distroyed!=None:
                    if i.respawning==False:
                        if i.time_distroyed-respawn_frequency_time>time_left:
                            if random.randrange(0,20)==0:
                                i.respawning=True
                                if random_respawn_types==False:
                                    i.block_type=i.original_block_type
                                    i.image=i.original_image
                                    if i.block_type=="Metal":
                                        i.hits_to_distroy=i.original_hits_to_distroy
                                if random_respawn_types==True:
                                    new_type_num=random.randint(1,10)
                                    if new_type_num==1: 
                                        i.block_type="Speed_up"
                                        i.image=pygame.image.load("speed_up_block.bmp").convert()
                                    if new_type_num==2: 
                                        i.block_type="Speed_down"
                                        i.image=pygame.image.load("speed_down_block.bmp").convert()
                                    if new_type_num==3: 
                                        i.block_type="Paddle_grow"
                                        i.image=pygame.image.load("paddle_grow_block.bmp").convert()
                                    if new_type_num==4:
                                        i.block_type="Paddle_shrink"
                                        i.image=pygame.image.load("paddle_shrink_block.bmp").convert()
                                    if new_type_num==5: 
                                        i.block_type="Multi_ball"
                                        i.image=pygame.image.load("multi_ball_block.bmp").convert()
                                    if new_type_num==6: 
                                        i.block_type="Fire_5_balls"
                                        i.image=pygame.image.load("fire_5_balls_block.bmp").convert()
                                    if new_type_num>6:
                                        i.block_type="None" 
                                        i.image=pygame.image.load("normal_block.bmp").convert()
                                    i.image.set_alpha(255)
                                
                    #Handles the flashing effect if a block is respawning
                    if i.respawning==True:
                        respawning_blocks+=[i]
                        i.respawn_timer-=1
                        if i.respawn_timer<=0:
                            if len(pygame.sprite.spritecollide(i, ball_group, False))==0:
                                i.time_distroyed=None
                                i.respawning=False
                                i.respawn_timer=7
                                i.image.set_alpha(255)
                                        
                                    
                                new_tiles=[]
                                for ii in tiles:
                                    if ii.time_distroyed==None:
                                        new_tiles+=[ii]
                                tile_group=pygame.sprite.Group(new_tiles)
                                
        #Display UI
        power_up_group.clear(screen, background)
        power_up_group.update()
        power_up_group.draw(background)
                    
        player_group.clear(screen, background)
        player_group.draw(background)
        tile_group.clear(screen, background)
        tile_group.draw(background)
        ball_group.clear(screen, background)
        ball_group.update()
        ball_group.draw(background)
        
        if blocks_respawn==True:
            for i in respawning_blocks:
                if i.time_distroyed!=None:
                    if i.image.get_alpha()==0:
                        i.image.set_alpha(255)
                    elif i.image.get_alpha()==255:
                        i.image.set_alpha(0)
                    background.blit(i.image, i.rect)
        
        time_left_text=menu_font.render("{}:{:0>2}".format(int(time_left/60), int(time_left)-(int(time_left/60)*60)), True, (0,0,0)) 
        background.blit(time_left_text, (600, 5))
        
        #Display UI during countdown
        if balls_launched==False:
            countdown_font=pygame.font.Font(helvet, 150)
            countdown_text=countdown_font.render(str(int(timer_to_launch/30)+1), True, (0,0,0))
            background.blit(countdown_text, (320-(countdown_text.get_size()[0]/2),240-(countdown_text.get_size()[1]/2)))
            player_1.arrow_image=pygame.image.load("arrow.bmp").convert()
            player_1.arrow_image=pygame.transform.rotate(player_1.arrow_image, (math.degrees(player_1.launching_angle*.1)))     
            player_1.arrow_image.set_colorkey((255,0,255))
            background.blit(player_1.arrow_image, (320-player_1.arrow_image.get_size()[0]/2, start_ball_1.rect.centery-(player_1.arrow_image.get_size()[1]/2)))  
            player_2.arrow_image=pygame.image.load("arrow.bmp").convert()
            player_2.arrow_image=pygame.transform.rotate(player_2.arrow_image, (math.degrees(player_2.launching_angle*.1)))    
            player_2.arrow_image.set_colorkey((255,0,255))
            background.blit(player_2.arrow_image, (320-player_2.arrow_image.get_size()[0]/2, start_ball_2.rect.centery-(player_2.arrow_image.get_size()[1]/2)))  
            
            
        #Ends countdown
        if balls_launched==True and go_word_timer!=0:
            go_font=pygame.font.Font(helvet, 150)
            go_text=go_font.render("GO!", True, (0,0,0))
            background.blit(go_text, (320-(go_text.get_size()[0]/2),240-(go_text.get_size()[1]/2)))
            
            go_word_timer-=1   
            
        #If someone won
        if player_1_alive==False:
            winner=2
            in_game=False
            player_1.kill()
        if player_2_alive==False:
            winner=1
            in_game=False
            player_2.kill()            
            
        if in_game==False:
            #If the game just ended
            current_menu="win_screen"
            win_screen_img.blit(background, (0,0))
            winner_text_line_2=None
            winner_text_line_3=None
            winner_text_line_4=None
            
            if time_left!=0:
                if len(player_group)==1:
                    winner_text_line_1=winner_font.render("Player {} wins!".format(winner), True, (255,255,255))
                if len(player_group)==0:
                    winner_text_line_1=winner_font.render("It's a tie!", True, (255,255,255))
            
            if time_left==0:
                winner_text_line_1=winner_font.render("Time's up!", True, (255,255,255))
                if tie_breaker==False:
                    winner_text_line_2=winner_font.render("It's a tie!", True, (255,255,255))
                    
                #Handles different types of ties
                if tie_breaker==True:
                    if tie_breaker_type=="blocks_broken":
                        winner_text_line_2=winner_font.render("Player 1 broke {} blocks".format(len(player_1.blocks_broken)), True, (255,255,255))
                        winner_text_line_3=winner_font.render("Player 2 broke {} blocks".format(len(player_2.blocks_broken)), True, (255,255,255))
                        if len(player_1.blocks_broken)>len(player_2.blocks_broken):
                            winner_text_line_4=winner_font.render("Player 1 wins!", True, (255,255,255))
                        if len(player_1.blocks_broken)<len(player_2.blocks_broken):
                            winner_text_line_4=winner_font.render("Player 2 wins!", True, (255,255,255))
                        if len(player_1.blocks_broken)==len(player_2.blocks_broken):
                            winner_text_line_4=winner_font.render("It's a tie!", True, (255,255,255))
                            
                    if tie_breaker_type=="most_balls":
                        p1_balls=0
                        p2_balls=0
                        for i in ball_group:
                            if i.out==False:
                                if i.player_num==1:
                                    p1_balls+=1
                                if i.player_num==2:
                                    p2_balls+=1
                        winner_text_line_2=winner_font.render("Player 1 has {} balls".format(p1_balls), True, (255,255,255))
                        winner_text_line_3=winner_font.render("Player 2 has {} balls".format(p2_balls), True, (255,255,255))
                        if p1_balls>p2_balls:
                            winner_text_line_4=winner_font.render("Player 1 wins!", True, (255,255,255))
                        if p1_balls<p2_balls:
                            winner_text_line_4=winner_font.render("Player 2 wins!", True, (255,255,255))
                        if p1_balls==p2_balls:
                            winner_text_line_4=winner_font.render("It's a tie!", True, (255,255,255))
                        
                    if tie_breaker_type=="least_balls_dropped":
                        p1_balls_dropped=0
                        p2_balls_dropped=0
                        for i in ball_group:
                            if i.out==True:
                                if i.player_num==1:
                                    p1_balls_dropped+=1
                                if i.player_num==2:
                                    p2_balls_dropped+=1
                        winner_text_line_2=winner_font.render("Player 1 lost {} balls".format(p1_balls_dropped), True, (255,255,255))
                        winner_text_line_3=winner_font.render("Player 2 lost {} balls".format(p2_balls_dropped), True, (255,255,255))
                        if p1_balls_dropped<p2_balls_dropped:
                            winner_text_line_4=winner_font.render("Player 1 wins!", True, (255,255,255))
                        if p1_balls_dropped>p2_balls_dropped:
                            winner_text_line_4=winner_font.render("Player 2 wins!", True, (255,255,255))
                        if p1_balls_dropped==p2_balls_dropped:
                            winner_text_line_4=winner_font.render("It's a tie!", True, (255,255,255))
                        
            #Restarts the game
            for i in power_up_group:
                i.kill()
            power_ups=[]
            for i in player_group:
                i.kill()
            classes.Paddle.paddles=[]
            for i in tile_group:
                i.kill()
            tiles=[]
            for i in ball_group:
                i.kill()
            balls=[]
            
            player_1=classes.Paddle(1, img_dirr)
            player_2=classes.Paddle(2, img_dirr)
            
            player_group=pygame.sprite.OrderedUpdates([player_1, player_2])
            
            start_ball_1=classes.Ball(True, 1, img_dirr)
            start_ball_2=classes.Ball(True, 2, img_dirr)
            
            balls=[start_ball_1, start_ball_2]
            ball_group=pygame.sprite.OrderedUpdates(balls)

            balls_launched=False
            timer_to_launch=90
            go_word_timer=20
            
    m_group.update()       
    screen.blit(background, (0, 0))
    pygame.display.flip()