import sys 
import pygame
import random
from pygame.locals import *
DIFF = 100 #distance between pipes
OPENSIZE = 140 #size of the openings
GRAVITY = 0.3
FLAP_PWR = -6 #flap power
PIPE_SPEED = -2
PIPE_MIN = 60 #min distance between end of the pipe and the edge of the screen
PIPE_WIDTH = 90
SPWN_PIPE = USEREVENT + 1 #event number
width, height = 400, 600
BIRD_POS = (width/2.5, height/2)
gameover = False        # TODO maybe bird.dead? i dontkno
score = 0         #TODO class var?

class Bird(pygame.sprite.Sprite):
  def __init__(self):
    pygame.sprite.Sprite.__init__(self)
    #self.image = pygame.Surface([40,35])
    #self.image.fill((255,255,255))
    #self.image.set_colorkey((255,255,255))
    self.image = pygame.transform.scale(pygame.image.load('./bird.png').convert_alpha(), (55,55))
    self.yspeed = 0

    #pygame.draw.ellipse(self.image, (0,0,0), [0,0, self.image.get_width(), self.image.get_height()])
    self.rect = self.image.get_rect(center = BIRD_POS)
  
  def update(self):
    newpos = self.rect.move(0, self.yspeed)
    if newpos.bottom > height:
      newpos.bottom = height
      self.yspeed = 0
    self.rect = newpos
    self.yspeed += GRAVITY

  def flap(self):
    if gameover == False:  
      self.yspeed = FLAP_PWR


class Pipe(pygame.sprite.Sprite):
  def __init__(self, pos, dir):    #pos of previous pipe, opening of previous pipe
    pygame.sprite.Sprite.__init__(self)
    # self.image = pygame.Surface([PIPE_WIDTH, height])
    # self.image.fill((255,255,255))
    # self.image.set_colorkey((255,255,255))    #TODO add actual sprites
    self.image = pygame.transform.scale(pygame.image.load("pipe.png").convert_alpha(), [PIPE_WIDTH, int(height/1.4)])
    if dir == "top":
      self.image = pygame.transform.flip(self.image, False, True)
      # pygame.draw.rect(self.image, (0,255,0), [0,0, PIPE_WIDTH, height])
      self.rect = self.image.get_rect(bottomleft = pos)
    else:
      # pygame.draw.rect(self.image, (0,255,255), [0,0, PIPE_WIDTH, height])
      self.rect = self.image.get_rect(topleft = (pos[0], pos[1]))
    self.xspeed = PIPE_SPEED
    self.gave_point = False
  
  def update(self):
    if not gameover:
      newpos = self.rect.move(self.xspeed, 0)
      self.rect = newpos
      if self.rect.center[0] < BIRD_POS[0] and not self.gave_point:
        global score
        score += 1
        self.gave_point = True
      if self.rect.right < 0:
        self.kill()

def spawn_pipe():   #TODO get those func in a class or smth
  opening = random.randrange(PIPE_MIN, height-PIPE_MIN-OPENSIZE)
  pipe1 = Pipe((width + 20, opening), "top")
  pipe2 = Pipe((width + 20, opening + OPENSIZE), "bottom")
  pipesprites.add(pipe1, pipe2)

def restart():
  global gameover
  gameover = False
  bird.rect.center = BIRD_POS
  global score
  score = 0
  for i in pipesprites.sprites():
    i.kill()

pygame.init() 
pygame.time.set_timer(SPWN_PIPE, 2000)
pygame.display.set_caption("Flappy C0py")
fps = 60
fpsClock = pygame.time.Clock()
 
screen = pygame.display.set_mode((width, height))

bird = Bird()
birdsprite = pygame.sprite.GroupSingle((bird))
pipesprites = pygame.sprite.RenderPlain(())

background = pygame.image.load("background.png")
background = pygame.transform.scale(background, [width, height]).convert_alpha()

font = pygame.font.Font(None, 64)
text = font.render(str(score), True, (0,0,0))
text_rect = text.get_rect()

# Game loop.
while True:
  screen.fill((250,250,250))
  for event in pygame.event.get():
    if event.type == QUIT:
      pygame.quit()
      sys.exit()
    elif event.type == KEYDOWN:
      if event.key == K_SPACE:
        bird.flap()
      if event.key == K_r:
        restart()
    elif event.type == SPWN_PIPE:
      spawn_pipe()

  # Update.
  bird.update()
  pipesprites.update()
  text = font.render(str(score/2), True, (0,0,0))   #TODO it prbably should be here
  text_rect = text.get_rect()
  if pygame.sprite.spritecollideany(bird, pipesprites, collided = None) and not gameover:
    bird.yspeed = -4
    gameover = True

  # Draw.
  screen.blit(background, (0,0))
  pipesprites.draw(screen)
  birdsprite.draw(screen)
  screen.blit(text, text_rect)
  pygame.display.flip()
  fpsClock.tick(fps)