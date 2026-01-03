import math
import time
from astro_pi_orbit import ISS

# (in km)
RADIUS_EARTH = 6371

# (in km/s)
SPIN_SPEED_EARTH_EQUATOR = (2 * math.pi * RADIUS_EARTH) / 86400


# converts degrees, minutes, seconds to degrees as a float
def dms_to_d(dms):
    sign, d, m, s = dms[0], dms[1], dms[2], dms[3]
    return sign * (d + m/60 + s/3600)

def angle_two_points_haversine(point1lat, point1long, point2lat, point2long):
    # put latitude in radians
    r_p1lat, r_p2lat = math.radians(point1lat), math.radians(point2lat)
    difference_lat = r_p2lat - r_p1lat
    
    # check for weird cases like going from -179 to 179
    difference_long_deg = ((point2long - point1long + 180) % 360) - 180
    difference_long = math.radians(difference_long_deg)
    
    # see haversine-working-out.png
    a = math.sin(difference_lat/2)**2 + math.cos(r_p1lat) * math.cos(r_p2lat) * math.sin(difference_long/2)**2
    theta = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    
    return theta


#######################################

def init_latlong(iss):
    c1 = iss.coordinates()
    c1_altitude = c1.elevation.km
    c1_long = dms_to_d( c1.longitude.signed_dms() ) # in degrees as a decimal
    c1_lat = dms_to_d( c1.latitude.signed_dms() )   # in degrees as a decimal
    
    return c1_lat, c1_long, c1_altitude

def final_latlong(iss):
    c2 = iss.coordinates()
    c2_altitude = c2.elevation.km
    c2_long = dms_to_d( c2.longitude.signed_dms() ) # in degrees as a decimal
    c2_lat = dms_to_d( c2.latitude.signed_dms() )   # in degrees as a decimal
    
    return c2_lat, c2_long, c2_altitude



def measure_latlong(t):
    iss = ISS()
    
    lat1, long1, altitude1 = init_latlong(iss)
    
    time.sleep(t)
    
    lat2, long2, altitude2 = final_latlong(iss)
    
    # using haversine formula, we get the central angle between the two points
    angle_radians_between = angle_two_points_haversine(lat1, long1, lat2, long2)

    # add the altitude of the ISS to the radius of the earth to get the real radius of the sphere of orbit
    average_altitude = (altitude1 + altitude2) / 2
    real_radius = RADIUS_EARTH + average_altitude

    # arc length = theta * R
    distance = angle_radians_between * real_radius

    velocity_kms = distance / t

    # earth spins same way as the ISS, and because latitude and longitude are earth-based,
    # the true velocity is slightly more than the difference between the two coordinates
    avg_latitude = (lat1 + lat2) / 2
    added_earth_velocity = SPIN_SPEED_EARTH_EQUATOR * math.cos(math.radians(avg_latitude))

    velocity_w_earth = velocity_kms + added_earth_velocity
    
    return velocity_w_earth