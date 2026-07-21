import cv2
import numpy as np

def apply_filter(image, ftype):
    """Apply a filter to the image based on the filter type."""
    img = image.copy()

    '''
    img[:, :, 1] = 0 means,
    : → Select all rows.
    : → Select all columns.
    1 → Select the Green channel (BGR format).
    = 0 → Set every Green pixel value to 0, removing the green color from the image.
    '''

    if ftype == "red_tint":
        # Set Green and Blue channels to 0, keeping only the Red channel.
        img[:, :, 1] = img[:, :, 0] = 0

    elif ftype == "green_tint":
        # Set Blue and Red channels to 0, keeping only the Green channel.
        img[:, :, 0] = img[:, :, 2] = 0

    elif ftype == "blue_tint":
        # Set Green and Red channels to 0, keeping only the Blue channel.
        img[:, :, 1] = img[:, :, 2] = 0

    elif ftype == "sobel":
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # Detect vertical edges. gray: Input image, cv2.CV_64F: Stores output as 64-bit float to preserve negative and large values, dx=1: Detect changes along x-axis, dy=0: No changes along y-axis, ksize=3: Uses a 3×3 Sobel kernel.
        sx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
        # Detect horizontal edges. gray: Input image, cv2.CV_64F: Stores output as 64-bit float to preserve negative and large values, dx=0: No changes along x-axis, dy=1: Detect changes along y-axis, ksize=3: Uses a 3×3 Sobel kernel.
        sy = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
        # Convert the Sobel results to uint8 and combine both edge images.
        sob = cv2.bitwise_or(sx.astype('uint8'), sy.astype('uint8'))
        img = cv2.cvtColor(sob, cv2.COLOR_GRAY2BGR)

    elif ftype == "canny":
        # Convert the image from BGR to Grayscale for Canny edge detection.
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # Detect edges using the Canny algorithm.
        # gray: Input grayscale image, 100: Lower threshold (weak edges), 200: Upper threshold (strong edges).
        can = cv2.Canny(gray, 100, 200)
        # Convert the grayscale edge image back to a BGR image for display.
        img = cv2.cvtColor(can, cv2.COLOR_GRAY2BGR)

    elif ftype == "cartoon":

        # Convert the image from BGR to Grayscale.
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # Remove small noise while preserving edges.
        # gray: Input image, 5: Kernel size for the median filter.
        gray = cv2.medianBlur(gray, 5)
        # Detect strong edges using adaptive thresholding.
        # gray: Input image, 255: Maximum pixel value, cv2.ADAPTIVE_THRESH_MEAN_C: Uses local mean,
        # cv2.THRESH_BINARY: Produces a black-and-white image, 9: Neighborhood size, 9: Constant subtracted from the mean.
        edges = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9
        )
        # Smooth the image while preserving edges.
        # image: Input image, 9: Pixel neighborhood diameter, 300: Color sigma, 300: Space sigma.
        color = cv2.bilateralFilter(image, 9, 300, 300)
        # Combine the smooth color image with the detected edges to create a cartoon effect.
        # color: Smoothed image, mask=edges: Edge mask used to keep only the cartoon outlines.
        img = cv2.bitwise_and(color, color, mask=edges)

    return img


def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        return
    ftype = "original"
    print("Keys: r=Red, g=Green, b=Blue, s=Sobel, c=Canny, t=Cartoon, q=Quit")
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Can't receive frame")
            break
        out = apply_filter(frame, ftype)
        cv2.imshow("Filter", out)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('r'):
            ftype = "red_tint"
        elif key == ord('g'):
            ftype = "green_tint"
        elif key == ord('b'):
            ftype = "blue_tint"
        elif key == ord('s'):
            ftype = "sobel"
        elif key == ord('c'):
            ftype = "canny"
        elif key == ord('t'):
            ftype = "cartoon"
        elif key == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()