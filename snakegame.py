import pygame 
import sys
import time
import random

from pygame.locals import *

w = 800
h = 600

gs = 20
gw = w/gs
gh = h/gs

background_color = (0,0,0)
snake_color = (20,100,150)
feed_color = (150,0,0)
specialfeed_color = (150,0,150)
text_color = (100,100,100)

up = (0,-1)
down = (0,1)
left = (-1,0)
right = (1,0)

fps = 10

class Python(object):
	def __init__(self):
		self.create()
		self.color = snake_color

	def create(self):
		self.length = 2
		self.positions = [((w/2),(h/2))]
		self.direction = random.choice([up,down,left,right])

	def control(self, xy):
		if (xy[0] * -1,xy[1] * -1) == self.direction:
			return
		else:
			self.direction = xy

	def move(self):
		cur = self.positions[0]
		x,y = self.direction
		new = (((cur[0] + (x * gs)) %  w), (cur[1]+(y * gs)) % h)
		if new in self.positions[2:]:
			self.create()
		else:
			self.positions.insert(0,new)
			if len(self.positions) > self.length:
				self.positions.pop()	

	def eat(self):
		self.length += 1

	def specialeat(self):
		self.length += random.randrange(1,4)

	def draw(self,surface):
		for p in self.positions:
			draw_object(surface,self.color,p)

class Feed(object):
	def __init__(self):
		self.position = {0,0}
		self.color = feed_color
		self.create()

	def create(self):
		self.position = (random.randint(0,gw -1) * gs,random.randint(0,gh -1) * gs)

	def draw(self,surface):
		draw_object(surface,self.color,self.position)

class SpecialFeed(object):
	def __init__(self):
		self.position = {0,0}
		self.color = specialfeed_color
		self.create()

	def create(self):
		self.position = (random.randint(0,gw -1) * gs,random.randint(0,gh -1) * gs)

	def draw(self,surface):
		draw_object(surface,self.color,self.position)

def draw_object(surface,color,pos):
	r = pygame.Rect((pos[0],pos[1]), (gs,gs))
	pygame.draw.rect(surface,color,r)

def check_eat(python,feed):
	if python.positions[0] == feed.position:
		python.eat()
		feed.create()

def check_specialeat(python,feed):
	if python.positions[0] == specialfeed.position:
		python.specialeat()
		specialfeed.create()

def show_info(length,speed,surface):
	font = pygame.font.Font(None,34)
	text = font.render("Length : " + str(length) + "      Speed: " + str(round(speed,2)),1,text_color)
	pos = text.get_rect()
	pos.centerx = 150
	surface.blit(text,pos)

if __name__ == '__main__':
	python = Python()
	feed = Feed()
	specialfeed = SpecialFeed()

	pygame.init()
	window = pygame.display.set_mode((w,h),0,32)
	pygame.display.set_caption('Pyton game')
	surface = pygame.Surface(window.get_size())
	surface = surface.convert()
	surface.fill(background_color)
	clock = pygame.time.Clock()
	pygame.key.set_repeat(1,40)
	window.blit(surface,(0,0))

	while True:

		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
			elif event.type == KEYDOWN:
				if event.key == K_UP:
					python.control(up)
				elif event.key == K_DOWN:
					python.control(down)
				elif event.key == K_LEFT:
					python.control(left)
				elif event.key == K_RIGHT:
					python.control(right)

		surface.fill(background_color)
		python.move()
		check_eat(python, feed)
		check_specialeat(python,feed)
		speed = (fps + python.length) / 2
		show_info(python.length,speed,surface)
		python.draw(surface)
		feed.draw(surface)
		specialfeed.draw(surface)
		window.blit(surface,(0,0))
		pygame.display.flip()
		pygame.display.update()
		clock.tick(speed)
	