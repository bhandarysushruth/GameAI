from pacman import *
import pygame
import math
import numpy as np
import argparse
import random
from random import randint
from time import clock

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
ath = pygame.image.load('athelete.png')
ath = pygame.transform.scale(ath, (80, 80))
counter = 0


## ======================================================================================
## ======================================================================================


State = type("State",(object,),{})

class Sleeping(State):
	def Execute(self):
		ret_message = "Sleeping"
		return ret_message
## ==================================================================

class Awake(State):
	def Execute(self):
		ret_messge = "Awake"
		return ret_messge

## ==================================================================

class Wander(State):
	
	def __init__(self, character):
		self.character = character
		self.name = "wander"

	def state_name(self):
		return "wander"

	def Execute(self):
		
		if (self.character.seeking_object is not None):
			dist = calcObjDistance(self.character, self.character.seeking_object)

		#changing direction if it reaches a temp target
		if (self.character.seeking_object is None) or (dist < 20):
			r_seek_x = random.randint(50,display_width-50)
			r_seek_y = random.randint(50,display_height-50)
			self.character.seeking_object = Ghost(r_seek_x, r_seek_y, 0, 0)

		vx, vy = seek(self.character.seeking_object.x,self.character.seeking_object.y,
							self.character.x, self.character.y, self.character.vel)

		self.character.x += vx
		self.character.y += vy


class Idle(State):
	
	def state_name(self):
		return "idle"

	def Execute(self):
		pass

class Approach(State):

	def __init__(self, character):
		self.character = character

	def state_name(self):
		return "approach"

	def Execute(self):
		vx, vy = seek(self.character.seeking_object.x,self.character.seeking_object.y,
							self.character.x, self.character.y, self.character.vel)

		self.character.x += vx
		self.character.y += vy

class Flee(State):
	def __init__(self, character):
		self.character = character

	def state_name(self):
		return "flee"

	def Execute(self):
		vx, vy = seek(self.character.following_object.x,self.character.following_object.y,
							self.character.x, self.character.y, self.character.vel)

		self.character.x -= vx
		self.character.y -= vy

## ==================================================================

class Transition(object):
	def __init__(self, toState):
		self.toState = toState


	def Execute(self):
		print("Transitioning....")

## ==================================================================

class SimpleFSM(object):
	def __init__(self, char):
		self.char = char
		self.states = {}
		self.transitions = {}
		self.curState = None
		self.trans = None

	def SetState(self, stateName):
		self.curState = self.states[stateName]

	def Transition(self, transName):
		self.trans = self.transitions[transName]

	def Execute(self):
		if(self.trans):
			self.trans.Execute()
			self.SetState(self.trans.toState)
			self.trans = None
			
		self.curState.Execute()

## ==================================================================
'''
class Cat(object):
	def __init__(self):
		self.FSM = SimpleFSM(self)
		self.sleeping = True

'''


class Ghost:
    def __init__(self,x,y,velocity,max_vel,seeking_object = None):
        self.x = x
        self.y = y
        self.x_vel = 0
        self.y_vel = 0
        self.vel = velocity
        self.max_vel = max_vel
        self.FSM = SimpleFSM(self)
        self.seeking_object = seeking_object

    def move(self,angle,wrap=False):
        
        if (wrap == False) and ((self.x > display_width - 20) or(self.y >display_height -40)):
            self.vel = 0

        self.x += self.vel * math.cos(math.radians(angle))
        self.y += self.vel * math.sin(math.radians(angle))
        
        if wrap == True:
            self.x %= display_width
            self.y %= display_height

    def render(self, visible=True):
        if visible == True:
            gameDisplay.blit(monst, (self.x,self.y))


class Athlete:
    def __init__(self,x,y,velocity,max_vel,seeking_object = None):
        self.x = x
        self.y = y
        self.x_vel = 0
        self.y_vel = 0
        self.vel = velocity
        self.max_vel = max_vel
        self.FSM = SimpleFSM(self)
        self.seeking_object = seeking_object
        self.following_object = None

    def move(self,angle,wrap=False):
        
        if (wrap == False) and ((self.x > display_width - 20) or(self.y >display_height -40)):
            self.vel = 0

        self.x += self.vel * math.cos(math.radians(angle))
        self.y += self.vel * math.sin(math.radians(angle))
        
        if wrap == True:
            self.x %= display_width
            self.y %= display_height

    def render(self, visible=True):
        if visible == True:
            gameDisplay.blit(ath, (self.x,self.y))


