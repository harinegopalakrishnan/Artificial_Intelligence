'''
Title:
Color Conversions and Cropping
Short description:
Convert an image from BGR to RGB and grayscale, then crop a region of interest.
'''

import cv2
import matplotlib.pyplot as plt

image = cv2.imread('flowers.jpg')

if image is None:
    print("Image not found!")
    exit()

# Convert BGR to RGB
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
plt.imshow(image_rgb)
plt.title("RGB Flowers")
plt.show()

# Convert to Grayscale
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
plt.imshow(gray_image, cmap='gray')
plt.title("Grayscaled Flowers")
plt.show()

# Cropping the image
# Assume we know the region we want: rows 50 to 250, columns 100 to 350
cropped_image = image[50:250, 100:400]
cropped_rgb = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB)
plt.imshow(cropped_rgb)
plt.title("Cropped Flowers")
plt.show()
