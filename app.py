from flask import *
import requests as r
from bs4 import BeautifulSoup
import math
import json
from datetime import *
from datetime import *
app = Flask(__name__)
def weather_details(place):
    url = "https://www.google.com/search?q="+place+"Longitude+and+Latitude"
    Response = r.get(url)
    soup = BeautifulSoup(Response.text,"html.parser")
    lat_long = soup.find(class_ = "BNeawe iBp4i AP7Wnd").text
    lat_and_long = lat_long.split(",")
    lat = lat_and_long[0]
    long = lat_and_long[1]
    new_lat = ""
    new_long = ""
    if 'S' in lat:
        new_lat = new_lat + "-"
    if 'W' in long:
        new_long = new_long + "-"
    for i in lat:
        if(i.isnumeric() or i=="."):
            new_lat = new_lat + i
    for i in long:
        if(i.isnumeric() or i=="."):
            new_long = new_long + i
    return new_lat,new_long
def add(new_lat,new_long):
    weather_url = "https://api.openweathermap.org/data/2.5/weather?lat="+ new_lat +"&lon="+ new_long +"&appid=281025482b8af38fa55d16b57772e588"
    new_Response = r.get(weather_url)
    data = json.loads(new_Response.text)
    return data
def weather(data):
    for desc,info in data.items():
        #iterating through keys and values
        if desc == 'weather':
            #this key has a value of list, thus we took it seperately
            return info[0]["description"]
    return None
def rain(data):
    for desc,info in data.items():
         if  desc == "rain":
            return info
    return None
def main(data):
    for desc,info in data.items():
        if desc == 'main':
            #selecting main seperately as we have to change the units
            return info
    return None
def wind(data):
    for desc,info in data.items():
        if desc == "wind":
            #selecting particular key to show up
            return info
    return None
def sys(data):
    for desc,info in data.items():
        if desc == "sys":
            #system
            return info
    return None
@app.route("/")
def ome():
    return render_template("index.html")
@app.route("/",methods=["POST"])
def home():
    if request.method == "POST":
        search = request.form['searchh']
    try:
        lat,long = weather_details(search)
        search = search.upper()
        new_data = add(lat,long)
        description = weather(new_data).capitalize()
        temperature = main(new_data)
        main_temp = round(temperature['temp'] - 273,2)
        feel_like = round(temperature['feels_like'] - 273,2)
        wind_ = wind(new_data)
        sys_ = sys(new_data)
        max = round(temperature['temp_max'] - 273,2)
        min = round(temperature['temp_min'] - 273,2)
        press = round(temperature['pressure'],2)
        hum = round(temperature['humidity'],2)
        ws = round(wind_['speed'],2)
        r = sys_['country']
        sunrise = datetime.utcfromtimestamp(sys_['sunrise']).strftime('%H:%M:%S')
        sunset = datetime.utcfromtimestamp(sys_['sunset']).strftime('%H:%M:%S')
    except:
        place = "--"
        r = "--"
        sunrise = "--"
        sunset = "--"
    return render_template("index.html",place = search,description=description,temperature=main_temp,feel_like = feel_like,max=max,min=min,press=press,hum=hum,ws=ws,r=r,sunrise=sunrise,sunset=sunset)
if __name__ == "__main__":
    app.run(debug=True)
