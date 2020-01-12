import mechanicalsoup
import random
import webbrowser
import time
from termcolor import colored
from os import system
system("title "+"Sick_Yt_Random_Things_Player")

br=mechanicalsoup.StatefulBrowser()

while True:
	links = []
	term = str(input("Search for "))
	term.replace(' ','+')
	br.open("https://www.youtube.com/results?search_query="+term)
	resp = br.get_current_page()
	count = 0
	#print(resp.text)
	print(colored("What I've found:", 'blue'))
	#print(resp.text)
	for link in resp.findAll('a',attrs={"dir" : "ltr"}, href=True ):
		if(link["href"].split('?')[0] == "/watch" and count <= 10):
			count+=1
			links.append((link.text,link["href"]))
			print(colored("{0}.{1}".format(count,link.text),'green'))
	if(len(links) != 0):
		#l = random.choice(links)
		l = int(input("Choose ur beat:"))
		#print("How about: {0}? (y/n)".format(links[l][0]))
		#if(input("-> ") == 'y'):
		print("Playin ' {0}".format(links[l][0]))
		gohere = "https://www.youtube.com"+str(links[l][1])
		#print(gohere)
		time.sleep(2)
		webbrowser.open(gohere)
		time.sleep(1)
	else:
		print(colored("I'm a shit ass program and for some god forsaken reason can't load this shit",'red'))
		#br.refresh()
		#print(br.get_current_page().prettify())