import numpy as np

# ****REPLACE WITH YOUR IN AND OUT TEXT FILES ******
in_file = "C:\\Users\\saura\\Downloads\\pinpoint.in.txt"
out_file = "C:\\Users\\saura\\Downloads\\pinpoint.out10.txt"

# Initialize file line to read
line = 0

# Read contents of file
with open(in_file, "r") as file:
    line = line + 1
    data = file.readline()
    altitude, x, y, N = map(float, data.split())
    pixel_coordinates = [list(map(int, line.split())) for line in file.readlines()]

# Constants used in calculations below:

# Field of Views (In Degrees)
horizontal_fov = 23.4
vertical_fov = 15.6

# Lengths
width_img = 5472
height_img = 3648

# Store the GPS coordinates of the spaced out objects
coordinate_list = []

# GPS coordinates
drone_long = x
drone_lat = y

# Calculate GPS coordinates for each object
for x, y in pixel_coordinates:

    # Object's relative position (meters) in relation to center of image
    x_change = (x - width_img / 2) / width_img * (2 * altitude * np.tan(np.radians(horizontal_fov / 2)))
    y_change = (y - height_img / 2) / height_img * (2 * altitude * np.tan(np.radians(vertical_fov / 2)))

    # Object's GPS coordinates below:

    object_latitude = drone_lat + (y_change / 111111)
    # 1 degree of long ≈ 111111 meters

    object_longitude = drone_long + (x_change / (111111 * np.cos(np.radians(drone_lat))))
    # 1 degree of lat ≈ 111111 meters

    # Adding coordinates into coordinate list
    coordinate_list.append((object_longitude, object_latitude))

# Write the output of (Longitude, Latitude) to the file
with open(out_file, "w") as file:
    for lon, lat in coordinate_list:
        file.write(f"{lon:.4f} {lat:.4f}\n")
