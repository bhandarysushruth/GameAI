

import pygame
import math
import numpy as np
import argparse
import random

#generating a path for path following
#from bresenham import bresenham

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
counter = 0

#contains the list of obstacles in the game world

obstacles = []


class Wall:
    def __init__(self,x,y,radius):
        self.x = x
        self.y = y
        self.radius = radius

    def render(self):
        pygame.draw.circle(gameDisplay, (0, 255, 0), (self.x, self.y), 10)


class Ghost:
    def __init__(self,x,y,velocity,max_vel):
        self.x = x
        self.y = y
        self.x_vel = 0
        self.y_vel = 0
        self.vel = velocity
        self.max_vel = max_vel

    def move(self,angle,wrap=False):
        
        if (wrap == False) and ((self.x > display_width - 20) or(self.y >display_height -40)):
            self.vel = 0

        self.x += self.vel * math.cos(math.radians(angle))
        self.y += self.vel * math.sin(math.radians(angle))
        
        if wrap == True:
            self.x %= display_width
            self.y %= display_height

    def render(self, visible):
        if visible == True:
            gameDisplay.blit(monst, (self.x,self.y))


## displays the pacman (player) on the game window
def pacman(x,y,rotation_angle,display_boolean):
    if display_boolean:
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


def dynamic_seek(following, leading, velocity_matching = True, stationary_target = False):

    if calcDistance(leading.x,leading.y,following.x,following.y) <= 10:
            following.x = leading.x -5
            following.y = leading.y
            following.vel = 0
            return
        

    if (leading.x - following.x) == 0:
        if (leading.y - following.y) > 0:
            theta = math.radians(90)
        elif (leading.y - following.y) < 0:
            theta = math.radians(-90)
        else:
            theta = math.radians(0)
    
    else : 

        tanVal = (leading.y - following.y)/(leading.x - following.x)
        theta = (math.atan(tanVal))
    
    #this will change the velocity with an acceleration of 1
    #it will change the vel attribute of the following object
    if stationary_target:
        match_velocity_stat(leading, following, 0.2, 50)
    elif velocity_matching == False:
        if calcDistance(following.x, following.y, leading.x, leading.y) < 30:
            decelerate(following, 0.2)
        else:
            accelerate(following, 0.2)
        
    else:
        match_vel(leading, following, 0.2)

    # right half :
    if (following.x > leading.x):
        mon_vel_x = following.vel * math.cos(theta) * -1
        mon_vel_y = following.vel * math.sin(theta) * -1
    
    ## left half
    else:

        mon_vel_x = following.vel * math.cos(theta)
        mon_vel_y = following.vel * math.sin(theta)    

    #return mon_vel_x, mon_vel_y
        following.x+=mon_vel_x
        following.y+=mon_vel_y

## takes in the cordinates of the target and monster and the monster velocity and returns the angular velocities

def seek(x,y,mx,my,mvel,velocity_matching=False,f_obj=None, l_obj=None):

    # avoiding oscilation at target arrival
    # this will make it land at the target
    if velocity_matching == True:
        dynamic_seek(f_obj, l_obj)
    else:
        if calcDistance(x,y,mx,my) <= mvel:
            return x-mx,y-my
        

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

def accelerate(follow, acceleration):
    if follow.vel < follow.max_vel:
        follow.vel += acceleration

def decelerate(follow, acceleration):
    if follow.vel > 0:
        follow.vel -= acceleration
    else:
        follow.vel = 0



# takes two objects and matches velocities for the folowing object to match the leading object
# it gives the following object an acceleration to make it look more realistic 
# this is match velocity for a moving target
def match_vel(lead,follow,acceleration):
    if follow.vel == lead.vel:
        pass
    elif (follow.vel < lead.vel) and (follow.vel < follow.max_vel):
        follow.vel += acceleration
    else:
        follow.vel-= acceleration

