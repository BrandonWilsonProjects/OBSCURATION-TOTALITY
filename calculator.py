import ephem
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

    # Calculate the angular size of the Sun and the Moon in radians
    sun_angular_radius = sun.size / (2 * 60) * (math.pi / 180)
    moon_angular_radius = moon.size / (2 * 60) * (math.pi / 180)

    # Calculate the angular distance between the centers of the Sun and Moon
    sun_moon_distance = ephem.separation((sun.az, sun.alt), (moon.az, moon.alt))

    # Calculate the obscuration using the formula for the overlapping area of two circles
    if sun_moon_distance >= sun_angular_radius + moon_angular_radius:
        # No overlap
        obscuration = 0.0
    elif sun_moon_distance <= abs(sun_angular_radius - moon_angular_radius):
        # Total obscuration (one circle is completely inside the other)
        obscuration = (moon_angular_radius ** 2 / sun_angular_radius ** 2) if moon_angular_radius < sun_angular_radius else 1.0
    else:
        # Partial overlap
        r1, r2, d = sun_angular_radius, moon_angular_radius, sun_moon_distance
        part1 = r1**2 * math.acos((d**2 + r1**2 - r2**2) / (2 * d * r1))
        part2 = r2**2 * math.acos((d**2 + r2**2 - r1**2) / (2 * d * r2))
        part3 = 0.5 * math.sqrt((-d + r1 + r2) * (d + r1 - r2) * (d - r1 + r2) * (d + r1 + r2))
        intersection_area = part1 + part2 - part3
        obscuration = intersection_area / (math.pi * r1 ** 2)

    return obscuration * 100  # Convert to percentage
    
# Load data
coordinates = pd.read_csv(r'C:\Users\bzwil\OneDrive\Desktop\OBSCURATION ALGORITHM\OBSCURATION-TOTALITY\clean dataset - 4_8_24 total solar eclipse.csv')

# Date of Eclipse
eclipse_date = "2024-04-24"
eclipse_time = "12:00:00"

# Calculating obscuration for each datapoint
obscuration_data = []
for index, row in coordinates.iterrows():
    latitude = row['LATITUDE']
    longitude = row['LONGITUDE']
    obscuration = obscuration_algorithm(latitude, longitude, eclipse_date, eclipse_time)
    obscuration_data.append(obscuration)
    
# Adding obscuration totality to csv file
coordinates['OBSCURATION'] = obscuration_data

coordinates.to_csv('new dataframe', index=False)

print(coordinates)

