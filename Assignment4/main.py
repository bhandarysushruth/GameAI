import pygame
import math
import numpy as np
import argparse
import random
from Movement_Strategy import MoveDown
from Movement_Strategy import MoveRight

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

moveDown = MoveDown()
moveRight = MoveRight()

class Ghost:
    def __init__(self,x,y,velocity,max_vel, movement_strategy=None):
        self.x = x
        self.y = y
        self.x_vel = 0
        self.y_vel = 0
        self.vel = velocity
        self.max_vel = max_vel
        self.move_strategy = movement_strategy


    def move(self):
    	self.move_strategy.move(self)


    '''
    def move(self,angle,wrap=False):
        
        if (wrap == False) and ((self.x > display_width - 20) or(self.y >display_height -40)):
            self.vel = 0

        self.x += self.vel * math.cos(math.radians(angle))
        self.y += self.vel * math.sin(math.radians(angle))
        
        if wrap == True:
            self.x %= display_width
            self.y %= display_height

	'''

    def render(self, visible):
        if visible == True:
            gameDisplay.blit(monst, (self.x,self.y))



class VerticalGhost(Ghost):
	def __init__(self, x, y, velocity,max_vel):
		super(VerticalGhost,self).__init__(x, y, velocity,max_vel,moveDown)

class HorizontalGhost(Ghost):
	def __init__(self, x, y, velocity,max_vel):
		super(HorizontalGhost,self).__init__(x, y, velocity,max_vel,moveRight)


if __name__ == '__main__':

	## Ghost object which moves down
	downGhost = VerticalGhost(100, 10, 3, 10)


	## Ghost object which moves right
	rightGhost = HorizontalGhost(100,10,3, 10)

	exit = False

	while not exit:

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				exit = True

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_q:
					exit =True

		downGhost.move()
		rightGhost.move()
		gameDisplay.fill(white)
		downGhost.render(True)
		rightGhost.render(True)
		pygame.display.update()
		clock.tick(60)

	pygame.quit()
	quit()

