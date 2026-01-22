import os.path
if os.path.exists('Image Files/example1.jpeg'):
    TEST_LOCAL = True
else:
    TEST_LOCAL = False

from exif import Image
from datetime import datetime
if not TEST_LOCAL:
    from picamzero import Camera
import cv2
import math
import time

########## CONSTANTS ##########

DEFAULT_RES = (4056, 3040)

CROPPED_RES_X_START, CROPPED_RES_Y_START = 300, 100
CROPPED_RES_X_END, CROPPED_RES_Y_END = 4056-300, 3040-100

GSD_ISS_CM_PER_PIXEL = 12648

FAST_THRESHOLD, EDGE_THRESHOLD = 15, 0

################################

# def current_gsd(altitude):
    

def get_time(image):
    with open(image, 'rb') as image_file:
        img = Image(image_file)
        time_str = img.get("datetime_original")
        time = datetime.strptime(time_str, '%Y:%m:%d %H:%M:%S')
    return time

def get_time_difference(image_1, image_2):
    time_1 = get_time(image_1)
    time_2 = get_time(image_2)
    time_difference = time_2 - time_1

    return time_difference.seconds

def convert_to_cv(image_1, image_2):
    image_1_cv = cv2.imread(image_1, 0)
    image_2_cv = cv2.imread(image_2, 0)
    
    #crop images
    cropped_image_1 = image_1_cv[CROPPED_RES_Y_START:CROPPED_RES_Y_END, CROPPED_RES_X_START:CROPPED_RES_X_END]
    cropped_image_2 = image_2_cv[CROPPED_RES_Y_START:CROPPED_RES_Y_END, CROPPED_RES_X_START:CROPPED_RES_X_END]

    
    return cropped_image_1, cropped_image_2

def calculate_features(image_1, image_2, feature_number):
    orb = cv2.ORB_create(nfeatures = feature_number, fastThreshold=FAST_THRESHOLD, edgeThreshold=EDGE_THRESHOLD)
    keypoints_1, descriptors_1 = orb.detectAndCompute(image_1, None)
    keypoints_2, descriptors_2 = orb.detectAndCompute(image_2, None)
    return keypoints_1, keypoints_2, descriptors_1, descriptors_2

def calculate_matches(descriptors_1, descriptors_2):
    brute_force = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = brute_force.match(descriptors_1, descriptors_2)
    matches = sorted(matches, key=lambda x: x.distance)
    return matches

def display_matches(image_1_cv, keypoints_1, image_2_cv, keypoints_2, matches):
    match_img = cv2.drawMatches(image_1_cv, keypoints_1, image_2_cv, keypoints_2, matches[:100], None)
    resize = cv2.resize(match_img, (1600,600), interpolation = cv2.INTER_AREA)
    cv2.imshow('matches', resize)
    cv2.waitKey(0)
    cv2.destroyWindow('matches')
    
def find_matching_coordinates(keypoints_1, keypoints_2, matches):
    coordinates_1 = []
    coordinates_2 = []
    for match in matches:
        image_1_idx = match.queryIdx
        image_2_idx = match.trainIdx
        (x1,y1) = keypoints_1[image_1_idx].pt
        (x2,y2) = keypoints_2[image_2_idx].pt
        coordinates_1.append((x1,y1))
        coordinates_2.append((x2,y2))
    return coordinates_1, coordinates_2

def calculate_mean_distance(coordinates_1, coordinates_2):
    all_distances = 0
    merged_coordinates = list(zip(coordinates_1, coordinates_2))
    for coordinate in merged_coordinates:
        x_difference = coordinate[0][0] - coordinate[1][0]
        y_difference = coordinate[0][1] - coordinate[1][1]
        distance = math.hypot(x_difference, y_difference)
        all_distances = all_distances + distance
    return all_distances / len(merged_coordinates)

def calculate_speed_in_kmps(feature_distance, GSD, time_difference):
    distance = feature_distance * (GSD / 100000)
    speed = distance / time_difference
    return speed


#####################################

def measure_cam(t):
    photo1_filename = ''
    photo2_filename = ''
    time_difference = 0
    
    if TEST_LOCAL == False:
        camera = Camera()
        
#         time1 = time.time()
        photo1_filename = camera.take_photo('image_' + str(datetime.now().strftime("%H:%M:%S")) + '.jpg')
        
        time.sleep(t)
        
        photo2_filename = camera.take_photo('image_' + str(datetime.now().strftime("%H:%M:%S")) + '.jpg')
#         time2 = time.time()
        
#         time_difference = time2 - time1  # It will take longer than t to take the pictures so this is the real value
        time_difference = get_time_difference(photo1_filename, photo2_filename)
        
    else:
        photo1_filename = 'Image Files/example1.jpeg'
        photo2_filename = 'Image Files/example2.jpeg'
        time_difference = get_time_difference(photo1_filename, photo2_filename) # Get time difference between the example images

       
    image_1_cv, image_2_cv = convert_to_cv(photo1_filename, photo2_filename) # Create OpenCV image objects
    
    keypoints_1, keypoints_2, descriptors_1, descriptors_2 = calculate_features(image_1_cv, image_2_cv, 1000) # Get keypoints and descriptors
    
    matches = calculate_matches(descriptors_1, descriptors_2) # Match descriptors
    
    if TEST_LOCAL == True:
        display_matches(image_1_cv, keypoints_1, image_2_cv, keypoints_2, matches) # Display matches
        
    
    coordinates_1, coordinates_2 = find_matching_coordinates(keypoints_1, keypoints_2, matches)
    
    average_feature_distance = calculate_mean_distance(coordinates_1, coordinates_2)
    
    print("Average feature distance: ", average_feature_distance)
    print("Time difference: ", time_difference)
    
    speed = calculate_speed_in_kmps(average_feature_distance, GSD_ISS_CM_PER_PIXEL, time_difference)
    
    return speed
