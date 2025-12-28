# Must write a file named result.txt with result for ISS's velocity in km/s, up to 5 sig. fig.

from astro_pi_orbit import ISS
import time
import math

DEGREES_IN_KM_EQUATOR = 111
MINUTES_IN_KM_EQUATOR = DEGREES_IN_KM_EQUATOR / 60
SECONDS_IN_KM_EQUATOR = MINUTES_IN_KM_EQUATOR / 60

def difference_two_coordinates(coords1, coords2):
    diffDegrees = coords2[0]  - coords1[0]
    diffMinutes = coords2[1] - coords1[1]
    diffSeconds = coords2[2] - coords1[2]
    
    return [diffDegrees, diffMinutes, diffSeconds]    

# need latitude because distance of degrees varies depending on the latitude
# (eg. at equator, 1 degree is 111km; at pole, 1 degree is basically 0)
# Formula is:
# distance in km at certain latitude = km at equator * cos(degrees of latitude)
def convert_longitude_to_km_from_origin(delta_longitude, latitude):
    degreesLong, minutesLong, secondsLong = delta_longitude[0], delta_longitude[1], delta_longitude[2]
    degreesLat, minutesLat, secondsLat = latitude[0], latitude[1], latitude[2]
    
    km_per_degree = DEGREES_IN_KM_EQUATOR * math.cos(degreesLat)
    km_per_minute = km_per_degree / 60
    km_per_second = km_per_minute / 60
    
    km_from_origin = (degreesLong * km_per_degree) + (minutesLong * km_per_minute) + (secondsLong * km_per_second)
    
    return km_from_origin
    
# returns two lists (latitude, longitude) with the numbers appropriately negative
# depending on side of planet
def parse_coords(coords):
    coords_lat_sd = coords.latitude.signed_dms()
    coords_long_sd = coords.longitude.signed_dms()
    latitude = [coords_lat_sd[1] * coords_lat_sd[0], coords_lat_sd[2] * coords_lat_sd[0], coords_lat_sd[3]* coords_lat_sd[0]]
    longitude = [coords_long_sd[1] * coords_long_sd[0], coords_long_sd[2]* coords_long_sd[0], coords_long_sd[3] * coords_long_sd[0]]
    
    return latitude, longitude

####################################

t = 10

iss = ISS()
coords1 = iss.coordinates()
time.sleep(t)
coords2 = iss.coordinates()

coords1latitude, coords1longitude = parse_coords(coords1)
coords2latitude, coords2longitude = parse_coords(coords2)

print("Inital longitude: ", coords1longitude)
print("Final longitude: ", coords2longitude)

diff = difference_two_coordinates(coords1longitude, coords2longitude)
print("Difference is ", diff)

km_diff = convert_longitude_to_km_from_origin(diff, coords1latitude)
print("In km that is ", km_diff)

km_per_second = km_diff / t
print("So that is ", km_per_second, " kilometres per second")


