import requests
import json
import time

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