import os
from dotenv import load_dotenv
import requests
import json
from datetime import datetime

load_dotenv()

def save_json(data_json):

    day = datetime.now()
    name_data = "place_api_google/poi_google_maps_"+str(day).replace(":","_").replace(".","_").replace(" ","_").replace("-","_")+".json"

    with open(name_data, "w") as outfile: 
        json.dump(data_json, outfile)

def find_place_text(query, api_key):    
    # Define the API endpoint
    url = 'https://places.googleapis.com/v1/places:searchText'

    # Define the headers
    headers = {
        'Content-Type': 'application/json',
        'X-Goog-Api-Key': api_key,  # Replace 'API_KEY' with your actual Google Places API key
        'X-Goog-FieldMask': '*'
    }

    # Define the data payload for the POST request
    data = {
        'textQuery': query
    }

    # Make the POST request
    response = requests.post(url, headers=headers, json=data)

    # Check if the request was successful
    if response.status_code == 200:
        # Process the response
        print(response.json())
    else:
        print(f"Error: {response.status_code}, {response.text}")
    return json.loads(response.text)

def find_place_nearby(query, api_key, lat, log):

        # Define the API endpoint
    url = 'https://places.googleapis.com/v1/places:searchNearby'

    # Define the headers
    headers = {
        'Content-Type': 'application/json',
        'X-Goog-Api-Key': api_key,  # Replace 'API_KEY' with your actual Google Places API key
        'X-Goog-FieldMask': '*'
    }

    # Define the data payload for the POST request
    data = {
        "excludedTypes": ["primary_school"],
        "rankPreference": "DISTANCE",
        "locationRestriction": {
            "circle": {
                "center": {
                    "latitude": lat,
                    "longitude": log
                },
                "radius": 50000 # Raio varia entre 0 e 50.000
            }
        }
    }

    # Make the POST request
    response = requests.post(url, headers=headers, json=data)

    # Check if the request was successful
    if response.status_code == 200:
        # Process the response
        print(response.json())
    else:
        print(f"Error: {response.status_code}, {response.text}")

    save_json(json.loads(response.text))
    return json.loads(response.text)


if __name__ == '__main__':

    api_key = os.environ['API_KEY']

    query = "restaurantes porto"
    lat = 41.152967
    log = -8.610042

    find_place_nearby(query, api_key, lat, log)
    # find_place_text(query, api_key)
    # 41.152967, -8.610042