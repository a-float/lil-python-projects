import sys
import pygame
import random
import math
from pygame.locals import *
width, height = 400, 400
n = 4

moves = {K_w : "up", K_d : "right", K_s : "down", K_a : "left"}

def spawnNumber(num):
    list = []
    for i in range(4):
        for j in range(4):
            if(num[i][j] == 0):
                list.append((i,j))
    if(len(list) == 0):
        return
    else:
        x = random.choice(list)
        num[x[0]][x[1]] = random.choice([2,4])
    
def change(num,a,b,c,d):
    if(num[c][d] == num[a][b] or num[c][d] == 0):
        num[c][d] += num[a][b]
        num[a][b] = 0

def move(dir,num):
    print(dir)
    if(dir) == "up":
        for i in range(n):
            for j in range(n-1):
                change(numbers,j+1,i,j,i)
    elif(dir) == "down":
        for i in range(n):
            for j in range(n-2, -1, -1):
                change(numbers,j,i,j+1,i)
    elif(dir) == "right":
        for i in range(n):
            for j in range(n-2, -1, -1):
                change(numbers,i,j,i,j+1)
    else:
        for i in range(n):
            for j in range(n-1):
                change(numbers,i,j+1,i,j)

def show(num):
    for i in range(n):
        print(num[i])

numbers = [[0 for _ in range(n)] for __ in range(n)]
show(numbers)
spawnNumber(numbers)

pygame.init()
font = pygame.font.Font(None, 80)
texts = []
rects = []
for i in range(n):
    for j in range(n):
        texts.append(font.render(str(numbers[i][j]), True, (255,255,255)))
        rects.append(texts[i*n + j].get_rect(center = (width/n * j + width/(2*n), height/n * i + height/(2*n))))

screen = pygame.display.set_mode((width, height))
while True:
    screen.fill((0,0,0))
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit() 
        if event.type == KEYDOWN:
            if event.key in moves.keys():
                move(moves[event.key], numbers)
                spawnNumber(numbers)
                show(numbers)

    for i in range(n):
        for j in range(n):
            if(numbers[i][j] == 0):
                col = 20
            else:
                col = int(math.log(numbers[i][j], 2)/11 * (255-20))
            texts[i*n + j] = font.render(str(numbers[i][j]), True, (0, col, 255-col))
            center_pos = (width/n * j + width/(2*n), height/n * i + height/(2*n))
            rects[i*n+j] = texts[i*n + j].get_rect(center = center_pos)

    for i in range(n**2):
        screen.blit(texts[i], rects[i])
    pygame.display.flip()    
