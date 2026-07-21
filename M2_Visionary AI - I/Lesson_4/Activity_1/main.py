'''
Title
Interactive Edge Detection & Filtering
Short description:
Explore edge detection techniques (Sobel, Canny, Laplacian) and apply noise reduction filters (Gaussian, Median) interactively. Students will experiment with parameters and observe their effects on real images.

'''

import cv2
import numpy as np
import matplotlib.pyplot as plt

# Define a function to display an image with a title.
# title is the heading displayed above the image.
# image is the image to be displayed.
def display_image(title, image):

    # Create a figure of size 8 x 8 inches.
    plt.figure(figsize=(8, 8))

    # Check if the image is grayscale.
    # A grayscale image has only 2 dimensions (height, width).
    if len(image.shape) == 2:
        plt.imshow(image, cmap='gray')   # Display grayscale image.

    # Otherwise, the image is a color image.
    # Convert BGR to RGB before displaying with Matplotlib.
    else:
        plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

    # Display the title above the image.
    plt.title(title)

    # Hide the x-axis and y-axis.
    plt.axis('off')

    # Display the image.
    plt.show()


def interactive_edge_detection(image_path):
    """Interactive activity for edge detection and filtering."""
    image = cv2.imread(image_path)
    if image is None:
        print("Error: Image not found!")
        return

    # Convert to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    display_image("Original Grayscale Image", gray_image)

    print("Select an option:")
    print("1. Sobel Edge Detection")
    print("2. Canny Edge Detection")
    print("3. Laplacian Edge Detection")
    print("4. Gaussian Smoothing")
    print("5. Median Filtering")
    print("6. Exit")

    while True:
        choice = input("Enter your choice (1-6): ")

        if choice == "1":
            # Sobel Edge Detection

            #dx = Direction along the X-axis (left ↔ right), dy = Direction along the Y-axis (top ↕ bottom)
            # Detects vertical edges in the grayscale image using a 3×3 Sobel filter (dx=1, dy=0) and stores the result as a 64-bit floating-point image.
            sobel_x = cv2.Sobel(gray_image, cv2.CV_64F, 1, 0, ksize=3)
            # Detects horizontal edges in the grayscale image using a 3×3 Sobel filter (dx=0, dy=1) and stores the result as a 64-bit floating-point image.
            sobel_y = cv2.Sobel(gray_image, cv2.CV_64F, 0, 1, ksize=3)
            # Converts both edge images to 8-bit format (0–255) and combines them into a single edge image using a bitwise OR operation.
            combined_sobel = cv2.bitwise_or(sobel_x.astype(np.uint8), sobel_y.astype(np.uint8))
            display_image("Sobel Edge Detection", combined_sobel)

        elif choice == "2":
            # Canny Edge Detection
            #Think of an edge as a place where the pixel intensity changes suddenly.
            print("Adjust thresholds for Canny (default: 100 and 200)")
            lower_thresh = int(input("Enter Lower threshold: "))
            upper_thresh = int(input("Enter Upper threshold: "))
            # Detect edges in the grayscale image using the Canny Edge Detection algorithm.
            # gray_image is the input image, lower_thresh removes weak edges, and upper_thresh detects strong edges.
            edges = cv2.Canny(gray_image, lower_thresh, upper_thresh)
            display_image("Canny Edge Detection", edges)

        elif choice == "3":
            # Laplacian Edge Detection
            # Detect all edges (horizontal, vertical, and diagonal) in the grayscale image and store the result as a 64-bit floating-point image.
            laplacian = cv2.Laplacian(gray_image, cv2.CV_64F)
            # Convert negative edge values to positive using abs, change the image to 8-bit format (0–255), and display the Laplacian edge-detected image.
            display_image("Laplacian Edge Detection", np.abs(laplacian).astype(np.uint8))

        elif choice == "4":
            # Gaussian Smoothing
            print("Adjust kernel size for Gaussian blur (must be odd, default: 5)")
            kernel_size = int(input("Enter kernel size (odd number): "))
            # (kernel_size, kernel_size) specifies the size of the Gaussian filter (e.g., 3×3, 5×5, 7×7).
            # 0 tells OpenCV to automatically calculate the blur strength (sigma).
            blurred = cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)
            display_image("Gaussian Smoothed Image", blurred)

        elif choice == "5":
            # Median Filtering
            print("Adjust kernel size for Median filtering (must be odd, default: 5)")
            kernel_size = int(input("Enter kernel size (odd number): "))
            # kernel_size specifies the size of the filter (must be an odd number like 3, 5, or 7).
            median_filtered = cv2.medianBlur(image, kernel_size)
            display_image("Median Filtered Image", median_filtered)

        elif choice == "6":
            # Exit
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please select a number between 1 and 6.")


# Provide the path to an image for the activity
interactive_edge_detection('flowers.jpg')