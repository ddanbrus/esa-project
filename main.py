# Must write a file named result.txt with result for ISS's velocity in km/s, up to 5 sig. fig.

from latlong import measure_latlong
from cam import measure_cam


####################################


t = 0.2

velocity_from_latlong = measure_latlong(t)
velocity_from_cam = measure_cam(t)

print("From latlong: ", velocity_from_latlong)
print("From cam: ", velocity_from_cam)

final_velocity = (velocity_from_latlong + velocity_from_cam) / 2

with open("result.txt", "w") as f:
    f.write(f"{final_velocity:.5g}")
