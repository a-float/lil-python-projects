import pygame, sys

KEYS1 = [119,100,115,97,32] 
multi = False
WIDTH = 8
HEIGHT = 8
T_WIDTH = 50
SPEED = 5
T_HEIGHT = 50
bombs = []
MOVEPLAYER_EVENT = pygame.USEREVENT+1
BOMB_TICK_EVENT = pygame.USEREVENT+2
MOVE_TIME = 50
board = [[0,0,0,0,2,2,1,0],
		 [0,2,2,1,2,2,1,0],
		 [0,2,2,1,2,2,1,0],
		 [0,2,2,1,2,2,1,0],
		 [0,2,2,1,2,2,1,0],
		 [0,2,2,1,2,2,1,0],
		 [0,2,2,1,2,2,1,0],
		 [0,2,2,1,2,2,1,0]
]
def showBoard():
	for i in range(HEIGHT):
		for j in range(WIDTH):
			k = board[i][j]
			if(k == 1):
				pygame.draw.rect(win, (50,50,50), (j*T_WIDTH+5, i*T_HEIGHT+5,40,40))
			elif(k==2):
				pygame.draw.rect(win, (120,120,120), (j*T_WIDTH+5, i*T_HEIGHT+5,40,40))
class Bomb:
	def __init__(self,x,y,p,t,r):
		self.x = x//T_WIDTH
		self.y =  y//T_HEIGHT
		self.owner = p
		self.time = t
		self.range = r
		self.detonated = False
		self.done = False
	
	def show(self):
		pygame.draw.rect(win, (255,0,0), (self.x*T_WIDTH+17, self.y*T_HEIGHT+17, 16,16))
	
	def tick(self):
		self.time -= 1
		if(self.time == 0):
			if(not self.detonated):
				self.detonate()
			else:
				board[self.y][self.x] = 0
				self.done = True

	def detonate(self):
		self.detonated = True
		self.owner.bomb_count += 1
		self.time = 1
		i = 1
		while(i <= self.range and self.x-i >= 0):
			if(board[self.y][self.x-i]==2):
				board[self.y][self.x-i] = 0
			else:
				i+=1
		i = 1
		while(i <= self.range and self.y-i >= 0):
			if(board[self.y-i][self.x]==2):
				board[self.y-i][self.x] = 0
			else:
				i+=1
		i = 1
		while(i <= self.range and self.y+i < HEIGHT):
			if(board[self.y+i][self.x]==2):
				board[self.y+i][self.x] = 0
			else:
				i+=1
		i = 1
		while(i <= self.range and self.x+i < WIDTH):
			if(board[self.y][self.x+i]==2):
				board[self.y][self.x+i] = 0
			else:
				i+=1

class Player:
	def __init__(self,x,y):
		self.keys = KEYS1
		self.bomb_count = 10
		self.color = (0,0,255)
		self.x = x
		self.y = y
		self.bomb_range = 1
		self.movebools = [0,0,0,0]
		self.canwalk = False
	
	def control(self, key, etype):
		#print(key,etype)
		p = self.keys.index(key)
		if(p == 4 and self.bomb_count > 0):
			self.bomb_count -= 1
			board[self.y//T_HEIGHT][self.x//T_WIDTH] = -1
			self.canwalk = True
			bombs.append(Bomb(self.x, self.y, self, 3, self.bomb_range))
		if(etype == 2 and p!=4):
			if(self.movebools[(p+2)%4] == 0):
				self.movebools[p] = 1
			else:
				self.movebools[p] = 2
		elif(etype == 3 and p != 4):
			self.movebools[p] = 0
			if(self.movebools[(p+2)%4] == 2):
				self.movebools[(p+2)%4] = 1

	def move(self):
		#print(self.canwalk)
		a, b = self.x, self.y
		if(sum(self.movebools) > 0):
			if(self.movebools[0] and self.y > 0 and ((board[((self.y-SPEED)//T_HEIGHT)%HEIGHT][self.x//T_WIDTH] == 0 or (board[((self.y-SPEED)//T_HEIGHT)%HEIGHT][self.x//T_WIDTH] == -1) and self.canwalk))):
				self.y -= SPEED
			if(self.movebools[2] and self.y+30 < HEIGHT*T_HEIGHT and ((board[((self.y+30+SPEED)//T_HEIGHT)%HEIGHT][self.x//T_WIDTH] == 0) or (board[((self.y+30+SPEED)//T_HEIGHT)%HEIGHT][self.x//T_WIDTH] == -1 and self.canwalk))):
				self.y += SPEED
			if(self.movebools[1] and self.x+30 < WIDTH*T_WIDTH and (board[((self.y+30)//T_HEIGHT)%HEIGHT][(self.x+30+SPEED)//T_WIDTH] == 0 or (board[((self.y+30)//T_HEIGHT)%HEIGHT][(self.x+30+SPEED)//T_WIDTH] == -1 and self.canwalk))):
				self.x += SPEED
			if(self.movebools[3] and self.x > 0 and (board[((self.y+30)//T_HEIGHT)%HEIGHT][(self.x-SPEED)//T_WIDTH] == 0 or (board[((self.y+30)//T_HEIGHT)%HEIGHT][(self.x-SPEED)//T_WIDTH] == -1 and self.canwalk))):
				self.x -= SPEED
		a,b = a//T_WIDTH, b//T_HEIGHT
		#print(board[b][a])
		if((a != self.x//T_WIDTH) or (b != self.y//T_HEIGHT)):
			self.canwalk = False
	def show(self):
		pygame.draw.rect(win, self.color, (self.x, self.y, 30, 30))

p1 = Player(0,0)
running = True
pygame.init()
clock = pygame.time.Clock()
pygame.time.set_timer(MOVEPLAYER_EVENT, MOVE_TIME)
pygame.time.set_timer(BOMB_TICK_EVENT, 1000)
win = pygame.display.set_mode((WIDTH*T_WIDTH, HEIGHT*T_HEIGHT))
pygame.display.set_caption('Bomberman')
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		elif event.type in [2,3] :
			e = event.key
			if(e in KEYS1):
				p1.control(e,event.type)
			elif(multi and e in KEYS2):
				p2.constrol(e,event.type)
		elif event.type == MOVEPLAYER_EVENT:
			p1.move()
		elif event.type == BOMB_TICK_EVENT:
			for b in bombs:
				b.tick()
				if(b.done == True):
					bombs.remove(b)

	win.fill((0,0,0))
	showBoard()
	for b in (bombs):
		b.show()
	p1.show()		
	pygame.display.update()
pygame.quit()
sys.exit()