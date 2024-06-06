# This file aims to extract all maximum obscuration totality values for a given coordinate point. 
import math
from skyfield.api import Topos, load
import openpyxl
import pandas as pd
from datetime import datetime, timedelta, time
from timezonefinder import TimezoneFinder
from zoneinfo import ZoneInfo
from tqdm import tqdm

# obscuration algorithm - variables pulled from skyfield.api
def obscuration_algorithm_skyfield(latitude, longitude, dt, altitude=0.0):
    ts = load.timescale()
    t = ts.utc(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)
    
    eph = load('de431t.bsp')
    observer = eph['earth'] + Topos(latitude_degrees=latitude, longitude_degrees=longitude, elevation_m=altitude)
    
    sun = eph['sun']
    moon = eph['moon']
    
    astrometric_sun = observer.at(t).observe(sun).apparent()
    astrometric_moon = observer.at(t).observe(moon).apparent()
    
    sun_distance = astrometric_sun.distance().km
    moon_distance = astrometric_moon.distance().km

    sun_radius_km = 696340  
    moon_radius_km = 1737.4  

    sun_angular_radius = sun_radius_km / sun_distance
    moon_angular_radius = moon_radius_km / moon_distance
    sun_moon_distance = astrometric_sun.separation_from(astrometric_moon).radians

    # if there is no obscuration
    if sun_moon_distance >= sun_angular_radius + moon_angular_radius:
        obscuration = 0.0
    # some obscuration...
    elif sun_moon_distance <= abs(sun_angular_radius - moon_angular_radius):
        # accounting for some obscuration
        if moon_angular_radius < sun_angular_radius:
            obscuration = (moon_angular_radius ** 2) / (sun_angular_radius ** 2)
            # 100% obscuration
        else:
            obscuration = 1.0
    # partial obscuration
    else:
        r1, r2, d = sun_angular_radius, moon_angular_radius, sun_moon_distance
        part1 = r1**2 * math.acos((d**2 + r1**2 - r2**2) / (2 * d * r1))
        part2 = r2**2 * math.acos((d**2 + r2**2 - r1**2) / (2 * d * r2))
        part3 = 0.5 * math.sqrt((-d + r1 + r2) * (d + r1 - r2) * (d - r1 + r2) * (d + r1 + r2))
        intersection_area = part1 + part2 - part3
        obscuration = intersection_area / (math.pi * r1 ** 2)

    return obscuration * 100  # convert to percentage


# timezone identification
tf = TimezoneFinder()
    
# file w/ updated cleaned latitude and longitude values
coordinates = pd.read_excel(r'EXCEL FILE')

# full solar eclipse date/time (can change if needed...)
eclipse_date = "2024-04-08"
eclipse_time = "18:00:00"

# creating an empty list, iterating through each latitude and longitude point in the dataframe, calculating obscuration for each row, appending these values to the created list...
obscuration_data = []
for index, row in coordinates.iterrows():
    latitude = row['LATITUDE']
    longitude = row['LONGITUDE']
    timezone_name = tf.timezone_at(lat=latitude, lng=longitude)
    if timezone_name:
        timezone = ZoneInfo(timezone_name)
        naive_dt = datetime.strptime(f"{eclipse_date} {eclipse_time}", "%Y-%m-%d %H:%M:%S")
        local_dt = naive_dt.replace(tzinfo=timezone)
        obscuration = obscuration_algorithm_skyfield(latitude, longitude, local_dt)
    else:
        obscuration = None
        
    obscuration_data.append(obscuration)
    
# adding the new values from algorithm to the empty list
coordinates['OBSCURATION'] = obscuration_data

# creating a new file with new obscuration data
coordinates.to_excel('new dataframe30.xlsx', index=False)
print(coordinates)

