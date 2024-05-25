# This file aims to extract all maximum obscuration totality values for a given coordinate point. 
import ephem
import openpyxl
import pandas as pd
import math
from datetime import datetime
from datetime import timedelta
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

# created start and end timestamps for solar eclipse date
def hourly_timestamps(start_date, start_time, end_time):
    start_datetime = datetime.strptime(f"{start_date} {start_time}", "%Y-%m-%d %H:%M:%S")
    end_datetime = datetime.strptime(f"{start_date} {end_time}", "%Y-%m-%d %H:%M:%S")
    delta = timedelta(hours=1)
    # created empty timestamps list, iterates by one hour...  
    timestamps = []
    current_time = start_datetime
    while current_time <= end_datetime:
        timestamps.append(current_time.strftime("%H:%M:%S"))
        current_time += delta
    
    return timestamps

# file w/ updated cleaned latitude and longitude values
coordinates = pd.read_csv(r'CSV FILE')

eclipse_date = "2024-04-08"
start_time = "00:00:00"
end_time = "23:59:59"

hourly_times = hourly_timestamps(eclipse_date, start_time, end_time)

# empty list for maximum obscuration found over this iteration
max_obscuration_data = []

# iterating through each row in dataset
for index, row in coordinates.iterrows():
    latitude = row['LATITUDE']
    longitude = row['LONGITUDE']
    
    # initializing maximum obscuration
    max_obscuration = 0.0
    
    # iterating through each time string in 'hourly stamps' function to calculate obscuration 
    for time_str in hourly_times:
        obscuration = obscuration_algorithm(latitude, longitude, eclipse_date, time_str)
        # if the obscuration is largest in evaluated row, set equal to max obscuration
        if obscuration > max_obscuration:
            max_obscuration = obscuration
    
    # to the empty list, append every max obscuration retrieved 
    max_obscuration_data.append(max_obscuration)
    
# add to data frame
coordinates['MAX_OBSCURATION'] = max_obscuration_data
coordinates.to_excel('new dataframe101.xlsx', index=False)
print(coordinates)

