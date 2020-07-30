import sys
 
import pygame
from pygame.locals import *

class Vector2:
	def __init__(self,x,y):
		self.x = x
		self.y = y
	def __str__(self):
		return 'Vector2({},{})'.format(self.x,self.y)
 
COLS = 8
ROWS = 8
C_SIZE = 60
board = [
[1,1,1,1,1,1,1,1],
[1,0,0,0,0,0,0,1],
[1,1,1,0,1,1,0,1],
[1,0,0,0,0,1,0,1],
[1,0,0,0,0,1,0,1],
[1,0,0,0,0,1,0,1],
[1,0,0,0,0,0,0,1],
[1,1,1,1,1,1,1,1],
]

player = Vector2(100,100)
width, height = 960, 480


def show_board():
	for y in range(ROWS):
		for x in range(COLS):
			if board[y][x]:
				r = pygame.Rect(x*C_SIZE+1, y*C_SIZE+1, C_SIZE-2, C_SIZE-2) 
				pygame.draw.rect(screen,(255,255,255),r)

def show_player(vec):
	r = pygame.Rect(vec.x, vec.y, 10, 10)
	pygame.draw.rect(screen,(200,0,255),r)

screen = pygame.display.set_mode((width, height))
pygame.display.init()  
fps = 60
fpsClock = pygame.time.Clock() 
# Game loop.
running = True
while running:
	screen.fill((0, 0, 0))
	for event in pygame.event.get():
		# print(event.type, pygame.QUIT)
		if event.type == pygame.QUIT:
			running = False
		keys = pygame.key.get_pressed()
		vel = 5
		if keys[pygame.K_a]:
			player.x -= vel

		elif keys[pygame.K_d]:
			player.x += vel

		if keys[pygame.K_w]:
			player.y -= vel

		elif keys[pygame.K_s]:
			player.y += vel

	show_board()
	show_player(player)
  # Draw.
	pygame.display.flip()
	fpsClock.tick(fps)

print("closed")
# pygame.quit()
print("closed2")
