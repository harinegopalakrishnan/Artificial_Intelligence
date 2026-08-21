import cv2, time, numpy as np
import mediapipe as mp

# Store the MediaPipe Hands module in the variable 'H' for easier access.
H = mp.solutions.hands
# Store the HandLandmark class in the variable 'TIP' to access landmarks easily.
TIP = H.HandLandmark
# Store the fingertip landmark positions in a dictionary.
ids = {
    "thumb": TIP.THUMB_TIP,
    "index": TIP.INDEX_FINGER_TIP,
    "middle": TIP.MIDDLE_FINGER_TIP,
    "ring": TIP.RING_FINGER_TIP,
    "pinky": TIP.PINKY_TIP,
}

# Create the MediaPipe hand detector.
hands = H.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
# Load the utility to draw hand landmarks.
draw = mp.solutions.drawing_utils
# Map finger touch gestures to their corresponding filter pairs.
pairs = {"middle":("SEPIA","NEGATIVE"), "ring":("BLUR","GLITCH"), "pinky":("EDGE","CARTOON")}
# Initialize the filter state and set the default filter.
st = {k:0 for k in pairs}; cur = "SEPIA"
# Set the debounce time, capture delay, and touch thresholds.
DEB, CAP, TT, TP = 0.6, 1.2, 30, 20
# Initialize the timers and pinch detection state.
la = lc = 0; pinch_on = False
# Store the names of the application windows.
MAIN, POP = "Gesture-Controlled Photo App", "Captured (ESC / Close to resume)"
# Initialize the pause state and frozen image.
paused = False; freeze = None
# Create the Sepia filter transformation matrix.
SEPIA_M = np.array([[0.272,0.534,0.131],[0.349,0.686,0.168],[0.393,0.769,0.189]])

# Apply the selected filter to the image.
def apply(img, t):
    # Apply the Sepia filter.
    if t == "SEPIA": return np.clip(cv2.transform(img, SEPIA_M), 0, 255).astype(np.uint8)
    # Apply the Negative filter.
    if t == "NEGATIVE": return cv2.bitwise_not(img)
    # Apply the Blur filter.
    if t == "BLUR": return cv2.GaussianBlur(img, (15, 15), 0)
    # Apply the Glitch filter.
    if t == "GLITCH":
        # Get the image dimensions and split the color channels
        h,w = img.shape[:2]; r,g,b = img[:,:,2], img[:,:,1], img[:,:,0]
         # Shift the red and blue channels to create a glitch effect.
        return cv2.merge([np.roll(b, -int(0.02*w), 1), g, np.roll(r, int(0.04*w), 1)])
    # Apply the Edge Detection filter.
    if t == "EDGE": return cv2.Canny(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), 80, 160)
    # Apply the Cartoon filter.
    if t == "CARTOON":
        # Convert the image to grayscale.
        g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Detect the edges in the image.
        e = cv2.adaptiveThreshold(cv2.medianBlur(g, 7), 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 2)
        # Smooth the image while preserving edges.
        c = cv2.bilateralFilter(img, 9, 75, 75)
        # Combine the smooth image with the detected edges.
        return cv2.bitwise_and(c, c, mask=e)
    return img

# Open the default webcam.
cap = cv2.VideoCapture(0)
# Exit the program if the webcam cannot be accessed.
if not cap.isOpened(): print("Error: Could not access the webcam."); exit()
# Create a resizable application window.
cv2.namedWindow(MAIN, cv2.WINDOW_NORMAL)

while True:
    if paused:
        cv2.imshow(MAIN, freeze)
        k = cv2.waitKey(50) & 0xFF
        if k == ord("q"): break
        if k == 27:
            paused = False; pinch_on = False
            try: cv2.destroyWindow(POP)
            except: pass
            continue
        try:
            if cv2.getWindowProperty(POP, cv2.WND_PROP_VISIBLE) <= 0: paused = False; pinch_on = False
        except cv2.error:
            paused = False; pinch_on = False
        continue

    ok, img = cap.read()
    if not ok: break
    img = cv2.flip(img, 1); h, w = img.shape[:2]
    res = hands.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    now = time.time(); capture = False

    if res.multi_hand_landmarks:
        hand = res.multi_hand_landmarks[0]; draw.draw_landmarks(img, hand, H.HAND_CONNECTIONS)
        lm = hand.landmark; tips = {k:(int(lm[v].x*w), int(lm[v].y*h)) for k,v in ids.items()}
        tx,ty = tips["thumb"]; ix,iy = tips["index"]
        pinch = abs(tx-ix) < TP and abs(ty-iy) < TP
        if pinch and not pinch_on and now-lc > CAP: pinch_on = True; capture = True; lc = now
        if not pinch and pinch_on: pinch_on = False
        if not pinch:
            t = next((k for k in pairs if abs(tx-tips[k][0]) < TT and abs(ty-tips[k][1]) < TT), None)
            if t and now-la > DEB: cur = pairs[t][st[t]]; st[t] ^= 1; la = now; print("Filter:", cur)

    out = apply(img, cur)
    if cur == "EDGE": out = cv2.cvtColor(out, cv2.COLOR_GRAY2BGR)

    if capture:
        name = f"picture_{int(now)}.jpg"; cv2.imwrite(name, out); print("Saved:", name)
        paused, freeze = True, out.copy(); cv2.imshow(POP, freeze)

    cv2.imshow(MAIN, out)
    if cv2.waitKey(1) & 0xFF == ord("q"): break

cap.release(); cv2.destroyAllWindows(); hands.close()