import pandas as pd
import geopy as gp
from geopy.geocoders import Nominatim
from tqdm import tqdm 

location_data = pd.read_csv(r"C:\Users\bzwil\OneDrive\Desktop\OBSCURATION ALGORITHM\OBSCURATION-TOTALITY\clean dataset - 4_8_24 total solar eclipse.csv")
location_data_df = pd.DataFrame(location_data)

geolocator = Nominatim(user_agent="reverse_geocoding")

def retrieving_location(row):
    location = geolocator.reverse((row['LATITUDE'], row['LONGITUDE']), language='en')
    return location.__getstate__

tqdm.pandas()
location_data_df['LOCATION'] = location_data_df.progress_apply(retrieving_location, axis=1)

location_data_df.to_csv('new dataframe1', index=False)

print(location_data_df)


