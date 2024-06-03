# This file identifies the proximal location of coordinate points in a excel file. (REVERSE)
import pandas as pd
import openpyxl
import geopy as gp
from geopy.geocoders import Nominatim
from tqdm import tqdm 

# loading the cleaned latitude and longitude data and convering it to a data frame 
location_data = pd.read_excel(r'EXCEL FILE')
location_data_df = pd.DataFrame(location_data)

# activating nominatim class...
geolocator = Nominatim(user_agent="reverse_geocoding")

# function for retrieving location data for each latitude and longitude row in the data frame
def retrieving_location(row):
    location = geolocator.reverse((row['LATITUDE'], row['LONGITUDE']), language='en')
    if location:
        address = location.raw['address']
        if address.get('country_code') in ['ca', 'us']:
            return location.__getstate__
    return None

# adding progress bars to the iteration 
tqdm.pandas()
location_data_df['LOCATION'] = location_data_df.progress_apply(retrieving_location, axis=1)

# creating a new csv file with updated location data
location_data_df.to_excel('new dataframe202.xlsx', index=False)
print(location_data_df)


