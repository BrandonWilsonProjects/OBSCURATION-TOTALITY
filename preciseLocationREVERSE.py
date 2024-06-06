import pandas as pd
import openpyxl
import geopy as gp
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
from tqdm import tqdm
import time

# loading the cleaned latitude and longitude data and converting it to a data frame 
location_data = pd.read_excel(r'EXCEL FILE')
location_data_df = pd.DataFrame(location_data)

# activating nominatim class with a timeout
geolocator = Nominatim(user_agent="reverse_geocoding", timeout=10)

# function for retrieving location data for each latitude and longitude row in the data frame with retries
def retrieving_location(row, retries=3, delay=5):
    for _ in range(retries):
        try:
            location = geolocator.reverse((row['LATITUDE (ASSISTED)'], row['LONGITUDE (ASSISTED)']), language='en')
            if location:
                address = location.raw['address']
                if address.get('country_code') in ['ca', 'us']:
                    return location.__getstate__()
            return None
        except GeocoderTimedOut:
            time.sleep(delay)
    return None

# adding progress bars to the iteration 
tqdm.pandas()
location_data_df['LOCATION (ASSISTED)'] = location_data_df.progress_apply(retrieving_location, axis=1)

# creating a new excel file with updated location data
location_data_df.to_excel('new_dataframe1050.xlsx', index=False)
print(location_data_df)