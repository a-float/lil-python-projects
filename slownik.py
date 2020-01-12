import mechanicalsoup
import re
from os import system
system("title "+"Sick_Słownik")

#term = "małpa"
while True:
	term = str(input("Search for "))
	br=mechanicalsoup.StatefulBrowser()
	url = "https://sjp.pl/"+term
	br.open(url)
	resp = br.get_current_page()
	ans = re.split(r'\d.\ ',resp.findAll('p')[3].text.strip())
	for a in ans:
		if(len(a)>3 and a!= "POWIĄZANE HASŁA:" and a!= "dodaj komentarz"):
			print('-{}'.format(a))
	print()