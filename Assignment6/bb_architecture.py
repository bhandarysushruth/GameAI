from pacman_assn6 import *
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
blue = (25,25,255)
green = (25,255,25)

ball = pygame.image.load("boid.png")
ball = pygame.transform.scale(ball, (20, 20))
ballrect = ball.get_rect()

class Enemy:
    def __init__(self,x,y,health,color=black):
        self.x = x
        self.y = y
        self.health = health
        self.is_dead = False
        self.color = color

    def render(self):
        if not self.is_dead:
            pygame.draw.circle(gameDisplay, self.color,(self.x, self.y), 12)
        else:
        	pygame.draw.circle(gameDisplay, self.color,(self.x, self.y), 12, 1)


class Player:
    def __init__(self,x,y,velocity,max_vel,ammo):
        self.x = x
        self.y = y
        self.vel = velocity
        self.max_vel = max_vel
        self.visible = True
        self.ammo = ammo

    def render(self):
        if self.visible == True:
        	boidRect = pygame.Rect(ballrect)
        	boidRect.x = self.x
        	boidRect.y = self.y
        	gameDisplay.blit(ball, boidRect)

class Ammo_stock:
    def __init__(self,x,y,ammo):
        self.x = x
        self.y = y
        self.ammo = ammo
        self.is_finished = False
        

    def render(self):
        if not self.is_finished:
            pygame.draw.circle(gameDisplay, black,(self.x, self.y), 20)
        else:
        	pygame.draw.circle(gameDisplay, black,(self.x, self.y), 20, 1)


class Blackborad:

	def __init__(self,platform):
		#possible modes : "attack", "restock", "flee", "idle"
		self.mode = "idle"
		self.seeking_object = None
		self.platform = platform

		#to manage access to the the class object
		self.executing = False

	
	def strategyExpert(self):
		min_dist_enemy = 20000
		min_distancce_stockpile = 20000
		chosen_obj = None
		
		#checking is attack is possible:
		for enemy in self.platform.enemies_alive:
			
			if enemy.is_dead:
				continue
			
			dist = calcObjDistance(self.platform.player, enemy)

			if dist < min_dist_enemy:
				if self.platform.player.ammo >= enemy.health:
					chosen_obj = enemy
					min_dist_enemy = dist

		if chosen_obj is not None:
			#this means an object for attack was found
			self.mode = "attack"
			self.seeking_object = chosen_obj
			self.executing = True
		else:
			#This means no attacking object found
			#now we check if restocking ammo is an option and selects the closest one if any

			for stockpile in self.platform.ammo_stockpiles:
				
				if stockpile.is_finished:
					continue
				
				dist = calcObjDistance(self.platform.player, stockpile)
				if dist < min_distancce_stockpile:
					chosen_obj = stockpile

			if chosen_obj is not None:
				#means that a restock location found
				self.mode = "restock"
				self.seeking_object = chosen_obj
				self.executing = True

			else:
				#means that restocking is also not an option
				#so now we return to the safe zone
				self.mode = "flee"
				self.seeking_object = self.platform.safeZone
				self.executing = True


	#attacks the enemy and makes all the required changes
	def attackingExpert(self):
		self.platform.player.ammo -= self.seeking_object.health
		self.seeking_object.health = 0
		self.seeking_object.is_dead = True
		self.mode = "idle"
		self.executing = False

	#restocks ammo fromt he stockpile and makes the required changes
	def restockingExpert(self):

		if self.seeking_object.ammo <= 5:
			self.platform.player.ammo += self.seeking_object.ammo
			self.seeking_object.ammo = 0
			self.seeking_object.is_finished = True
		else:
			self.platform.player.ammo += 5
			self.seeking_object.ammo -= 5

		self.mode = "idle"
		self.executing = False



	def update(self):
		if not self.executing:
			#the player is not doing anything so now you decide a new strategy
			self.strategyExpert()
		else:
			#this means that the player is doing something
			#so now we check what mode it is in and what object it is targeting and move the player towards the target
			#once it is close enough to the target, we check the mode to see what it is supposed to do once it gets there and then we call the approprate function

			vx,vy = seek(self.seeking_object.x, self.seeking_object.y,self.platform.player.x, self.platform.player.y, self.platform.player.vel)
			self.platform.player.x += vx
			self.platform.player.y += vy

			if calcObjDistance(self.platform.player, self.seeking_object) < 22:
				# player has reached the target
				# now we perform the required action

				if self.mode == "attack":
					self.attackingExpert()

				elif self.mode == "restock":
					self.restockingExpert()

				elif self.mode == "flee":
					pass







class GamePlatform:

	def __init__(self, player, enemies_alive, ammo_stockpiles):
		self.player = player
		self.ammo_stockpiles = ammo_stockpiles
		self.enemies_alive = enemies_alive

		#creating a dummy enemy object which acts as th seek object for the safe zone
		self.safeZone = Enemy(700,700,5)



if __name__ == '__main__':

	enemies_alive=[]
	enemies_alive.append(Enemy(50,50,5,red))
	enemies_alive.append(Enemy(50,500,5,blue))
	enemies_alive.append(Enemy(500,50,7,green))

	ammo_stockpiles = []
	ammo_stockpiles.append(Ammo_stock(400,400,10))

	player = Player(700,700,5,5,10)

	platform = GamePlatform(player,enemies_alive,ammo_stockpiles)
	bb = Blackborad(platform)

	exit=False

	while not exit:

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				exit = True

		#building the game display and the safe zone;

		gameDisplay.fill(white)
		pygame.draw.line(gameDisplay, black, [650, 650], [display_width,650])
		pygame.draw.line(gameDisplay, black, [650, 650], [650,display_height])
		printMsg("SAFE ZONE",660,660)

		bb.update()

		for enemy in platform.enemies_alive:
			
			info_str = "Health : " + str(enemy.health)
			printMsg(info_str,enemy.x - 35, enemy.y + 20)
			enemy.render()

		
		for stockpile in platform.ammo_stockpiles:
			info_str = "Ammo in Stockpile : " + str(stockpile.ammo)
			printMsg(info_str, stockpile.x - 45, stockpile.y - 35)
			stockpile.render()

		player_info = "Ammo : "+ str(platform.player.ammo)
		printMsg(player_info, platform.player.x -20, platform.player.y + 20)
		printMsg("Mode : "+bb.mode, platform.player.x -20, platform.player.y + 34)
		platform.player.render()

		pygame.display.update()
		clock.tick(60)

	pygame.quit()
	quit()















