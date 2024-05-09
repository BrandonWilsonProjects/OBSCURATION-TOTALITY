import ephem

def compute_obscuration_totality(latitude, longitude, date_time):
    obs = ephem.Observer()
    obs.lat = str(latitude)
    obs.lon = str(longitude)

    # Set the date and time
    obs.date = date_time

    # Compute the sun's position
    sun = ephem.Sun(obs)
    sun.compute(obs)

    # Find the next solar eclipse
    eclipse = ephem.(obs)

    # If there is no eclipse, return 0
    if not eclipse:
        return 0.0

    # Check if the time falls within the eclipse period
    if eclipse[0] <= obs.date <= eclipse[4]:
        # Compute the obscuration
        obscuration = 1.0 - 10 ** (-0.4 * eclipse[6])
        return obscuration

    return 0.0

latitude = 31.55191
longitude = -84.53428
date_time = '2024/4/8 19:00:00'

obscuration_totality = compute_obscuration_totality(latitude, longitude, date_time)
print("Obscuration of totality on April 8th, 2024 at 7:00 p.m.:", obscuration_totality)