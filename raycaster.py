import sys
from math import *
import pygame
from pygame.locals import *

class Vector2:
	def __init__(self,x,y):
		self.x = x
		self.y = y
	def __str__(self):
		return 'Vector2({},{})'.format(self.x,self.y)
 
PI = pi
COLS = 8
ROWS = 8
C_SIZE = 60 #cell size
P_SIZE = 10 #player size
board = [
[1,1,1,1,1,1,1,1],
[1,0,0,0,0,0,0,1],
[1,1,1,0,1,1,0,1],
[1,1,0,0,0,1,0,1],
[1,1,0,0,0,1,0,1],
[1,0,0,0,0,1,0,1],
[1,1,0,1,0,0,0,1],
[1,1,1,1,1,1,1,1],
]

player = Vector2(100,100)
ang = 0 #player rotation
width, height = 960, 480
CYAN = (0,230,255)
PINK = (255,0,255)


def show_board():
	for y in range(ROWS):
		for x in range(COLS):
			if board[y][x]:
				r = pygame.Rect(x*C_SIZE+1, y*C_SIZE+1, C_SIZE-2, C_SIZE-2) 
				pygame.draw.rect(screen,(255,255,255),r)

def show_player(pla):
	r = pygame.Rect(pla.x, pla.y, P_SIZE, P_SIZE)
	pygame.draw.rect(screen, CYAN, r)
	radius = 18
	end_point = (pla.x + cos(ang)*radius+P_SIZE/2, pla.y + sin(ang)*radius+P_SIZE/2)
	pygame.draw.line(screen, CYAN, (pla.x+P_SIZE/2, pla.y+P_SIZE/2), end_point, 5)

def calc_dist(a,b):
	return (a[0]-b[0])**2 + (a[1]-b[1])**2

def show_ray(pla, a):
	while a > 2*pi:
		a-=2*pi
	while a < 0:
		a+=2*pi

	#finding closest x obstacle hitpoint
	#cs is current x
	cx = floor(pla.x//60) #starting to the left
	dx = -1 #dx is order of checking ray to the left -1 or to the right 1
	if a < pi/2 or a > 1.5*pi:
		cx +=1	#starting to the right
		dx = 1
	tg = tan(a)
	hity = tg*(cx*60-pla.x) + pla.y #y = ax + b
	hity_i = floor(hity//60) 
	while cx > -1 and cx < COLS and hity_i > -1 and hity_i < ROWS:
		tmp_fix = 0	#fixes checking wrong tile when looking backwards
		if dx == -1:
			tmp_fix = 1
		if board[hity_i][cx-tmp_fix]:
			break
		cx+=dx
		hity = tg*(cx*60-pla.x) + pla.y #y = ax + b
		hity_i = floor(hity//60) 
	xres = (cx * C_SIZE, hity)
	
	#+=0.05
	#finding closes y obstacle hitpoint
	cy = floor(pla.y//60) #starting up
	dy = -1 #dx is order of checking ray to the left -1 or to the right 1
	if a <= pi:
		cy +=1	#starting down
		dy = 1
	inv_tg = 1/(tan(a)+0.00001)
	hitx = (cy*60 - pla.y)*inv_tg + pla.x #x = (y-b)/a
	hitx_i = floor(hitx//60) 
	while cy > -1 and cy < ROWS and hitx_i > -1 and hitx_i < COLS:
		tmp_fix = 0	#fixes checking wrong tile when looking backwards
		if dy == -1:
			tmp_fix = 1
		if board[cy-tmp_fix][hitx_i]:
			break
		cy+=dy
		hitx = (cy*60 - pla.y)*inv_tg + pla.x#x = (y-b)/a
		hitx_i = floor(hitx//60) 
	yres = (hitx, cy*60)

	if calc_dist((pla.x,pla.y), xres) < calc_dist((pla.x,pla.y), yres):
		hit = xres
		col_mult = 0.5
	else:
		hit = yres
		col_mult = 1
	# pygame.draw.line(screen, (255,0,0), (pla.x+P_SIZE/2, pla.y+P_SIZE/2), xres, 1)
	# pygame.draw.line(screen, (0,0,255), (pla.x+P_SIZE/2, pla.y+P_SIZE/2), yres, 1)
	pygame.draw.line(screen, (0,255,0), (pla.x+P_SIZE/2, pla.y+P_SIZE/2), hit, 1)
	return (calc_dist(hit, (pla.x,pla.y)),col_mult)

screen = pygame.display.set_mode((width, height))
pygame.display.init()  
fps = 20
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
			ang-=0.08
		elif keys[pygame.K_d]:
			ang+=0.08
		if ang > 2*PI:
			ang -= 2*PI

		if keys[pygame.K_w]:
			new_x = (player.x+vel*cos(ang))
			new_y = (player.y+vel*sin(ang))
			if not board[floor(new_y//60)][floor(new_x//60)]:
				player = Vector2(new_x, new_y)
		elif keys[pygame.K_s]:
			new_x = (player.x-vel*cos(ang))
			new_y = (player.y-vel*sin(ang))
			if not board[floor((new_y)//60)][floor(new_x//60)]:
				player = Vector2(new_x, new_y)


	show_board()
	show_player(player)
	pygame.draw.rect(screen, (0,60,112), pygame.Rect(width*0.5, 0, width*0.5, height*0.5))
	pygame.draw.rect(screen, (40,40,40), pygame.Rect(width*0.5, height*0.5, width*0.5, height*0.5))
	ray_count = 60
	x_step = width*0.5/ray_count
	for i in range(0, ray_count):
		ray_angle = ang+(i-ray_count//2)*pi/2/ray_count
		dist, col_mult = show_ray(player, ray_angle)
		dist = (60*320)/(sqrt(dist)*cos(ang-ray_angle))
		hh = floor(dist/3) #half height
		r = pygame.Rect(width/2+x_step*i,height/2-hh,x_step, hh*2)
		pygame.draw.rect(screen, (col_mult*200,col_mult*200,col_mult*200), r)
  # Draw.
	pygame.display.flip()
	fpsClock.tick(fps)

print("closed")
pygame.quit()
