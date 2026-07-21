'''
Title
Real-Time Face Tracking and Counting People
Short description:
Students will implement real-time face tracking and counting using their webcam. They will detect faces, count the number of people in the frame, and display the count dynamically.

Pre-Requisite:
1)OpenCV Library
2)Python 3.10 version
'''


import cv2

# Load pre-trained Haar Cascade Classifier for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Initialize video capture (use webcam)
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to capture image")
        break

    # Convert frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the grayscale image.
    # gray: Grayscale image for face detection. scaleFactor=1.1: Reduces the image by 10% at each step to detect faces of different sizes.
    # minNeighbors=5: Accept a face only if at least 5 nearby detections agree. minSize=(30,30): Ignore objects smaller than 30×30 pixels.
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Loop through each detected face. x and y are the top-left coordinates, while w and h are the width and height of the face.
    for (x, y, w, h) in faces:
        # Draw a blue rectangle around each detected face.
        # frame: Image to draw on, (x,y): Top-left corner, (x+w,y+h): Bottom-right corner,
        # (255,0,0): Blue color (BGR), 2: Rectangle thickness in pixels.
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

    # Select the font style used to display text on the image.
    font = cv2.FONT_HERSHEY_SIMPLEX

    # Select the font style used to display text on the image.
    font = cv2.FONT_HERSHEY_SIMPLEX

    # Display the number of detected faces on the video frame.
    # frame: Image to display text on, f'People Count: {len(faces)}': Text to display,
    # (10,30): Text position, font: Font style, 1: Font size,
    # (255,0,0): Blue text color (BGR), 2: Text thickness, cv2.LINE_AA: Smooth text edges.
    cv2.putText(frame, f'People Count: {len(faces)}', (10, 30), font, 1, (255, 0, 0), 2, cv2.LINE_AA)

    # Display the frame with face detection and people count
    cv2.imshow('Face Tracking and Counting', frame)

    # Exit the loop when the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close the window
cap.release()
cv2.destroyAllWindows()