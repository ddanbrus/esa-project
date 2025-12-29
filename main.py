# Must write a file named result.txt with result for ISS's velocity in km/s, up to 5 sig. fig.

from astro_pi_orbit import ISS
import time
import math

# (all in km)
LONGITUDE_DEGREES_PER_KM_EQUATOR = 111
LATITUDE_DEGREES_PER_KM = 111
RADIUS_EARTH = 6371
CIRCUMFERENCE_EARTH = 40075

# converts degrees, minutes, seconds to degrees as a float
def dms_to_d(dms):
    sign, d, m, s = dms[0], dms[1], dms[2], dms[3]
    return sign * (d + m/60 + s/3600)

# converts degrees of latitude into km which requires the latitude because longitude
# varies based on the latitude (equator -> 111km, poles -> ~0km)
def dlong_to_km(d_long, d_lat):
    km_per_degree = LONGITUDE_DEGREES_PER_KM_EQUATOR * math.cos(math.radians(d_lat))
    return d_long * km_per_degree

# the distance 1 degree of latitude represents stays more or less constant at around 111km
def dlat_to_km(d_lat):
    return d_lat * LATITUDE_DEGREES_PER_KM 

def difference_degrees(d1, d2):
    diff = abs(d2 - d1)
    diff = min(diff, 360 - diff)
    return diff

####################################


t = 10
iss = ISS()

c1 = iss.coordinates()
c1_altitude = c1.elevation.km
c1_long = dms_to_d( c1.longitude.signed_dms() ) # in degrees as a decimal
c1_lat = dms_to_d( c1.latitude.signed_dms() )   # in degrees as a decimal

time.sleep(t)

c2 = iss.coordinates()
c2_altitude = c2.elevation.km
c2_long = dms_to_d( c2.longitude.signed_dms() ) # in degrees as a decimal
c2_lat = dms_to_d( c2.latitude.signed_dms() )   # in degrees as a decimal

displacement_lon = difference_degrees(c1_long, c2_long)
displacement_lat = difference_degrees(c1_lat, c2_lat)
average_lat = (c1_lat + c2_lat) / 2
average_altitude = (c1_altitude + c2_altitude) / 2

# convert to kilometres
displacement_long_km = dlong_to_km(displacement_lon, average_lat)
displacement_lat_km = dlat_to_km(displacement_lat)

# total displacement = sqrt( (longitude displacement)^2 + (latitude displacement)^2 )
total_displacement_surface_km = math.sqrt(displacement_long_km**2 + displacement_lat_km**2)

# get theta as an angle using the circumference of the earth
theta = (total_displacement_surface_km / CIRCUMFERENCE_EARTH) * 360
# using the formula to find the length of an arc (theta/360 * 2PiR), we find the distance
# travelled accounting for altitude
total_displacement_in_altitude_km = (theta/360) * 2*math.pi*(RADIUS_EARTH + average_altitude)


velocity_kms = total_displacement_in_altitude_km  / t
print("velocity is ", velocity_kms, " km/s")


with open("result.txt", "w") as f:
    f.write(f"{velocity_kms:.5g}\n")
