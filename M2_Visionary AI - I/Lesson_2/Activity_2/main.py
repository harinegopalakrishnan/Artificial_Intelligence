'''
Title:
Rotating and Adjusting Image Brightness
Short description:
Rotate an image by 45 degrees and adjust its brightness to see the effects of basic arithmetic operations on images.
'''

import cv2
import numpy as np
import matplotlib.pyplot as plt

image = cv2.imread('flowers.jpg')
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Rotate the image by 45 degrees around its center

# Get the height (h) and width (w) of the image.
# image.shape returns (height, width, channels).
# [:2] extracts only the height and width.
(h, w) = image.shape[:2]

# Calculate the center point of the image.
# w//2 gives the center width.
# h//2 gives the center height.
center = (w//2, h//2)

# Create a rotation matrix.
# Rotate the image by 45 degrees around the center.
# Scale factor 1.0 keeps the image at its original size.
M = cv2.getRotationMatrix2D(center, 45, 1.0)

# Apply the rotation to the image.
# image is the input image.
# M contains the rotation information.
# (w, h) keeps the output image size the same.
rotated = cv2.warpAffine(image, M, (w, h))

rotated_rgb_image = cv2.cvtColor(rotated, cv2.COLOR_BGR2RGB)
plt.imshow(rotated_rgb_image)
plt.title("Rotated rgb Image")
plt.show()

# Increase brightness by adding 50 to all pixel values.
# np.ones() creates a matrix of 1's with the same size as the image.
# Multiplying by 50 makes every value in the matrix equal to 50.
brightness_matrix = np.ones(image.shape, dtype="uint8") * 50

# Increase the brightness of the image.
# cv2.add() adds the brightness matrix to every pixel.
# It prevents pixel values from exceeding 255 (overflow).
brighter = cv2.add(image, brightness_matrix)

brighter_rgb = cv2.cvtColor(brighter, cv2.COLOR_BGR2RGB)
plt.imshow(brighter_rgb)
plt.title("Brighter Image")
plt.show()
