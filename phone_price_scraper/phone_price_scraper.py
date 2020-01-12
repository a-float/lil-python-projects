#!/home/matt/envs/env/bin/python3

import sys
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

currentDate = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
print(currentDate, end=" ")

PHONEPATH="/home/matt/Projects/my_projects/phone_price_scraper/"
target = PHONEPATH+"prices.json"
read_list = PHONEPATH+"list_phones.txt"
url = "https://www.ceneo.pl/Telefony_komorkowe;szukaj-"

with open(read_list ,"r") as f:
    phones = [x[:-1] for x in f.readlines()]    #getting rid of "/n"
data = {}
for p in phones:
    #print("Prices for "+p)
    try:
        r = requests.get(url + p.replace(' ','+'))
    except:
        print("Unexpected error:", sys.exc_info()[0])
        sys.exit()
    if r.status_code != 200:
        print("Not done :< {}".format(r.status_code))
        sys.exit()
    soup = BeautifulSoup(r.text, features="html.parser")
    d = soup.find_all("div", {"class" : "cat-prod-row-price"})
    title_price_dict = {}
    for i in range(len(d)):
        title = d[i].find('a')["title"]
        price_span = d[i].find("span" , {"class" : "price"})
        price = float(price_span.contents[0].text) + float(price_span.contents[1].text[1::])/100
        #print('%.2f'%price + "zl", title)
        title_price_dict.update({title : {"prices" : [price], "dates" : [currentDate]}})
    data.update({p : title_price_dict})

with open(target, "r") as f:
    try:
        stored_data = json.load(f)
    except ValueError:
        stored_data = {}

for i in data.keys():
    if i in stored_data.keys():
        for j in data[i].keys():
            if j in stored_data[i].keys():
                stored_data[i][j]["prices"].extend(data[i][j]["prices"])
                stored_data[i][j]["dates"].extend(data[i][j]["dates"])
            else:
                stored_data[i].update({j : data[i][j]})
    else:
        stored_data.update({i : data[i]})
with open(target, "w") as f:
    json.dump(stored_data, f, indent=3)

print("Done! Very nice!")
