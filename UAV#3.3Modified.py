import cv2
import numpy as np

# Read image:

# ***** in_file1 & in_file2 are the same text files just used for different applications, so put your input text file in both **********

# 1 for gray scale for character/shape detection
in_file1 = cv2.imread("C:\\Users\\saura\\Downloads\\colordetect.png.png")

# 1 for color detection
in_file2 = cv2.imread("C:\\Users\\saura\\Downloads\\colordetect.png.png")

out_file = "C:\\Users\\saura\\Downloads\\colordetect.out.txt"

# Convert image to grayscale
gray_image = cv2.cvtColor(in_file1, cv2.COLOR_BGR2GRAY)

# Use contours -> Character/shape detection

# Used fixed threshold and parameters from Stack Overflow
_, thresholded = cv2.threshold(gray_image, 128, 255, cv2.THRESH_BINARY)
contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Store detected character & shape
character = None
shape = None

# Loop through contours & classify -> character or shape
for con in contours:
    perimeter = cv2.arcLength(con, True)
    approx = cv2.approxPolyDP(con, 0.04 * perimeter, True)

    # If contour has 4 vertices -> shape
    if len(approx) == 4:
        shape = con
    else:
        character = con

# After detecting the character and shape, store their coordinates in variables

if character is not None:
    char_x, char_y, char_w, char_h = cv2.boundingRect(character)
else:
    char_x, char_y, char_w, char_h = -1, -1, -1, -1

if shape is not None:
    shape_x, shape_y, shape_w, shape_h = cv2.boundingRect(shape)
else:
    shape_x, shape_y, shape_w, shape_h = -1, -1, -1, -1

# Proceeded with color recognition based on the detected coordinates of the image below:

# Define dict of colors for mapping names to RGB
colors = {
    'green': (0, 128, 0),
    'blue': (0, 0, 255),
    'purple': (128, 0, 128),
    'black': (0, 0, 0),
    'gray': (128, 128, 128),
    'white': (255, 255, 255),
    'pink': (255, 192, 203),
    'red': (255, 0, 0),
    'orange': (255, 165, 0),
    'yellow': (255, 255, 0)
}

# Exception: Determine nearest color given RGB
def near_color(rgb_value):
    min_color = None
    min_distance = float('inf')

    for color, color_rgb in colors.items():

        distance = np.linalg.norm(np.array(color_rgb) - np.array(rgb_value))

        if distance < min_distance:
            min_distance = distance
            min_color = color

    return min_color

# Get regions of interest (ROI) from detected coordinates
char_roi = in_file2[char_y:char_y + char_h, char_x:char_x + char_w]
shape_roi = in_file2[shape_y:shape_y + shape_h, shape_x:shape_x + shape_w]

# Average color of the character & shape ROIs
char_avg_color = np.mean(char_roi, axis=(0, 1))
shape_avg_color = np.mean(shape_roi, axis=(0, 1))

# Determine the nearest color for character and shape using near_color method
character_color = near_color(char_avg_color)
shape_color = near_color(shape_avg_color)

# Print the recognized colors
print(f"Character color: {character_color}")
print(f"Shape color: {shape_color}")

# Write the output of character color and shape color to a text file
with open(out_file, "w") as file:
    # Write the recognized colors to the file
    file.write(f"{character_color}, {shape_color}\n")