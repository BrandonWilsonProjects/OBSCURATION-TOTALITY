# This file allows for a comparison of obscuration percentage datasets at different times
import math
from skyfield.api import Topos, load
import openpyxl
import pandas as pd
from datetime import datetime, timedelta, time
from timezonefinder import TimezoneFinder
from zoneinfo import ZoneInfo
from tqdm import tqdm
import matplotlib.pyplot as plt

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
coordinates = pd.read_csv(r'CSV FILE')

# eclipse date/time for first comparison dataset
eclipse_date_1 = "2024-04-08"
eclipse_time_1 = "12:00:00"
eclipse_time_2 = "4:00:00"

# creating an empty list, iterating through each latitude and longitude point in the dataframe, calculating obscuration for each row, appending these values to the created list...
obscuration_data_1 = []
obscuration_data_2 = []
for index, row in coordinates.iterrows():
    latitude = row['LATITUDE']
    longitude = row['LONGITUDE']
    timezone_name = tf.timezone_at(lat=latitude, lng=longitude)
    if timezone_name:
        timezone = ZoneInfo(timezone_name)
        naive_dt_1 = datetime.strptime(f"{eclipse_date_1} {eclipse_time_1}", "%Y-%m-%d %H:%M:%S")
        naive_dt_2 = datetime.strptime(f"{eclipse_date_1} {eclipse_time_2}", "%Y-%m-%d %H:%M:%S")
        local_dt_1 = naive_dt_1.replace(tzinfo=timezone)
        local_dt_2 = naive_dt_2.replace(tzinfo=timezone)
    obscuration_1 = obscuration_algorithm_skyfield(latitude, longitude, local_dt_1)
    obscuration_data_1.append(obscuration_1)
    obscuration_2 = obscuration_algorithm_skyfield(latitude, longitude, local_dt_2)
    obscuration_data_2.append(obscuration_2)

# seting values to graph in the bar chart (can change if needed...)
low_obscuration_1 = [95]
high_obscuration_1 = [87 < obscuration_1 <= 95.0]

low_obscuration_2 = [70]
high_obscuration_2 = [60 < obscuration_2 <= 75]

# plotting the bar graph (can change if needed...)
plt.bar(low_obscuration_1, high_obscuration_1, label='Obscuration 12 hrs into 4/8', color='r')
plt.bar(low_obscuration_2, high_obscuration_2, label='Obscuration 4 hrs into 4/8', color='c')

plt.xlabel('obscuration percentage')
plt.ylabel('quantity of respectively categorized obscuration values')
plt.title('Obscuration Comparison Graph')
plt.legend()
plt.show()


