'''
Title
Face detection with open CV

Short description:
This activity will guide students through accessing their computer’s camera and performing real-time face detection using OpenCV’s pre-trained Haar Cascade classifier.

OpenCV: pip install opencv-python
NumPy: pip install numpy
Keras/TensorFlow (for emotion detection model): pip install keras tensorflow
Matplotlib (optional for visualizing emotion predictions): pip install matplotlib
'''

import cv2

# Load the pre-trained Haar Cascade Classifier for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Start video capture from the default webcam (0)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

while True:

    # Capture frame-by-frame
    ret, frame = cap.read()

    # If frame is read correctly, ret will be True
    if not ret:
        print("Error: Failed to capture image")
        break

    # Convert frame to grayscale (Face detection works better on grayscale)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the grayscale image
    
    # gray: Grayscale image used for face detection. scaleFactor=1.1: Reduces the image size by 10% at each step to detect faces of different sizes.
    # minNeighbors=5: Accepts a face only if at least 5 nearby detections agree. minSize=(30,30): Ignores objects smaller than 30 × 30 pixels.
    
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Draw rectangles around the faces
    # Loop through each detected face. x and y are the top-left coordinates, while w and h are the width and height of the face.
    
    for (x, y, w, h) in faces:
        # Draw a blue rectangle on the original frame around each detected face.
        # frame: Image to draw on, (x,y): Top-left corner, (x+w,y+h): Bottom-right corner,
        # (255,0,0): Blue color (BGR), 2: Rectangle border thickness
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)  # Blue rectangle with thickness 2

    # Display the resulting frame
    cv2.imshow('Face Detection - Press q to Quit', frame)

    # Break the loop when the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture and close any open windows
cap.release()
cv2.destroyAllWindows()

