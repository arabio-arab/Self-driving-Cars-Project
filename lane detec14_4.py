import cv2
import numpy as np

def nothing(x):
    pass

# Initialize video capture on the second camera device
vidcap = cv2.VideoCapture(1)
if not vidcap.isOpened():
    print("Error: Camera could not be opened.")
    exit()

cv2.namedWindow("Trackbars")
cv2.createTrackbar("L - H", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("L - S", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("L - V", "Trackbars", 200, 255, nothing)
cv2.createTrackbar("U - H", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("U - S", "Trackbars", 50, 255, nothing)
cv2.createTrackbar("U - V", "Trackbars", 255, 255, nothing)

while True:
    success, image = vidcap.read()
    if not success:
        print("Failed to capture image")
        break

    frame = cv2.resize(image, (640, 480))

    # Points for perspective transformation
    tl, bl, tr, br = (222, 387), (70, 472), (400, 380), (538, 472)
    pts1 = np.float32([tl, bl, tr, br])
    pts2 = np.float32([[0, 0], [0, 480], [640, 0], [640, 480]])

    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    transformed_frame = cv2.warpPerspective(frame, matrix, (640, 480))

    hsv_transformed_frame = cv2.cvtColor(transformed_frame, cv2.COLOR_BGR2HSV)
    l_h = cv2.getTrackbarPos("L - H", "Trackbars")
    l_s = cv2.getTrackbarPos("L - S", "Trackbars")
    l_v = cv2.getTrackbarPos("L - V", "Trackbars")
    u_h = cv2.getTrackbarPos("U - H", "Trackbars")
    u_s = cv2.getTrackbarPos("U - S", "Trackbars")
    u_v = cv2.getTrackbarPos("U - V", "Trackbars")

    lower = np.array([l_h, l_s, l_v])
    upper = np.array([u_h, u_s, u_v])
    mask = cv2.inRange(hsv_transformed_frame, lower, upper)

    histogram = np.sum(mask[mask.shape[0]//2:, :], axis=0)
    midpoint = np.int(histogram.shape[0] / 2)
    left_base = np.argmax(histogram[:midpoint])
    right_base = np.argmax(histogram[midpoint:]) + midpoint

    # Decision making for turning
    lane_width = right_base - left_base
    lane_center = left_base + lane_width // 2

    if lane_center < midpoint - 50:  # Adjust threshold as needed
        print("Turn Left")
    elif lane_center > midpoint + 50:  # Adjust threshold as needed
        print("Turn Right")
    else:
        print("Forward")

    cv2.imshow("Original", frame)
    cv2.imshow("Bird's Eye View", transformed_frame)
    cv2.imshow("Lane Detection - Image Thresholding", mask)

    if cv2.waitKey(10) == 27:  # Exit on ESC
        break

vidcap.release()
cv2.destroyAllWindows()
