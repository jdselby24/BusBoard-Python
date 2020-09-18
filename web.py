from flask import Flask, render_template, request
import bus_api
import json

app = Flask(__name__)
busHandler = bus_api.bus_api()

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/busInfo")
def busInfo():
    bus_stops = []
    departures = [[], []]
    postcode = request.args.get('postcode')    
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
                if(departure['expected_departure_time'] != None):
                    time = departure['expected_departure_time'].replace(":","")
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
