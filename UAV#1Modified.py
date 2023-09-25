import numpy as np

# ****REPLACE WITH YOUR IN AND OUT TEXT FILES ******
in_file = "C:\\Users\\saura\\Downloads\\box.in.txt"
out_file = "C:\\Users\\saura\\Downloads\\box.out.txt"

def compute_convex_hull(points):
    hull = []

    # Logic: Use the gift wrapping algorithm (from Stack Overflow) to calculate convex hull of given points

    # Find lowest (leftmost) y-coordinate point
    start = min(points, key=lambda point: (point[1], point[0]))
    hull.append(start)

    while True:
        current = hull[-1]
        next_point = points[0]

        for p in points:
            if p == current:
                continue

            # Calculate current angle
            angle = np.degrees(np.arctan2(current[1] - start[1], current[0] - start[0]))

            angle_next = np.degrees(np.arctan2(p[1] - start[1], p[0] - start[0]))

            # Condition if same angle measure
            if angle_next < angle or (
                    angle_next == angle and np.linalg.norm(np.array(p) - np.array(start)) > np.linalg.norm(
                    np.array(next_point) - np.array(start))):
                next_point = p

        # Break if reached start of loop
        if next_point == start:
            break

        hull.append(next_point)

    return hull

# Read points from the file
with open(in_file, 'r') as file:
    lines = file.readlines()
    N = int(lines[0])
    points = [tuple(map(int, line.strip().split())) for line in lines[1:]]

# Calculate convex hull
convex_hull = compute_convex_hull(points)

# Find angle of convex hull
angle = np.degrees(np.arctan2(convex_hull[0][1] - convex_hull[-1][1], convex_hull[0][0] - convex_hull[-1][0]))

# Find dimensions of bounded box
min_x = min(point[0] for point in convex_hull)
max_x = max(point[0] for point in convex_hull)
min_y = min(point[1] for point in convex_hull)
max_y = max(point[1] for point in convex_hull)
width = max_x - min_x
height = max_y - min_y

# Calculate area of bounded box
area = round(abs(width * height), 2)

# Write the area of bounded box & angle of orientation in the specified format to a text file
with open(out_file, "w") as file:
    file.write(f"{angle:.2f} {area:.2f}")
