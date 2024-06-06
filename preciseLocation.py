import pandas as pd
import openpyxl
from geopy.exc import GeocoderTimedOut
from geopy.geocoders import Nominatim
from geopy.location import Location
from tqdm import tqdm
import time

# Load data
location_data = pd.read_excel(r'EXCEL FILE')
location_data_df = pd.DataFrame(location_data)

# Initialize geolocator
geolocator = Nominatim(user_agent="zipcode_to_coordinates")

# Function to retrieve location data for each zipcode
def retrieving_location(zipcode):
    try:
        location = geolocator.geocode(zipcode)
        if location:
            return location.latitude, location.longitude
        else:
            return (None, None)
    except GeocoderTimedOut:
        time.sleep(1)
        return retrieving_location(zipcode)

# Function to check if coordinates are in the US or Canada
def is_in_us_or_canada(latitude, longitude):
    try:
        location = geolocator.reverse((latitude, longitude), exactly_one=True)
        if location:
            address = location.raw['address']
            country_code = address.get('country_code', '').upper()
            return country_code in ['US', 'CA']
        else:
            return False
    except GeocoderTimedOut:
        time.sleep(1)
        return is_in_us_or_canada(latitude, longitude)

# Initialize lists for latitude and longitude
latitude = []
longitude = []

# Iterate over each zipcode in the DataFrame
for zipcode in tqdm(location_data_df['ZIPCODE'], desc='Processing Zip Codes'):
    lat, long = retrieving_location(zipcode)
    if lat is not None and long is not None and not is_in_us_or_canada(lat, long):
        lat, long = 0, 0
    latitude.append(lat)
    longitude.append(long)

# Add latitude and longitude to DataFrame
location_data_df['LATITUDE'] = latitude
location_data_df['LONGITUDE'] = longitude

# Save the updated DataFrame to a new Excel file
location_data_df.to_excel('new_dataframe5.xlsx', index=False)

# Print the updated DataFrame
print(location_data_df)