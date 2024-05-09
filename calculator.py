import ephem

def compute_obscuration_totality(latitude, longitude):
    obs = ephem.Observer()
    obs.lat = str(latitude)
    obs.lon = str(longitude)

    sun = ephem.Sun()

    # Set the date to April 8th, 2024
    obs.date = '2024/4/8'

    # Compute the details of the eclipse
    eclipse_details = obs.previous_transit(sun)

    # Compute the obscuration
    obscuration = 1.0 - 10 ** (-0.4 * eclipse_details.imag)

    return obscuration

latitude = 31.55191
longitude = -84.53428

obscuration_totality = compute_obscuration_totality(latitude, longitude)
print("Obscuration of totality on April 8th, 2024:", obscuration_totality)