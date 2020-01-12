import socket
import pygame
import sys

HOST = "192.168.137.1"
PORT = 65432

pygame.init()
screen = pygame.display.set_mode((200, 200))

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	s.connect((HOST, PORT))
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				print("quitttting")
				pygame.quit()
				sys.exit()
			elif event.type == 2: 		#button down
				text = str(event.key) + " d "
				s.send(text.encode('utf-8'))
				print("released "+str(event.key))
			elif event.type == 3:	#button up
				text = str(event.key) + " u "
				s.send(text.encode('utf-8'))
				print("released "+str(event.key))

pygame.quit()
sys.exit()
			