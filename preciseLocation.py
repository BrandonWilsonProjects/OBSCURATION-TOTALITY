from geopy import Nominatim
import pandas as pd
from geopy.exc import GeocoderTimedOut
from geopy.point import Point
import time

def precise_location(geolocator, latitude, longitude, max_retries=3):
   retries = 0
   while retries < max_retries:
       try:
           location = geolocator.reverse((latitude, longitude), exactly_one=True)
           return location
       except GeocoderTimedOut:
           retries += 1
           time.sleep(1)
           return None

# Load file
new_coordinates = pd.read_csv(r'C:\Users\bzwil\OneDrive\Desktop\OBSCURATION ALGORITHM\OBSCURATION-TOTALITY\clean dataset - 4_8_24 total solar eclipse.csv')

# Initialize Nominatim API
geolocator = Nominatim(user_agent="geoapiExcersises")

# Store results of cities, states, and countries in list
cities = []
states = []
countries = []

# Itterate through each 'LATITUDE' and 'LONGITUDE' datapoint
for index, row in new_coordinates.iterrows():
    latitude = row['LATITUDE']
    longitude = row['LONGITUDE']
    # Check for validity of latitude and longitude data 
    if pd.isnull(latitude) or pd.isnull(longitude):
        print(f"Invalid coordinates at index {index}: ({latitude}, {longitude})")
        city = state = country = ''
    else:
        try:
            latitude = float(latitude)
            longitude = float(longitude)
        except ValueError:
            print(f"Non-numeric coordinates at index {index}: ({latitude}, {longitude})")
            city = state = country = ''
            cities.append(city)
            states.append(state)
            countries.append(country)
            continue
    
    location = precise_location(geolocator, latitude, longitude)
    
    if location:
        address = location.raw['address']
        city = address.get('city', address.get('town', address.get('village', '')))
        state = address.get('state', '')
        country = address.get('country', '')
    else:
        city = state = country = ''
        
    cities.append(city)
    states.append(state)
    countries.append(country)
    
if len(cities) == len(states) == len(countries) == len(new_coordinates):
    new_coordinates['city'] = cities
    new_coordinates['state'] = states
    new_coordinates['country'] = countries
    
    new_coordinates.to_csv('completedDataset.csv', index=False)
    print("Geocoding complete")
else:
    print("Error")
