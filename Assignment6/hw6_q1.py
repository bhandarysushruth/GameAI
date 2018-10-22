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
cat = pygame.image.load('cat.png')
cat = pygame.transform.scale(cat, (100, 100))
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

		ret_msg = self.curState.Execute()
		return ret_msg

## ==================================================================

class Cat(object):
	def __init__(self):
		self.FSM = SimpleFSM(self)
		self.sleeping = True



## ======================================================================================
## ======================================================================================


def pacman(x,y,rotation_angle,display_boolean):
    if display_boolean:
        img = pygame.transform.rotate(cat, rotation_angle)
        gameDisplay.blit(cat, (x,y))

def printMsg(text_string,x,y):
    font = pygame.font.SysFont("comicsansms", 22)
    text = font.render(text_string, True, (0, 128, 0))
    gameDisplay.blit(text,(x, y))


if __name__ == '__main__':

	#setting up the objects:
	cat1 = Cat()
	cat1.FSM.states["Sleeping"] = Sleeping()
	cat1.FSM.states["Awake"] = Awake()
	cat1.FSM.transitions["goToSleep"] = Transition("Sleeping")
	cat1.FSM.transitions["wakeUp"] = Transition("Awake")

	cat1.FSM.SetState("Sleeping")

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
		
		for event in pygame.event.get():

			if event.type == pygame.QUIT:
				exit = True

			if event.type == pygame.KEYDOWN:

				if event.key == pygame.K_q:
					exit = True

				if event.key == pygame.K_s:

					sound_on = not sound_on

					if(sound_on):
						cat1.FSM.Transition("wakeUp")
					else:
						cat1.FSM.Transition("goToSleep")

			if event.type == pygame.KEYUP:
				pass


		gameDisplay.fill(white)

		printMsg("Press 's' to start/stop sound", 500,100)

		if(sound_on):
			printMsg("Rat Sound On !!!!", 100,50)

		screen_message = "State : " + cat1.FSM.Execute()
		printMsg(screen_message, 100, 100)
		pacman(x,y,rot_angle, is_displayed)
		pygame.display.update()		
		clock.tick(60)

	pygame.quit()
	quit()

















