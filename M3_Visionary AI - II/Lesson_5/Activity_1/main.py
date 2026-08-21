'''
Title
Gesture-Based Scrolling Control
Short description:
Students will build a gesture-controlled scroll system that detects hand gestures in real-time and controls the system’s scrolling behavior based on whether the hand is open or closed.

Pre-Requisite:

Check python verion: python --version

Python version(3.10.8):

https://www.python.org/ftp/python/3.10.8/python-3.10.8-amd64.exe

Create a Virtual Environment

Windows:
py -3.10 -m venv ai310

Activate the Virtual Environment:
.\ai310\Scripts\activatee


Install the required libraries:
pip install pyautogui
'''



import cv2, time, pyautogui
import mediapipe as mp

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

# Configurations
SCROLL_SPEED = 300
SCROLL_DELAY = 1
CAM_WIDTH, CAM_HEIGHT = 640, 480

def detect_gesture(landmarks, handedness):
    
    # Create a list to store the fingers that are raised.
    fingers = []

    # Store the landmark positions of the four fingertips (excluding the thumb).
    tips = [mp_hands.HandLandmark.INDEX_FINGER_TIP, mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
            mp_hands.HandLandmark.RING_FINGER_TIP, mp_hands.HandLandmark.PINKY_TIP]
   
    # Check whether each finger (except the thumb) is raised.
    for tip in tips:
        # Compare the fingertip with its lower joint.
        if landmarks.landmark[tip].y < landmarks.landmark[tip - 2].y:
            # Add the finger to the list if it is raised.
            fingers.append(1)

    # Get the thumb tip and thumb joint positions.
    thumb_tip = landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    thumb_ip = landmarks.landmark[mp_hands.HandLandmark.THUMB_IP]
    # Check whether the thumb is raised based on the hand (Left/Right).

    if (handedness == "Right" and thumb_tip.x > thumb_ip.x) or (handedness == "Left" and thumb_tip.x < thumb_ip.x):
        # Add the thumb to the list if it is raised.
        fingers.append(1)
    # Return the gesture based on the number of raised fingers.
    return "scroll_up" if sum(fingers) == 5 else "scroll_down" if len(fingers) == 0 else "none"

# Open the default webcam.
cap = cv2.VideoCapture(0)
# Set the webcam frame width.
cap.set(3, CAM_WIDTH)
# Set the webcam frame height.
cap.set(4, CAM_HEIGHT)
# Initialize the scroll timer and previous frame time.
last_scroll = p_time = 0
# Display the gesture controls and exit key in the console.
print("Gesture Scroll Control Active\nOpen palm: Scroll Up\nFist: Scroll Down\nPress 'q' to exit")

while cap.isOpened():
    success, img = cap.read()
    if not success: break

    # Convert to RGB and mirror the image.
    img = cv2.flip(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), 1)
    # Detect hands in the frame.
    results = hands.process(img)
    # Initialize gesture and handedness.
    gesture, handedness = "none", "Unknown"
   
    if results.multi_hand_landmarks:
        # Iterate through all detected hands and identify whether each is a left or right hand.
        for hand, handedness_info in zip(results.multi_hand_landmarks, results.multi_handedness):
            # Get whether the detected hand is Left or Right.
            handedness = handedness_info.classification[0].label
            # Identify the hand gesture (Open Palm, Fist, or None).
            gesture = detect_gesture(hand, handedness)
            # Draw the hand landmarks and connections on the webcam frame.
            mp_drawing.draw_landmarks(img, hand, mp_hands.HAND_CONNECTIONS)

            # Check if enough time has passed since the last scroll action.
            if (time.time() - last_scroll) > SCROLL_DELAY:
                # Scroll up if an open palm is detected.
                if gesture == "scroll_up": pyautogui.scroll(SCROLL_SPEED)
                # Scroll down if a closed fist is detected.
                elif gesture == "scroll_down": pyautogui.scroll(-SCROLL_SPEED)
                # Update the time of the last scroll action.
                last_scroll = time.time()

    # Calculate the Frames Per Second (FPS).
    fps = 1/(time.time()-p_time) if (time.time()-p_time) > 0 else 0
    # Store the current time for the next FPS calculation.
    p_time = time.time()
    # Display the FPS, detected hand, and gesture on the webcam frame.
    cv2.putText(img, f"FPS: {int(fps)} | Hand: {handedness} | Gesture: {gesture}", (10,30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,0,0), 2)
    # Show the processed webcam feed.
    cv2.imshow("Gesture Control", cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
    # Exit the program when the 'q' key is pressed.
    if cv2.waitKey(1) & 0xFF == ord('q'): break

cap.release()
cv2.destroyAllWindows()

