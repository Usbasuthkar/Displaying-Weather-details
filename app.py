from flask import *
from weatherBackend import *
import math
import json
from datetime import *
app = Flask(__name__)
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