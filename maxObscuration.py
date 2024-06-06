# This file aims to extract all maximum obscuration totality values for a given coordinate point. 
import math
from skyfield.api import Topos, load
from datetime import datetime
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

# created start and end timestamps for solar eclipse date
def hourly_timestamps(start_date, start_time, end_time):
    start_datetime = datetime.strptime(f"{start_date} {start_time}", "%Y-%m-%d %H:%M:%S")
    end_datetime = datetime.strptime(f"{start_date} {end_time}", "%Y-%m-%d %H:%M:%S")
    delta = timedelta(minutes=1)
    # created empty timestamps list, iterates by every minute... this could take a while   
    timestamps = []
    current_time = start_datetime
    while current_time <= end_datetime:
        timestamps.append(current_time.strftime("%H:%M:%S"))
        current_time += delta
    
    return timestamps

# timezone identification 
tf = TimezoneFinder()

# file w/ updated cleaned latitude and longitude values
coordinates = pd.read_excel(r'EXCEL FILE')

eclipse_date = "2024-04-08"
start_time = "17:00:00"
end_time = "21:00:00"

hourly_times = hourly_timestamps(eclipse_date, start_time, end_time)

# empty list for maximum obscuration found over this iteration
max_obscuration_data = []
max_obscuration_ten_minutes_before_data = []

# iterating through each row in dataset w/ progress bar to track iterated calculations...
for index, row in tqdm(coordinates.iterrows(), total=coordinates.shape[0], desc = 'Processing coordinates'):
    latitude = row['LATITUDE (ASSISTED)']
    longitude = row['LONGITUDE (ASSISTED)']
    
    timezone_name = tf.timezone_at(lat=latitude, lng=longitude)
    
    if timezone_name:
        timezone = ZoneInfo(timezone_name)
        max_obscuration = 0.0
        max_obscuration_time = None
       
    
    # iterating through each time string in 'hourly stamps' function to calculate obscuration 
    for time_str in hourly_times:
            naive_dt = datetime.strptime(f"{eclipse_date} {time_str}", "%Y-%m-%d %H:%M:%S")
            local_dt = naive_dt.replace(tzinfo=timezone)
            obscuration = obscuration_algorithm_skyfield(latitude, longitude, local_dt)
        # if the obscuration is largest in evaluated row, set equal to max obscuration
            if obscuration > max_obscuration:
               max_obscuration = obscuration
               max_obscuration_time = local_dt
               
    max_obscuration_data.append(max_obscuration)
    
    if max_obscuration_time:
        ten_minutes_before_max_time = max_obscuration_time - timedelta(minutes=10)
        ten_minutes_before_obscuration = obscuration_algorithm_skyfield(latitude, longitude, ten_minutes_before_max_time)
        max_obscuration_ten_minutes_before_data.append(ten_minutes_before_obscuration)
    else:
        max_obscuration_ten_minutes_before_data.append(0.0)
else:
    max_obscuration_data.append(None)
    max_obscuration_ten_minutes_before_data.append(None)

max_obscuration_data = max_obscuration_data[:len(coordinates)]
max_obscuration_ten_minutes_before_data = max_obscuration_ten_minutes_before_data[:len(coordinates)]
coordinates['MAX_OBSCURATION'] = max_obscuration_data
coordinates['OBSCURATION 10 MINUTES BEFORE MAXIMUM'] = max_obscuration_ten_minutes_before_data
coordinates.to_excel('new_dataframe232.xlsx', index=False)
print(coordinates)

