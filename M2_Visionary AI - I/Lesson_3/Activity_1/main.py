'''
Title
Image Annotation with Shapes and Measurements

Short description:
This activity involves annotating an image using OpenCV by drawing rectangles and circles to highlight regions of interest, connecting them with a line, and visualizing the image height using bi-directional arrows. Text annotations are added for clarity, making the image informative and visually structured.
'''

import cv2
import matplotlib.pyplot as plt

# Step 1: Load the Image
image_path = 'animals.jpg'  # User-provided image path
image = cv2.imread(image_path)


# Convert BGR to RGB for correct color display with matplotlib
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Get image dimensions

# Get the dimensions of the image.
# image_rgb.shape returns (height, width, channels).
# height stores the number of rows, width stores the number of columns.
# _ stores the number of color channels (3 for an RGB image) but is ignored.
height, width, _ = image_rgb.shape

# Step 2: Draw Two Rectangles Around Interesting Regions
# Rectangle 1: Top-left corner

# Set the width and height of the first rectangle.
# The rectangle will be 150 pixels wide and 150 pixels high.
rect1_width, rect1_height = 150, 150

# Specify the top-left corner of the rectangle.
# (20, 20) means the rectangle starts 20 pixels from the left and 20 pixels from the top.
top_left1 = (20, 20)

# Calculate the bottom-right corner of the rectangle.
# It is obtained by adding the rectangle's width and height to the top-left coordinates.
bottom_right1 = (top_left1[0] + rect1_width, top_left1[1] + rect1_height)

# Draw the rectangle on the image.
# (0, 255, 255) specifies the rectangle color (Yellow in RGB).
# 3 specifies the thickness of the rectangle border.
cv2.rectangle(image_rgb, top_left1, bottom_right1, (0, 255, 255), 3)


# Set the width and height of the second rectangle.
# The rectangle will be 200 pixels wide and 150 pixels high.
rect2_width, rect2_height = 200, 150

# Calculate the top-left corner of the rectangle.
# The rectangle is placed 20 pixels away from the bottom and right edges of the image.
top_left2 = (width - rect2_width - 20, height - rect2_height - 20)

# Calculate the bottom-right corner of the rectangle.
# It is obtained by adding the rectangle's width and height to the top-left coordinates.
bottom_right2 = (top_left2[0] + rect2_width, top_left2[1] + rect2_height)

# Draw the second rectangle on the image.
# (255, 0, 255) specifies the rectangle color (Magenta in RGB).
# 3 specifies the thickness of the rectangle border.
cv2.rectangle(image_rgb, top_left2, bottom_right2, (255, 0, 255), 3)


# Step 3: Draw Circles at the Centers of Both Rectangles
center1_x = top_left1[0] + rect1_width // 2
center1_y = top_left1[1] + rect1_height // 2
center2_x = top_left2[0] + rect2_width // 2
center2_y = top_left2[1] + rect2_height // 2

# Draw a filled circle at the center of the first rectangle.
# (center1_x, center1_y) specifies the center of the circle.
# 15 is the radius of the circle.
# (0, 255, 0) is the color Green and -1 fills the circle.
cv2.circle(image_rgb, (center1_x, center1_y), 15, (0, 255, 0), -1)

# Draw a filled circle at the center of the second rectangle.
# (center2_x, center2_y) specifies the center of the circle.
# 15 is the radius of the circle.
# (0, 255, 0) is the color Green and -1 fills the circle.
cv2.circle(image_rgb, (center2_x, center2_y), 15, (0, 255, 0), -1)

# Step 4: Draw Connecting Lines Between Centers of Rectangles
cv2.line(image_rgb, (center1_x, center1_y), (center2_x, center2_y), (0, 255, 0), 3)

# Syntax:
# cv2.putText(image, text, position, font, fontScale, color, thickness, lineType)
# image      -> Image on which the text is displayed.
# text       -> Text to be displayed.
# position   -> Starting (x, y) coordinates of the text.
# font       -> Font style of the text.
# fontScale  -> Size of the text.
# color      -> Color of the text (RGB).
# thickness  -> Thickness of the text.
# lineType   -> Style of the text edges (LINE_AA = smooth edges).

# Select the font style for the text.
font = cv2.FONT_HERSHEY_SIMPLEX

# Add the label "Region 1" above the first rectangle.
cv2.putText(image_rgb, 'Region 1', (top_left1[0], top_left1[1] - 10),font, 0.7, (255, 255, 255), 2, cv2.LINE_AA)

# Add the label "Region 2" above the second rectangle.
cv2.putText(image_rgb, 'Region 2', (top_left2[0], top_left2[1] - 10),font, 0.7, (255, 255, 255), 2, cv2.LINE_AA)

# Add the label "Center 1" below the first circle.
cv2.putText(image_rgb, 'Center 1', (center1_x - 40, center1_y + 40),font, 0.6, (0, 255, 0), 2, cv2.LINE_AA)

# Add the label "Center 2" below the second circle.
cv2.putText(image_rgb, 'Center 2', (center2_x - 40, center2_y + 40),font, 0.6, (0, 255, 0), 2, cv2.LINE_AA)

# Step 6: Add Bi-Directional Arrow Representing Height
arrow_start = (width - 50, 20)  # Start near the top-right
arrow_end = (width - 50, height - 20)  # End near the bottom-right

# Syntax:
# cv2.arrowedLine(image, start_point, end_point, color, thickness, tipLength)
# image      -> Image on which the arrow is drawn.
# start_point-> Starting (x, y) coordinates of the arrow.
# end_point  -> Ending (x, y) coordinates of the arrow.
# color      -> Color of the arrow (RGB).
# thickness  -> Thickness of the arrow line.
# tipLength  -> Size of the arrow head.

# Draw a downward arrow from the top to the bottom.
# The arrow is drawn in Cyan with a thickness of 3 pixels.
# tipLength=0.05 sets the size of the arrow head.
cv2.arrowedLine(image_rgb, arrow_start, arrow_end,(255, 255, 0), 3, tipLength=0.05)

# Draw an upward arrow from the bottom to the top.
# This creates a bi-directional arrow representing the image height.
# The arrow uses the same color, thickness, and arrow head size.
cv2.arrowedLine(image_rgb, arrow_end, arrow_start,(255, 255, 0), 3, tipLength=0.05)

# Calculate the position to display the height label.
# The text is placed 150 pixels to the left of the arrow.
# The y-coordinate is the midpoint between the start and end of the arrow.
height_label_position = (arrow_start[0] - 150, (arrow_start[1] + arrow_end[1]) // 2)

# Display the height value on the image.
# f'Height: {height}px' inserts the image height into the text.
# The text is displayed in Cyan with a font size of 0.8 and thickness of 2.
cv2.putText(image_rgb, f'Height: {height}px', height_label_position, font, 0.8,(255, 255, 0), 2, cv2.LINE_AA)

# Step 7: Display the Annotated Image
plt.figure(figsize=(12, 8))
plt.imshow(image_rgb)
plt.title('Annotated Image with Regions, Centers, and Bi-Directional Height Arrow')
plt.axis('off')
plt.show()

