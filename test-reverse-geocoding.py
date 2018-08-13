import gmplot
import pandas as pd
import requests
import logging
import time
from IPython.display import display
import urllib.request


# source: https://gist.github.com/shanealynn/033c8a3cacdba8ce03cbe116225ced31

logger = logging.getLogger("root")
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)

API_KEY = "AIzaSyDlSW-rf4lc5SvxQKVSox7E5XSIQrTAojY"

BACKOFF_TIME = 30

RETURN_FULL_RESULTS = False

raw_data= pd.read_csv(r"C:\Users\Labeeba\Desktop\new_opensky\active_rx.csv", encoding='utf8')

#display(raw_data.head(n=672))
data = raw_data.head(n=672)

latitudes = data["position__latitude"]
longitudes = data["position__longitude"]



api_url = "http://maps.googleapis.com/maps/api/geocode/json?sensor=false&language=en"

#api_url = api_url + "&key={}".format(api_key)
lat = list(latitudes)
lon = list(longitudes)
coordinates = ['%f,%f' % (lat1, lon1) for lat1, lon1 in zip(lat,lon)]


def google_results(coordinate, return_full_response=False):  
    api_url = "https://maps.googleapis.com/maps/api/geocode/json?sensor=false&language=en&key=AIzaSyDlSW-rf4lc5SvxQKVSox7E5XSIQrTAojY&latlng={}".format(coordinate)
    #api_url = api_url + "&key={}".format(api_key)
    results = requests.get(api_url)
    results = results.json()
    return results['results'][0]

countries= {}
for c in coordinates:
    #geocoded = False
    #while geocoded is not True:
        try:
            
            answer = google_results(c, return_full_response=RETURN_FULL_RESULTS)
            addr = answer["address_components"]
            
            for a in addr:
                if "country" in a["types"]:
                    country = a["long_name"]
                    if country in countries.keys():
                            countries[country]+= 1
                    else:
                            countries[country]=1
        except Exception as e:
            logger.exception(e)
            logger.error("Error with {}".format(c))
            logger.error("Skipping!")
            #geocoded = True
    
    #resp = urllib.request.urlopen(api_request)
    #print(resp.read())
logger.info("Finished geocoding all addresses")
print("Receiver density in each country: ")
print(countries)

print("Countries with 4 or more receivers: ")
i=1
for c, v in countries.items():
    if v >= 4:
        print(i,".", c ,"-", v, sep='')
        i+=1
#pd.DataFrame(results).to_csv(output_filename, encoding='utf8')

