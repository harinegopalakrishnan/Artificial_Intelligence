'''
If faced any error during running the code, run these lines
Expected Output:
OpenCV Version: 4.10.0
CascadeClassifier Available: True
Wrong Output:
Uninstall: pip uninstall opencv-python
Reinstall: pip install opencv-python==4.10.0.84
'''
import cv2

print("OpenCV Version:", cv2.__version__)
print("CascadeClassifier Available:", hasattr(cv2, "CascadeClassifier"))