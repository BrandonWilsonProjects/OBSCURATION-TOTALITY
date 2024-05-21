import ephem
import pandas as pd
import math
from datetime import datetime
from datetime import time
import matplotlib.pyplot as plt

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

coordinates = pd.read_csv(r"C:\Users\bzwil\OneDrive\Desktop\OBSCURATION ALGORITHM\OBSCURATION-TOTALITY\clean dataset - 4_8_24 total solar eclipse.csv")

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
    obscuration_1 = obscuration_algorithm(latitude, longitude, eclipse_date_1, eclipse_time_1)
    obscuration_data_1.append(obscuration_1)
    obscuration_2 = obscuration_algorithm(latitude, longitude, eclipse_date_1, eclipse_time_2)

# seting values to graph in the bar chart
low_obscuration_1 = [95]
high_obscuration_1 = [87 < obscuration_1 <= 95.0]

low_obscuration_2 = [70]
high_obscuration_2 = [60 < obscuration_2 <= 75]

# plotting the bar graph 
plt.bar(low_obscuration_1, high_obscuration_1, label='Obscuration 12 hrs into 4/8', color='r')
plt.bar(low_obscuration_2, high_obscuration_2, label='Obscuration 4 hrs into 4/8', color='c')

plt.xlabel('obscuration percentage')
plt.ylabel('quantity of respectively categorized obscuration values')
plt.title('Obscuration Comparison Graph')
plt.legend()
plt.show()