#used to give the object an acceleration and deceleration
def match_velocity_stat(lead, follow, acceleration, deceleration_radius):
    if calcDistance(lead.x, lead.y, follow.x, follow.y) <= deceleration_radius:
        if calcDistance(lead.x, lead.y, follow.x, follow.y) <= 15:
            pass
        else:
            if follow.vel > 0:
                follow.vel -= acceleration
            else:
                follow.vel = 0
    else:
        if follow.vel < follow.max_vel:
            follow.vel += acceleration
        else:
            follow.vel = follow.max_vel



def flee(x,y,mx,my,mvel,flee_radius, collision_avoid = False):

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
        
        
        if collision_avoid:
            theta*=-1
            theta+= math.radians(45)

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

#takes input as old seek x and y. Also takes monster cordinates and vel as input to pass to seek
#
#returns velocities for new seek position.(new seek is the same as old seek for 5 ticks)
def wander(oseek_x, oseek_y, mx, my, mvel):
    #follows a given path 5 ticks
    if self.counter % 5 == 0:
        #rand_x = random.randint(oseek_x+100, oseek_x - 100)
        #rand_y = random.randint(oseek_y+100, oseek_y - 100)
        rand_x = random.randint(0, 500)
        rand_y = random.randint(0, 500)
        counter+=0
    else:
        rand_x = oseek_x
        rand_y = oseek_y
        counter+=1

    return seek(rand_x, rand_y, mx, my, mvel)


## --------------------------------------- MAIN ---------------------------------------------

