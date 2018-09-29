import pygame
import math
import numpy as np
import argparse
import random
import sys

pygame.init()

display_width = 800
display_height = 800

maxVelocity = 5
numBoids = 20
boids = []

screen = pygame.display.set_mode((display_width, display_height))

ball = pygame.image.load("boid.png")
ball = pygame.transform.scale(ball, (15, 15))
ballrect = ball.get_rect()

class Boid:
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocityX = random.randint(1, 10) / 10.0
        self.velocityY = random.randint(1, 10) / 10.0

    
    ## returns the distance between two boids

    def calc_distance(self, boid):
        dist = math.sqrt(((self.x - boid.x)**2) + ((self.y - boid.y)**2))        
        return dist


    ## gathers the flock together and brings the boid closer if theys start scattering

    def gather(self, boids):
        if len(boids) == 0: 
        	return
        
        # calculating the average separation from other boids

        avgX = 0
        avgY = 0

        for boid in boids:
            
            # not considering itself

            if boid.x == self.x and boid.y == self.y:
                continue
                
            avgX += (self.x - boid.x)
            avgY += (self.y - boid.y)

        avgX /= len(boids)
        avgY /= len(boids)
       
        self.velocityX -= (avgX / 100) 
        self.velocityY -= (avgY / 100) 
        

    # gets the average velocity of the other boids and matches that velocity and general direction

    def moveWith(self, boids):
        if len(boids) == 0: 
        	return
        
        
        avg_vel_x = 0
        avg_vel_y = 0
                
        for boid in boids:
            avg_vel_x += boid.velocityX
            avg_vel_y += boid.velocityY

        avg_vel_x /= len(boids)
        avg_vel_y /= len(boids)

        # set our velocity towards the others
        self.velocityX += (avg_vel_x)/10
        self.velocityY += (avg_vel_y)/10
    
    
    # scatters the boid away from another boid if it gets closer than minimum distance
    def separate(self, boids, min_separation):
        if len(boids) == 0: 
        	return
        
        distanceX = 0
        distanceY = 0
        
        # number of boids within the radius of separation

        numClose = 0

        for boid in boids:
            
            distance = self.calc_distance(boid)
            
            if  distance < min_separation:
                numClose += 1
                xdiff = (self.x - boid.x) 
                ydiff = (self.y - boid.y) 
                
                if xdiff >= 0: 
                	xdiff = math.sqrt(min_separation) - xdiff
                elif xdiff < 0: 
                	xdiff = -math.sqrt(min_separation) - xdiff
                
                if ydiff >= 0: 
                	ydiff = math.sqrt(min_separation) - ydiff
                elif ydiff < 0: 
                	ydiff = -math.sqrt(min_separation) - ydiff

                distanceX += xdiff 
                distanceY += ydiff 
        
        ## maintains velocity is none of the boids are in the separation radius 
        if numClose == 0:
            return
            
        self.velocityX -= distanceX / 5
        self.velocityY -= distanceY / 5
        
    # changes the cordinates as per the velocity changes from the previous functions

    def move(self):
        
        if abs(self.velocityX) > maxVelocity or abs(self.velocityY) > maxVelocity:
            scaleFactor = maxVelocity / max(abs(self.velocityX), abs(self.velocityY))
            self.velocityX *= scaleFactor
            self.velocityY *= scaleFactor
        
        self.x += self.velocityX
        self.y += self.velocityY

    def render(self):
    	boidRect = pygame.Rect(ballrect)
    	boidRect.x = self.x
    	boidRect.y = self.y
    	screen.blit(ball, boidRect)



if __name__ == '__main__':

	# initializing boids at random positions
	
	for i in range(numBoids):
	    boids.append(Boid(random.randint(0, display_width), random.randint(0, display_height)))   

	while True:
	    
	    for event in pygame.event.get():
	        if event.type == pygame.QUIT: 
	        	sys.exit()

	        if event.type == pygame.KEYDOWN:
	        	if event.key == pygame.K_q:
	                    sys.exit()

	    for boid in boids:
	        closeBoids = []
	        for otherBoid in boids:
	            if otherBoid == boid: 
	            	continue
	            distance = boid.calc_distance(otherBoid)
	            if distance < 200:
	                closeBoids.append(otherBoid)

	        
	        boid.gather(closeBoids)
	        boid.moveWith(closeBoids)  
	        boid.separate(closeBoids, 20)  

	        # padding for rebounce off walls
	        padding = 25
	        
	        #velocities changed randomly after bouncing off walls 

	        if boid.x < padding and boid.velocityX < 0:
	            boid.velocityX = -boid.velocityX * random.random()
	        if boid.x > display_width - padding and boid.velocityX > 0:
	            boid.velocityX = -boid.velocityX * random.random()
	        if boid.y < padding and boid.velocityY < 0:
	            boid.velocityY = -boid.velocityY * random.random()
	        if boid.y > display_height - padding and boid.velocityY > 0:
	            boid.velocityY = -boid.velocityY * random.random()
	            
	        boid.move()
	        
	    screen.fill((255,255,255))
	    for boid in boids:
	    	boid.render()
	        
	    pygame.display.flip()
	    pygame.time.delay(10)
