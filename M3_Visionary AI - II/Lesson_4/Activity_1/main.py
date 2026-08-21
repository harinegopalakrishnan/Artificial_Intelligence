'''
Title
Gesture-Based Volume and Brightness Control

Short description:
Students will build a real-time gesture control system that adjusts the system volume and screen brightness using hand gestures. By calculating the distance between the thumb and index finger, students will manipulate the volume and brightness on their computer in real-time.

Pre-Requisite:

Check python verion: python --version

Python version(3.10.8):

https://www.python.org/ftp/python/3.10.8/python-3.10.8-amd64.exe

Create a Virtual Environment

Windows:
py -3.10 -m venv ai310

Activate the Virtual Environment:
.\ai310\Scripts\activate


Install the required libraries:

python -m pip install mediapipe==0.10.5
python -m pip install opencv-python
python -m pip install numpy
python -m pip install pycaw
python -m pip install comtypes
python -m pip install screen-brightness-control
'''



import cv2, mediapipe as mp, numpy as np
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import screen_brightness_control as sbc

# Access MediaPipe's Hand Detection solution.
Hands = mp.solutions.hands
# Create a hand detector with 70% detection and tracking confidence.
hands = Hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
# Access the drawing utility to draw hand landmarks and connections.
draw = mp.solutions.drawing_utils
# Get the landmark IDs for the thumb tip and index finger tip.
TH, IX = Hands.HandLandmark.THUMB_TIP, Hands.HandLandmark.INDEX_FINGER_TIP

try:
    # Get the default audio output device.
    dev = AudioUtilities.GetDefaultOutputDevice() if hasattr(AudioUtilities, "GetDefaultOutputDevice") else AudioUtilities.GetSpeakers()
    # Gets access to control its volume..
    volctl = dev.EndpointVolume.QueryInterface(IAudioEndpointVolume)
    # Get the minimum and maximum system volume levels.
    minv, maxv = volctl.GetVolumeRange()[:2]
except Exception as e:
    # Show an error if volume control cannot be accessed.
    print(f"Pycaw error: {e}"); exit()

# Start the webcam.
cap = cv2.VideoCapture(0)

# Check if the webcam is accessible.
if not cap.isOpened(): print("Error: Webcam not accessible."); exit()

# Create a resizable window for the hand gesture control
WIN = "Hand Gesture Control"
cv2.namedWindow(WIN, cv2.WINDOW_NORMAL)

while True:
    # Capture a frame from the webcam.
    ok, img = cap.read()
    # Stop if the frame could not be captured.
    if not ok: 
        break
    # Flip the image horizontally to create a mirror view.
    img = cv2.flip(img, 1)
    # Get the height and width of the webcam frame.
    h, w = img.shape[:2]
    # Process the frame to detect hands.
    res = hands.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

    # Check if a hand and its handedness (Left or Right hand) are detected.
    if res.multi_hand_landmarks and res.multi_handedness:
        # Loop through each detected hand.
        for i, hand in enumerate(res.multi_hand_landmarks):
            # Get the handedness (whether the hand is Left or Right).
            label = res.multi_handedness[i].classification[0].label
            # Draw the hand landmarks (key points) and connections on the image.
            draw.draw_landmarks(img, hand, Hands.HAND_CONNECTIONS)
            # Store all the detected hand landmark positions.
            lm = hand.landmark
            # Get the pixel coordinates of the thumb tip.
            tp = (int(lm[TH].x*w), int(lm[TH].y*h))
            # Get the pixel coordinates of the index finger tip.
            ip = (int(lm[IX].x*w), int(lm[IX].y*h))
            # Draw a blue circle on the thumb and index finger tips.
            cv2.circle(img, tp, 10, (255,0,0), cv2.FILLED)
            cv2.circle(img, ip, 10, (255,0,0), cv2.FILLED)
            # Draw a green line between the thumb and index finger.
            cv2.line(img, tp, ip, (0,255,0), 3)
            # Calculate the distance between the thumb and index finger tips.
            dist = float(np.hypot(ip[0]-tp[0], ip[1]-tp[1]))

            # Check if the detected hand is the Left hand.
            if label == "Left":  # real RIGHT hand -> volume (frame is flipped)
                # Convert the finger distance into a system volume level.
                v = np.interp(dist, [30,300], [minv,maxv])
                # Try to set the computer's master volume.
                try:
                    volctl.SetMasterVolumeLevel(v, None)
                # Show an error message if the volume cannot be changed.
                except Exception as e:
                    print(f"Volume error: {e}")
                # Convert the finger distance into a position for the volume bar.
                bar = int(np.interp(dist, [30,300], [400,150]))
                # Convert the finger distance into a percentage from 0 to 100.
                pct = int(np.interp(dist, [30,300], [0,100]))
                
                # Draw the outline of the volume bar.
                cv2.rectangle(img, (50,150), (85,400), (255,0,0), 2)
                # Fill the volume bar according to the current volume.
                cv2.rectangle(img, (50,bar), (85,400), (255,0,0), cv2.FILLED)
                # Display the current volume percentage on the screen.
                cv2.putText(img, f"{pct}%", (40,450), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 3)

            # Check if the detected hand is the Right hand.
            elif label == "Right":  # real LEFT hand -> brightness
                # Convert the finger distance into a brightness percentage from 0 to 100.
                b = int(np.interp(dist, [30,300], [0,100]))
                # Try to set the computer screen brightness.
                try:
                    sbc.set_brightness(b)
                # Show an error message if the brightness cannot be changed.
                except Exception as e: 
                    print(f"Brightness error: {e}")
                # Convert the finger distance into a position for the brightness bar.
                bar = int(np.interp(dist, [30,300], [400,150]))
                # Set the left and right positions of the brightness bar.
                x1, x2 = w-85, w-50
                # Draw the outline of the brightness bar.
                cv2.rectangle(img, (x1,150), (x2,400), (0,255,0), 2)
                # Fill the brightness bar according to the current brightness.
                cv2.rectangle(img, (x1,bar), (x2,400), (0,255,0), cv2.FILLED)
                # Display the current brightness percentage on the screen.
                cv2.putText(img, f"{b}%", (w-110,450), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 3)

    # Display the webcam image in the window.
    cv2.imshow(WIN, img)
    # Wait for 1 millisecond and store the pressed key.
    k = cv2.waitKey(1) & 0xFF
    # Stop the program if the ESC key or 'q' key is pressed.
    if k in (27, ord("q")):
        break
    # Try to check whether the window is still open.
    try:
        # Stop the program if the window has been closed.
        if cv2.getWindowProperty(WIN, cv2.WND_PROP_VISIBLE) < 1:
            break
    # Handle an OpenCV error if the window is already closed.
    except cv2.error:
        break
# Release the webcam and stop using the camera.
cap.release()
# Close all OpenCV windows.
cv2.destroyAllWindows()