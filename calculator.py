import pandas as pd
import ephem as ep
import math

def obscuration_algorithm(latitude, longitude, date):
    observer = ep.Observer()
    observer.lat = str(latitude)
    observer.long = str(longitude)
    observer.date = date
    
    sun = ep.Sun(observer)
    moon = ep.Moon(observer)
    
    # Angular size of the Moon and the Sun in degrees
    angular_size_sun = math.degrees(sun.size) * 3600
    angular_size_moon = math.degrees(moon.size) * 3600
    
    # Calculating obsuration totality...
    obscuration = (angular_size_sun - angular_size_moon) / angular_size_sun 
    
    return obscuration 

# Load data
coordinates = pd.read_csv(r'C:\Users\bzwil\OneDrive\Documents\OBSCURATION ALGORITHM\OBSCURATION-TOTALITY\clean dataset - 4_8_24 total solar eclipse.csv')

# Date of Eclipse
eclipse_date = "2024-04-08"

# Calculating obscuration for each datapoint
obscuration_data = []
for index, row in coordinates.iterrows():
    latitude = row['LATITUDE']
    longitude = row['LONGITUDE']
    obscuration = obscuration_algorithm(latitude, longitude, eclipse_date)
    obscuration_data.append(obscuration)
    
# Adding obscuration totality to csv file
coordinates['OBSCURATION'] = obscuration_data

print(coordinates)

    