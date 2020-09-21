from flask import Flask, render_template, request
import json
import re
import time
import requests

app = Flask(__name__)


class bus_api:
    def __init__(self):
        self.API_KEY = ""
        self.APP_ID = ""

    def loadconfig(self):
        with open('busboard.config') as configfile:
            configData = json.load(configfile)
            self.API_KEY = configData['api-key']
            self.APP_ID = configData['app-id']

    def get_bus_info(self,post_code):
        request = requests.get("https://api.postcodes.io/postcodes/"+post_code.upper())
        dict = json.loads(request.text)
        result = dict["result"]
        lat = result["latitude"]
        long = result["longitude"]

        request = requests.get("https://transportapi.com/v3/uk/places.json?lat="+str(lat)+"&lon="+str(long)+"&type=bus_stop",params={'api_key':self.API_KEY,'app_id':self.APP_ID})
        time.sleep(0.25)
        dict = json.loads(request.text)
        bus_stops = []
        for i in dict["member"][:2]:
            bus_code = i["atcocode"]
            request = requests.get("https://transportapi.com/v3/uk/bus/stop/"+bus_code+"/live.json",params={'api_key':self.API_KEY,'app_id':self.APP_ID})
            time.sleep(0.25)
            bus_stops.append(request.text)
        return(bus_stops)

busHandler = bus_api()

@app.route("/")
def index():
    return render_template('index.html', postcodeInvalid=False, postcode="")

@app.route("/busInfo")
def busInfo():
    postcode = request.args.get('postcode')
    postcodeRegex = re.compile("([Gg][Ii][Rr] 0[Aa]{2})|((([A-Za-z][0-9]{1,2})|(([A-Za-z][A-Ha-hJ-Yj-y][0-9]{1,2})|(([A-Za-z][0-9][A-Za-z])|([A-Za-z][A-Ha-hJ-Yj-y][0-9][A-Za-z]?))))\s?[0-9][A-Za-z]{2})")   

    if not(postcodeRegex.match(postcode)):
        return render_template("index.html", postcodeInvalid=True, postcode=postcode)
    else:
        bus_stops = []
        departures = [[], []]
        
        busHandler.loadconfig()
        api_response = busHandler.get_bus_info(postcode)
        for i in api_response:
            nearby_stop = json.loads(i)
            bus_stops.append(nearby_stop)

        for i in range(len(bus_stops)):
            departures = []
            departuresUnsorted = bus_stops[i]['departures']
            for line in departuresUnsorted:
                departureListLine = departuresUnsorted[line]
                for departure in departureListLine:
                    if(departure['best_departure_estimate'] != None):
                        time = departure['best_departure_estimate'].replace(":","")
                        departure['sortTime'] = int(time)
                    else: 
                        departure['sortTime'] = 9999
                    departures.append(departure)

                departures = sorted(departures, key = lambda x: x['sortTime']) 

            if len(departures) > 5:
                departures = departures[:5]
            
            bus_stops[i]['departures'] = departures

        return render_template('info.html', postcode=postcode,bus_stops=bus_stops)
    
if __name__ == "__main__": app.run()
