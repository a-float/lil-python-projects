import mechanicalsoup
import time
import json
import string

printable = set(string.printable)

changes = []
new_episodes = {}
with open("anime_episodes.json",'r') as f:	#load old  data
	old_episodes = json.load(f)
new_episodes.update(old_episodes)	
br=mechanicalsoup.StatefulBrowser()
for page_num in range(5,0,-1):
	url = "https://www03.gogoanimes.tv//page-recent-release.html?page="+str(page_num)
	br.open(url)
	resp = br.get_current_page()
	data = resp.findAll('p',attrs={'class' : 'name'})	#get new data
	for d in data:
		new_episodes.update({d.text : int(d.find('a')['href'].split('-')[-1])})
#new_episodes['Bakumatsu'] = 66666
#new_episodes['test_anime'] = 999999

for k in new_episodes.keys():			#find changes
	if(k in old_episodes.keys()):
		if(new_episodes[k] != old_episodes[k]):
			changes.append('"{0}" has a new episode {1} -> {2}\n'.format(k,old_episodes[k],new_episodes[k]))
	else:
		changes.append('"{0}" has been added -> {1}\n'.format(k,new_episodes[k]))

for e in new_episodes.items():					#print results
	print("'{0}' {1}".format(e[0],e[1]))
print("Changes made: " + str(len(changes)))

with open("updates.txt",'r') as f:			#save changes
	r = f.read()	
with open("updates.txt",'w') as f:
	f.write(str(time.asctime()).strip() +"\n")
	for c in changes:
		#c1 = "".join(list(filter(lambda x: x in printable, c)))
		try:
			f.write(str(c))
		except UnicodeEncodeError:
			f.write("someanimehere\n")
		print(str(c))
	f.write(r)


with open("anime_episodes.json",'w') as f:		#save new episodes
	f.write(json.dumps(new_episodes,indent=2))
time.sleep(3)