if __name__ == '__main__':

    ## -------------------- SETTING UP ENVIRONMENTS AND VARIABLES ------------------------------

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
    is_displayed = True
    

    #monster attributes
    theta = 0
    if args.monsterBehavior == 'path':    
        mon_x = 50
        mon_y = 50
    else:
        mon_x = 400
        mon_y = 400
    mon_vel = 3
    mon_vel_x = 0
    mon_vel_y = 0
    is_eaten = False

    #creating a monster for v_math

    if args.monsterBehavior =='v_match':
        ghost_lead = Ghost(200, 100, 5, 10)
        ghost_following = Ghost(200, 50, 0, 10)

    ## variables for wander
    seek_x = random.randint(50,display_width-50) 
    seek_y = random.randint(50, display_height-50)

    #variables for path
    if args.monsterBehavior == 'path':
        point_list = list(bresenham(50,50,200,200))
        point_list+=  list(bresenham(250,200,250,700))
        point_list+=  list(bresenham(500,700,350,200))
        point_list+=  list(bresenham(350,200,600,200))  
        point_counter = 0

    #used to make pacman face in the direction of movement
    rot_angle = 0

    ## for obstacles mode :
    # flag to display obstacles
    obstacles_present = False

    if args.monsterBehavior == 'obstacles':
        obstacles.append(Wall(500, 400, 10))
        obstacles.append(Wall(300, 400, 10))
        ghost_target = Ghost(700, 410, 0, 0)
        ghost_chase = Ghost(100, 390, 0, 2)


    if args.monsterBehavior == 'pursue':
        ghost_target = Ghost(100, 300, 4, 4)
        ghost_chase = Ghost(100, 600, 2, 10)


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

       
       ## ------------------- VELOCITY/MOVEMENT CALCULATIONS ---------------------------------------

        
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

        elif args.monsterBehavior == 'wander':
            
            #doesn't display pacman in this mode
            is_displayed =False

            #generates a new random seek location of the monster is close to the old seek
            if calcDistance(seek_x,seek_y,mon_x,mon_y) < 20:
                seek_x = random.randint(50,display_width-50)
                seek_y = random.randint(50, display_height-50)
            
            mon_vel_x, mon_vel_y = seek(seek_x, seek_y, mon_x, mon_y, mon_vel)


            mon_x = mon_x + mon_vel_x
            mon_y = mon_y + mon_vel_y
            
        elif args.monsterBehavior == 'path':
            
            is_displayed = False
            if point_counter < len(point_list):
                mon_vel_x, mon_vel_y = seek(point_list[point_counter][0], point_list[point_counter][1], mon_x, mon_y, mon_vel)
                point_counter+=1
            else:
                mon_vel_x = 0
                mon_vel_y = 0
            mon_x = mon_x + mon_vel_x
            mon_y = mon_y + mon_vel_y

        
        elif args.monsterBehavior == 'v_match':
            #if ghost_lead.y < display_height:
            ghost_lead.move(90,False)
            dynamic_seek(ghost_following, ghost_lead)
            #print ("in main. ghost x: "+str(ghost_lead.x)+" "+str(ghost_lead.y))
        
        elif args.monsterBehavior == 'obstacles':
            #no pacman needed in this mode
            is_displayed =False

            if len(obstacles) > 0:
                for obstacle in obstacles:
                    if calcDistance(ghost_chase.x, ghost_chase.y, obstacle.x, obstacle.y) < 30:
                        #reducing velocity of the ghost when it gets close to a obstacle
                        ghost_chase.vel = 1

                        if ghost_target.x > obstacle.x:
                            
                            if ghost_target.y <=  obstacle.y:
                                dynamic_seek(ghost_chase ,Ghost(ghost_chase.x, obstacle.y - 50, 0, 0), False, True)

                            else:
                                dynamic_seek(ghost_chase ,Ghost(ghost_chase.x, obstacle.y + 50, 0, 0), False, True)
                    else:
                        dynamic_seek(ghost_chase, ghost_target, False, True)
            else:
                dynamic_seek(ghost_chase, ghost_target, False, True)


        elif args.monsterBehavior == 'pursue':
            ghost_target.move(0)
            # making a dummy ghost which is at a future position of the target ghost
            dynamic_seek(ghost_chase, Ghost(ghost_target.x+(5*ghost_target.vel), ghost_target.y, ghost_target.vel, ghost_target.max_vel), False)

        else:

            if (mon_x + mon_vel_x) > display_width or (mon_x + mon_vel_x) < 0:
                mon_vel_x = mon_vel_x * -1

            if (mon_y + mon_vel_y) > display_height or (mon_y + mon_vel_y) < 0:
                mon_vel_y = mon_vel_y * -1

            mon_x = mon_x + mon_vel_x
            mon_y = mon_y + mon_vel_y

        ## displaying objects on the game window

        
        ## --------------------- RENDERING ON GAME DISPLAY ------------------------------

        gameDisplay.fill(white)
        
        if args.monsterBehavior == 'v_match':
            ghost_lead.render(True)
            ghost_following.render(True)
        
        elif args.monsterBehavior == 'obstacles':
            for obstacle in obstacles:
                obstacle.render()
            ghost_target.render(True)
            ghost_chase.render(True)
        
        elif args.monsterBehavior == 'pursue':
            ghost_target.render(True)
            ghost_chase.render(True)
        else:
            pacman(x,y,rot_angle, is_displayed)
            monster(mon_x,mon_y,is_eaten)
            if args.monsterBehavior == 'path':
                pygame.draw.line(gameDisplay,(0,0,255),(50,50),(200,200), 2)
                pygame.draw.line(gameDisplay,(0,0,255),(250,200),(250,700), 2)
                pygame.draw.line(gameDisplay,(0,0,255),(500,700),(350,200), 2)
                pygame.draw.line(gameDisplay,(0,0,255),(350,200),(600,200), 2)

        '''
        # printing theta vals
        text1= "theta is :"
        text_theta = text1 + str(math.degrees(theta))
        printMsg(text_theta,400,30)
        '''
        '''
        #printing the distance at that tick
        text2= "Distance between monster and pacman :"
        text_dist = text2 + str(calcDistance(x,y,mon_x,mon_y))
        printMsg(text_dist,400,10)
        '''
        pygame.display.update()
        
        clock.tick(60)



    pygame.quit()
    quit()

