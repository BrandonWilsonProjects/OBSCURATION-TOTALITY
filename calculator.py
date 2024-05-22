# This file calculates the obscuration percentage for latitude and longitude values in a csv file for any given time throughout the day of the eclipse.
import ephem
import openpyxl
import pandas as pd
import math
from datetime import datetime
from datetime import time


def obscuration_algorithm(latitude, longitude, date, time_str):
    observer = ephem.Observer()
    observer.lat = str(latitude)
    observer.lon = str(longitude)
    
    dt = datetime.strptime(f"{date} {time_str}", "%Y-%m-%d %H:%M:%S")
    observer.date = dt
    
    sun = ephem.Sun(observer)
    moon = ephem.Moon(observer)

    # calculating angular radius for both the sun and the moon
    sun_angular_radius = sun.size / (2 * 60) * (math.pi / 180)
    moon_angular_radius = moon.size / (2 * 60) * (math.pi / 180)

    # finding the angular distance between the center of the sun and the moon
    sun_moon_distance = ephem.separation((sun.az, sun.alt), (moon.az, moon.alt))

    # calculating the obscuration considering potential overlap of both astronomical objects
    if sun_moon_distance >= sun_angular_radius + moon_angular_radius:
        obscuration = 0.0
    elif sun_moon_distance <= abs(sun_angular_radius - moon_angular_radius):
        # complete totality
        obscuration = (moon_angular_radius ** 2 / sun_angular_radius ** 2) if moon_angular_radius < sun_angular_radius else 1.0
    else:
        # partial overlap
        r1, r2, d = sun_angular_radius, moon_angular_radius, sun_moon_distance
        part1 = r1**2 * math.acos((d**2 + r1**2 - r2**2) / (2 * d * r1))
        part2 = r2**2 * math.acos((d**2 + r2**2 - r1**2) / (2 * d * r2))
        part3 = 0.5 * math.sqrt((-d + r1 + r2) * (d + r1 - r2) * (d - r1 + r2) * (d + r1 + r2))
        intersection_area = part1 + part2 - part3
        obscuration = intersection_area / (math.pi * r1 ** 2)

    return obscuration * 100  # convert to percentage
    
# file w/ updated cleaned latitude and longitude values
coordinates = pd.read_csv(r'CSV FILE')

# full solar eclipse date/time (can change if needed...)
eclipse_date = "2024-04-08"
eclipse_time = "12:00:00"

# creating an empty list, iterating through each latitude and longitude point in the dataframe, calculating obscuration for each row, appending these values to the created list...
obscuration_data = []
for index, row in coordinates.iterrows():
    latitude = row['LATITUDE']
    longitude = row['LONGITUDE']
    obscuration = obscuration_algorithm(latitude, longitude, eclipse_date, eclipse_time)
    obscuration_data.append(obscuration)
    
# adding the new values from algorithm to the empty list
coordinates['OBSCURATION'] = obscuration_data

# creating a new file with new obscuration data
coordinates.to_excel('new dataframe8.xlsx', index=False)
print(coordinates)

