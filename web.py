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
    postcode = request.args.get('postcode')    
    busHandler.loadconfig()
    api_response = busHandler.get_bus_info(postcode)
    for i in api_response:
        nearby_stop = json.loads(i)
        bus_stops.append(nearby_stop["name"])


    return render_template('info.html', postcode=postcode,bus_stops=bus_stops)

if __name__ == "__main__": app.run()
