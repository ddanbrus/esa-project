# Must write a file named result.txt with result for ISS's velocity in km/s, up to 5 sig. fig.

from latlong import measure_latlong
from cam import measure_cam


####################################


t = 3
repeat = 10
threshold_for_discard = 1

latlong_values = []
cam_values = []

for i in range(repeat):
    print(i)
    velocity_from_latlong = measure_latlong(t)
    velocity_from_cam = measure_cam(t)
    
    print(i, ": got cam: ", velocity_from_cam, " and got latlong: ", velocity_from_latlong)
    
    if velocity_from_cam != None:
        if (velocity_from_cam > (velocity_from_latlong - threshold_for_discard)) and (velocity_from_cam < (velocity_from_latlong + threshold_for_discard)):
            cam_values.append(velocity_from_cam)
        
    if velocity_from_latlong != None:
        latlong_values.append(velocity_from_latlong)
    

avg_latlong = sum(latlong_values) / len(latlong_values)
avg_cam = sum(cam_values) / len(cam_values)

print("Final from latlong: ", avg_latlong)
print("Finabl from cam: ", avg_cam)

final_velocity = (avg_latlong + avg_cam) / 2
print("!final velocity! => ", final_velocity)

with open("result.txt", "w") as f:
    f.write(f"{final_velocity:.5g}")
