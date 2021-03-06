

import pygame
import math
import numpy as np
import argparse



pygame.init()


display_width = 800
display_height = 800

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


## displays the pacman (player) on the game window

def pacman(x,y,rotation_angle):
    img = pygame.transform.rotate(pac, rotation_angle)
    gameDisplay.blit(img, (x,y))

## displays the monster on the game window

def monster(x,y,is_eaten):
    if not is_eaten:
        gameDisplay.blit(monst, (x,y))


## used to print messages on the screen

def printMsg(text_string,x,y):
    font = pygame.font.SysFont("comicsansms", 22)
    text = font.render(text_string, True, (0, 128, 0))
    gameDisplay.blit(text,(x, y))

## takes in the cordinates of the pacman and monster and the monster velocity and returns the angular velocities

def seek(x,y,mx,my,mvel):

    if (x - mx) == 0:
        if (y - my) > 0:
            theta = math.radians(90)
        elif (y - mon_y) < 0:
            theta = math.radians(-90)
        else:
            theta = math.radians(0)
    
    else : 

        tanVal = (y - my)/(x - mx)
        theta = (math.atan(tanVal))
    
    

    # right half :
    if (mx > x):
        mon_vel_x = mvel * math.cos(theta) * -1
        mon_vel_y = mvel * math.sin(theta) * -1
    
    ## left half
    else:

        mon_vel_x = mvel * math.cos(theta)
        mon_vel_y = mvel * math.sin(theta)    

    return mon_vel_x, mon_vel_y

def flee(x,y,mx,my,mvel,flee_radius):

    if calcDistance(x,y,mx,my) < flee_radius:

        ## divide by zero errors

        if (x - mx) == 0:
            if (y - my) > 0:
                theta = math.radians(90)
            elif (y - my) < 0:
                theta = math.radians(-90)
            else:
                theta = math.radians(0)
        
        else : 

            tanVal = (y - my)/(x - mx)
            theta = (math.atan(tanVal))
        
        

        # right half :
        if (mx > x):
            mon_vel_x = mvel * math.cos(theta)
            mon_vel_y = mvel * math.sin(theta)
        
        ## left half
        else:

            mon_vel_x = mvel * math.cos(theta) * -1
            mon_vel_y = mvel * math.sin(theta) * -1          


    else :
        ## monster stays in place if its more than 200 pixels away
        mon_vel_x = 0
        mon_vel_y = 0


    return mon_vel_x, mon_vel_y

def calcDistance(x1,y1,x2,y2):
    val = (x2-x1)**2
    val += (y2-y1)**2
    dist = math.sqrt(val)
    return dist

if __name__ == '__main__':

    #to implement seek/ chase/ flee
    parser = argparse.ArgumentParser(description="Conway's GOL")
    parser.add_argument('--behavior', dest='monsterBehavior', required=False)
    args = parser.parse_args()

    exit = False
    
    #pacman attributes
    x_change = 0
    y_change = 0
    x = 100
    y = 100
    

    #monster attributes
    theta = 0
    mon_x = 400
    mon_y = 400
    mon_vel = 3
    mon_vel_x = 0
    mon_vel_y = 0
    is_eaten = False

    ## test cordinates
    test_x = 400
    test_y = 400

    #used to make pacman face in the direction of movement
    rot_angle = 0

    ## testing asin
    #print(np.degrees(math.asin(1)))

    ## the main game loop

    while not exit: 
        
        ## MOVEMENT FOR THE PACMAN

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

        ## Monster movement
        ## making the monster stay inside the game window

        
        if args.monsterBehavior == 'seek':
    
            mon_vel_x, mon_vel_y = seek(x,y,mon_x,mon_y,mon_vel)

            mon_x = mon_x + mon_vel_x
            mon_y = mon_y + mon_vel_y

        elif args.monsterBehavior == 'chase':
            
            #chase is basically seek but for a future position
            mon_vel_x, mon_vel_y = seek(x+x_change, y+y_change, mon_x, mon_y, mon_vel)
            mon_x = mon_x + mon_vel_x
            mon_y = mon_y + mon_vel_y
        
        elif args.monsterBehavior == 'flee':
            
            ## monster starts fleeing if pacman is within 200 pixels

            mon_vel_x, mon_vel_y = flee(x, y, mon_x, mon_y,mon_vel,200)

            mon_x = mon_x + mon_vel_x
            mon_y = mon_y + mon_vel_y

            ## making the monster stay inside the windows
            if (mon_x > display_width -25) or (mon_x < 5) or (mon_y < 5) or (mon_y > display_height - 25):
                mon_x = mon_x - mon_vel_x
                mon_y = mon_y - mon_vel_y                

        else:

            if (mon_x + mon_vel_x) > display_width or (mon_x + mon_vel_x) < 0:
                mon_vel_x = mon_vel_x * -1

            if (mon_y + mon_vel_y) > display_height or (mon_y + mon_vel_y) < 0:
                mon_vel_y = mon_vel_y * -1

            mon_x = mon_x + mon_vel_x
            mon_y = mon_y + mon_vel_y

        ## displaying objects on the game window

        gameDisplay.fill(white)
        pacman(x,y,rot_angle)
        monster(mon_x,mon_y,is_eaten)
        
        '''
        # printing theta vals
        text1= "theta is :"
        text_theta = text1 + str(math.degrees(theta))
        printMsg(text_theta,400,30)
        '''

        #printing the distance at that tick
        text2= "Distance between monster and pacman :"
        text_dist = text2 + str(calcDistance(x,y,mon_x,mon_y))
        printMsg(text_dist,400,10)
        
        pygame.display.update()
        
        clock.tick(60)



    pygame.quit()
    quit()

