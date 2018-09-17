
# coding: utf-8

# In[1]:

import pygame
import math
import numpy as np


# In[2]:

pygame.init()


# In[3]:


display_width = 800
display_height = 600

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('PACMAN')
clock = pygame.time.Clock()
black = (0,0,0)
white = (255,255,255)
red = (255,25,25)
pac = pygame.image.load('pacman.png')
pac = pygame.transform.scale(pac, (50, 50))
monst = pygame.image.load('monster.png')
monst = pygame.transform.scale(monst, (50, 50))

# In[4]:
def pacman(x,y,rotation_angle):
    img = pygame.transform.rotate(pac, rotation_angle)
    gameDisplay.blit(img, (x,y))

def monster(x,y,is_eaten):
    if not is_eaten:
        gameDisplay.blit(monst, (x,y))


## used to print messages on the screen

def printMsg(text_string,x,y):
    font = pygame.font.SysFont("comicsansms", 22)
    text = font.render(text_string, True, (0, 128, 0))
    gameDisplay.blit(text,(x, y))


#takes the locations of the monster and player and tells the monster which direction to move in
def calc_direction(mx,my,px,py):
    return 1

exit = False
x_change = 0
y_change = 0
x = 300
y = 500
is_eaten = False

#monster attributes
mon_x = 100
mon_y = 100
mon_vel_x = 5
mon_vel_y = 0

#used to make pacman face in the direction of movement
rot_angle = 0

## testing asin
print(np.degrees(math.asin(1)))

while not exit: 
    
    #making the monster stay inside the game window

    if (mon_x + mon_vel_x) > display_width or (mon_x + mon_vel_x) < 0:
        mon_vel_x = mon_vel_x * -1

    if (mon_y + mon_vel_y) > display_height or (mon_y + mon_vel_y) < 0:
        mon_vel_y = mon_vel_y * -1

    mon_x = mon_x + mon_vel_x
    mon_y = mon_y + mon_vel_y

    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            exit = True
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x_change = -5
                rot_angle = 180
            elif event.key == pygame.K_RIGHT:
                x_change = 5
                rot_angle = 0
            elif event.key == pygame.K_UP:
                y_change = -5
                rot_angle = 90
            elif event.key == pygame.K_DOWN:
                y_change = 5
                rot_angle = -90
            elif event.key == pygame.K_q:
                exit = True
        if event.type == pygame.KEYUP:
            
            x_change = 0
            y_change = 0
        
    
    x+= x_change
    y+= y_change

    gameDisplay.fill(white)
    pacman(x,y,rot_angle)
    monster(mon_x,mon_y,is_eaten)
    
    text1= "the distance between the centres is :"
    text_dst = text1 + str(0)
    #printMsg(text_dst,450,500)
    
    pygame.display.update()
    
    clock.tick(60)



pygame.quit()
quit()

