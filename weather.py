import requests as r
from bs4 import BeautifulSoup
import json
import math
from datetime import datetime
t = input("Enter any place: ")
text = t+"+latitude+longitude"
url_for_lat_and_long = "https://www.google.com/search?q="+text
#above steps are just to arrange the url based on locations
response = r.get(url_for_lat_and_long )#http request
soup = BeautifulSoup(response.text,"html.parser")# using a parser
lat_long = soup.find(class_="BNeawe iBp4i AP7Wnd")#to find the class which holds the lat and long values
if(lat_long is not None):
    m = lat_long.get_text().split(",")#split as we need lat and long in two seperate variables
    la = m[0]#holds lat with direction
    lo = m[1]#hold long with direction
    long = ""
    lat = ""
    for i in lo:
        if(i.isnumeric() or i == '.'):
            long += i
    # to just have numbers, therefore removing direction
    for i in la:
        if(i.isnumeric() or i =='.'):
            lat += i
    # to just have numbers, therefore removing direction
    url = "https://api.openweathermap.org/data/2.5/weather?lat="+ lat +"&lon="+ long +"&appid=281025482b8af38fa55d16b57772e588"
    new_response = r.get(url)#request for weather api data
    #new_response.text is the str json data
    data = json.loads(new_response.text)#this converts the json to dict
    for desc,info in data.items():
        #iterating through keys and values
        if desc == 'weather':
            #this key has a value of list, thus we took it seperately
            for val in info:
                #list contains dict
                for sub,value in val.items():
                    #iterating through key and values of list
                    if sub != "main":
                        print(sub + ":" + str(value))
        if  desc == "rain":
            #selecting particular key to show up
            for sub,value in info.items():
                print("HEYYYYYYYYYYYYYYY")
                #iterating through key and values
                print(sub + ":" + str(value))
        if desc == 'main':
            #selecting main seperately as we have to change the units
            for sub,value in info.items():
                #iterating through key and values
                if sub == 'temp' or sub == 'feels_like' or sub == "temp_min" or sub == "temp_max":
                    print(sub + ":" + str(math.ceil((-273 + value)*100)/100) + " C")
                if sub == "pressure":
                    print(sub + ":" + str(math.ceil((0.02953*value)*100 )/100) + " Hg")
                if sub == "humidity":
                    print(sub + ":" + str(value) + " %")
        if desc == "wind":
            #selecting particular key to show up
            for sub,value in info.items():
                #iterating through key and values
                print("wind " + sub + ":" + str(value))
        if desc == "sys":
            #system
            for sub,value in info.items():
                #iterate through keys and values
                if sub == "country":
                    print(sub + ":" + str(value))
                if sub == "sunrise" or sub == "sunset":
                    print(sub + ":" + str(datetime.utcfromtimestamp(value).strftime('%D %H:%M:%S')))
else:
    # if there is a wrong place entered by user
    print("Error!! Have a look at the place you entered")