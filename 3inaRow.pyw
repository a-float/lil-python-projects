import pygame,sys,random

def texts(score):
   font=pygame.font.Font(None,45)
   scoretext=font.render("Score:", 1,(255,255,255),BG_COLOR)
   win.blit(scoretext, (1.07*COLS * T_WIDTH - 20 , 20))
   scoretext=font.render(str(score), 1,(255,255,255),BG_COLOR)
   win.blit(scoretext, (1.11*COLS * T_WIDTH -30 , 60))

def check_if_bordering(pos,sel):
	if(pos == sel):
		return [-1,-1], True
	if(pos == [sel[0],sel[1]+1] or pos == [sel[0],sel[1]-1] or pos == [sel[0]+1,sel[1]] or pos == [sel[0]-1,sel[1]]):
		tiles[pos[1]][pos[0]][0], tiles[sel[1]][sel[0]][0] = tiles[sel[1]][sel[0]][0], tiles[pos[1]][pos[0]][0]
		return [-1,-1], True
	return sel, False

def update_board():
	destroy_list = {}
	for c in range(COLS-1,-1,-1):
		curr_color = tiles[c][0][0]
		series = 1
		for r in range(1,ROWS):
			if(tiles[c][r][0] == curr_color):
				series += 1
			else:
				if(series >= 3):
					destroy_list.update({(c,p) : True for p in range(r-series,r)})
				curr_color = tiles[c][r][0]
				series = 1
		if(series >= 3):
			destroy_list.update({(c,p) : True for p in range(ROWS-series,ROWS)})
	
	for r in range(ROWS):
		curr_color = tiles[0][r][0]	
		series = 1
		for c in range(1,COLS):
			if(tiles[c][r][0] == curr_color):
				series += 1
			else:
				if(series >= 3):
					destroy_list.update({(p,r) : True for p in range(c-series, c)})
				curr_color = tiles[c][r][0]
				series = 1
		if(series >= 3):
			destroy_list.update({(p,r) : True for p in range(COLS-series, COLS)})
	if(start_scoring):
		global score
		score += len(destroy_list)**2 * 100
	for d in destroy_list:
		for i in range(d[0],-1,-1):
			if(i== d[0]):
				tiles[i][d[1]][3] = tiles[i-1][d[1]][3]
			if(i>0):
				tiles[i][d[1]][0] = tiles[i-1][d[1]][0]
			else:
				tiles[0][d[1]][0] = random.choice([a for a in COLORS.keys()])
			tiles[i][d[1]][3] += 1
			moving.update({(i,d[1]) : tiles[0][d[1]][3]})

def update_animations():
	to_delete = []
	#print(moving)
	for m in moving:
		tiles[m[0]][m[1]][3] -= falling_speed
		if(tiles[m[0]][m[1]][3] <= 0):
			tiles[m[0]][m[1]][3] = 0
			to_delete.append((m[0],m[1]))
	for i in to_delete:
		del moving[i]

MOVETILES = pygame.USEREVENT + 1
pygame.time.set_timer(MOVETILES, 25)
falling_speed = 0.15
COLORS = {
	'RED'    : (255, 10, 5),
	'BLUE'   : (0, 70, 255),
	'GREEN'  : (10, 255, 45),
	'ORANGE' : (255, 120, 17),
	'PURPLE' : (158, 6, 208),
	'YELLOW' : (255, 198, 40),
	'PINK'	 : (255, 102, 204),
	'CYAN'   : (14, 235, 230)
	}
ROWS = 8
COLS = 8
BG_COLOR = (0, 51, 102)
T_WIDTH = 65
T_HEIGHT = 65
start_scoring = False
score = 0
RIGHT_BANNER = 150
t_selected = [-1,-1]
no_select = True
moving = {}

tiles = [[[random.choice([a for a in COLORS.keys()]),r*T_WIDTH, c*T_HEIGHT,0] for r in range(ROWS)] for c in range(COLS)]

running = True
pygame.init()

win = pygame.display.set_mode((ROWS*T_WIDTH + RIGHT_BANNER,COLS*T_HEIGHT))
pygame.display.set_caption('Python Game')
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		elif event.type == 4:
			pos = pygame.mouse.get_pos()
			t_pos = [pos[0]//T_WIDTH, pos[1]//T_HEIGHT]		

		elif event.type == 5 and event.button == 1:
			start_scoring = True
			if(no_select):
				t_selected = t_pos
				no_select = False
			else:
				t_selected, no_select = check_if_bordering(t_pos,t_selected)
				update_board()

		elif event.type == MOVETILES:
			update_animations()
			if(len(moving) == 0):
				update_board()

	win.fill(BG_COLOR)
	for c in range(COLS):
		for r in range(ROWS):
			pygame.draw.rect(win, COLORS[tiles[c][r][0]], (tiles[c][r][1]+3, tiles[c][r][2]-T_HEIGHT*tiles[c][r][3]+3, T_WIDTH-6, T_HEIGHT-6))
	pygame.draw.rect(win, (100,100,100), (t_pos[0]*T_WIDTH, t_pos[1]*T_HEIGHT, T_WIDTH, T_HEIGHT), 2)
	pygame.draw.rect(win, (255,255,255), (t_selected[0]*T_WIDTH, t_selected[1]*T_HEIGHT, T_WIDTH, T_HEIGHT), 3)
	texts(score)
	pygame.display.update()
pygame.quit()
sys.exit()