## =====================================================================================



def printMsg(text_string,x,y):
    font = pygame.font.SysFont("comicsansms", 22)
    text = font.render(text_string, True, (0, 128, 0))
    gameDisplay.blit(text,(x, y))


def calcDistance(x1,y1,x2,y2):
    val = (x2-x1)**2
    val += (y2-y1)**2
    dist = math.sqrt(val)
    return dist

def calcObjDistance(first, second):
    val = (second.x - first.x)**2
    val += (second.y - first.y)**2
    dist = math.sqrt(val)
    return dist

## ============================= MAIN ==========================================================

if __name__ == '__main__':

	#setting up the world variables

	objects_on_screen = []

	#first object
	obj1 = Ghost(100,100,5,5)
	obj1.FSM.states["wander"] = Wander(obj1)
	obj1.FSM.states["idle"] = Idle()
	obj1.FSM.states["approach"] = Approach(obj1)
	obj1.FSM.transitions["startWander"] = Transition("wander")
	obj1.FSM.transitions["goIdle"] = Transition("idle")
	obj1.FSM.transitions["startApproach"] = Transition("approach")
	obj1.FSM.SetState("idle")
	objects_on_screen.append(obj1)


	athlete1 = Athlete(500,500,7,7)
	athlete1.FSM.states["wander"] = Wander(athlete1)
	athlete1.FSM.states["idle"] = Idle()
	athlete1.FSM.states["flee"] = Flee(athlete1)
	athlete1.FSM.transitions["startWander"] = Transition("wander")
	athlete1.FSM.transitions["goIdle"] = Transition("idle")
	athlete1.FSM.transitions["startFleeing"] = Transition("flee")
	athlete1.FSM.SetState("idle")
	objects_on_screen.append(athlete1)


	#variables for 
	sound_on = False
	screen_message = 'DEFAULT'

	exit = False
	x = 100
	y = 300
	is_displayed = True
	rot_angle = 0



	while not exit: 
        
        ## MOVEMENT FOR THE PACMAN
		
		if (calcObjDistance(obj1, athlete1) < 250) and (obj1.FSM.curState.state_name() != "idle"):
			obj1.seeking_object = athlete1
			athlete1.following_object = obj1
			obj1.FSM.Transition("startApproach")

			if(calcObjDistance(obj1, athlete1) < 150) and (athlete1.FSM.curState.state_name() != "idle"):
				athlete1.FSM.Transition("startFleeing")

		for event in pygame.event.get():

			if event.type == pygame.QUIT:
				exit = True

			if event.type == pygame.KEYDOWN:

				if event.key == pygame.K_q:
					exit = True

				if event.key == pygame.K_a:
					
					if(athlete1.FSM.curState.state_name() == "idle"):
						print("here")
						athlete1.FSM.Transition("startWander")
					else:
						athlete1.FSM.Transition("goIdle")

				if event.key == pygame.K_m:
					if(obj1.FSM.curState.state_name() == "idle"):
						print("here")
						obj1.FSM.Transition("startWander")
					else:
						obj1.FSM.Transition("goIdle")


			if event.type == pygame.KEYUP:
				pass


		#for printing ditance on the screen
		dst = calcObjDistance(objects_on_screen[0], objects_on_screen[1])


		gameDisplay.fill(white)

		printMsg("Press 'a' to switch athelete between idle and wander", 400,780)
		printMsg("Press 'm' to switch monster between idle and wander", 400,760)

		for obj in objects_on_screen:

			obj.FSM.Execute()
			obj.render()
		
		printMsg("Distance : "+str(dst), 400, 20)
		pygame.display.update()		
		clock.tick(60)

	pygame.quit()
	quit()

















