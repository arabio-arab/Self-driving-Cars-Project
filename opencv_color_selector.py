
import cv2
import numpy as np

def createGUI():
    '''Function that creates the trackbar interface'''
    global screen
    cv2.createTrackbar("Low Hue", screen, 0, 179, lambda x: updateValues(x, 0, 0))
    cv2.createTrackbar("High Hue", screen, 179, 179, lambda x: updateValues(x, 1, 0))
    cv2.createTrackbar("Low Sat", screen, 0, 255, lambda x: updateValues(x, 0, 1))
    cv2.createTrackbar("High Sat", screen, 255, 255, lambda x: updateValues(x, 1, 1))
    cv2.createTrackbar("Low Val", screen, 0, 255, lambda x: updateValues(x, 0, 2))
    cv2.createTrackbar("High Val", screen, 255, 255, lambda x: updateValues(x, 1, 2))
    cv2.createTrackbar("Invert", screen, 0, 1, doInvert)

def doInvert(val):
    '''Function that alters mask inversion'''
    global invert
    invert = bool(val)
    updateImg()

def updateValues(val, colrange, param):
    '''Function that updates the value ranges as set by the trackbars'''
    global col
    col[colrange][param] = val
    updateImg()

def updateImg():
    '''Displays image, masked with updated values'''
    global capture, img_hsv, col, invert
    ret, img = capture.read()
    if not ret:
        print("Failed to grab frame")
        return
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(img_hsv, tuple(col[0]), tuple(col[1]))
    if invert:
        mask = cv2.bitwise_not(mask)
    res = cv2.bitwise_and(img, img, mask=mask)
    # Correct the resize function call
    res = cv2.resize(res, (480, 240))  # Width x Height
    rotated_frame = cv2.rotate(res, cv2.ROTATE_90_CLOCKWISE)
    cv2.imshow('Image', rotated_frame)

### Initial setup:
invert = False
col = [[0, 0, 0], [179, 255, 255]]
screen = "Control"

# Initialize the camera capture
capture = cv2.VideoCapture(0)  # 0 is typically the default camera

# The following line is not needed if you're capturing from the default camera
#     url = "http://100.65.0.166:8080/shot.jpg"

capture.open('http://10.206.6.217:8080/video')

if not capture.isOpened():
    raise IOError("Cannot open webcam")

cv2.namedWindow(screen, cv2.WINDOW_AUTOSIZE)
createGUI()

# Main loop to keep updating the image
while True:
    updateImg()
    if cv2.waitKey(1) & 0xFF == ord('q'):  # press 'q' to quit
        break

capture.release()
cv2.destroyAllWindows()
