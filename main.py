import requests
import json
API_KEY = ""
APP_ID = ""

def loadconfig():
    with open('busboard.config') as configfile:
        configs = []
        for line in configfile:
            configs.append(line[:-1])
        API_KEY = configs[0].split("=")[1]
        APP_ID = configs[1].split("=")[1]
    return API_KEY, APP_ID


def main():
    API_KEY, APP_ID = loadconfig()
    print("Enter post code")
    #post_code = input()
    post_code = "ba11an"

    #bus_code = "0180BAC30592"
    #request = requests.get("http://transportapi.com/v3/uk/bus/stop/"+bus_code+"/live.json",params={'api_key':API_KEY,'app_id':APP_ID})
    #print(request.text)

    request = requests.get("http://api.postcodes.io/postcodes/"+post_code.upper())
    #print(json.loads(request.text))
    dict = json.loads(request.text)
    result = dict["result"]
    lat = result["latitude"]
    long = result["longitude"]

    request = requests.get("http://transportapi.com/v3/uk/places.json?lat="+str(lat)+"&lon="+str(long)+"&type=bus_stop",params={'api_key':API_KEY,'app_id':APP_ID})
    dict = json.loads(request.text)

    #print(dict["member"][:2])
    #print()
    for i in dict["member"][:2]:
        bus_code = i["atcocode"]
        request = requests.get("http://transportapi.com/v3/uk/bus/stop/"+bus_code+"/live.json",params={'api_key':API_KEY,'app_id':APP_ID})
        print(request.text)




if __name__ == "__main__": main()
