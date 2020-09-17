import requests
import json

class bus_api:
    def __init__(self):
        self.API_KEY = ""
        self.APP_ID = ""

    def loadconfig(self):
        with open('busboard.config') as configfile:
            configs = []
            for line in configfile:
                configs.append(line[:-1])
            self.API_KEY = configs[0].split("=")[1]
            self.APP_ID = configs[1].split("=")[1]

    def get_bus_info(self,post_code):
        request = requests.get("http://api.postcodes.io/postcodes/"+post_code.upper())
        dict = json.loads(request.text)
        result = dict["result"]
        lat = result["latitude"]
        long = result["longitude"]

        request = requests.get("http://transportapi.com/v3/uk/places.json?lat="+str(lat)+"&lon="+str(long)+"&type=bus_stop",params={'api_key':self.API_KEY,'app_id':self.APP_ID})
        dict = json.loads(request.text)
        bus_stops = []
        for i in dict["member"][:2]:
            bus_code = i["atcocode"]
            request = requests.get("http://transportapi.com/v3/uk/bus/stop/"+bus_code+"/live.json",params={'api_key':self.API_KEY,'app_id':self.APP_ID})
            bus_stops.append(request.text)
        return(bus_stops)
