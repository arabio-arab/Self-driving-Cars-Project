import cv2
import numpy as np

def detect_lanes(frame):
    # Convert to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # Define range for lane colors (adjust these values based on your needs)
    lower_white = np.array([0, 0, 200])
    upper_white = np.array([180, 255, 255])
    mask = cv2.inRange(hsv, lower_white, upper_white)
    edges = cv2.Canny(mask, 100, 200)  # Increased thresholds

    # Apply dilation to strengthen the edges
    kernel = np.ones((5, 5), np.uint8)
    dilated_edges = cv2.dilate(edges, kernel, iterations=1)

    # Detect lines with adjusted parameters
    lines = cv2.HoughLinesP(dilated_edges, 1, np.pi / 180, threshold=100, minLineLength=100, maxLineGap=20)
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            angle = np.degrees(np.arctan2(y2 - y1, x2 - x1))
            if -10 < angle < 10 or 170 < angle < 190 or -190 < angle < -170 or 10 < angle < -10:
                cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)

    return frame, dilated_edges

def perspective_transform(frame):
    height, width = frame.shape[:2]
    pts1 = np.float32([[560, 440], [710, 440], [200, 640], [1000, 640]])
    pts2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    birds_eye = cv2.warpPerspective(frame, matrix, (width, height))
    return birds_eye

def main():
    cap = cv2.VideoCapture(1)
    if not cap.isOpened():
        print("Error: Camera could not be opened.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame.")
            break

        frame_with_lanes, edges = detect_lanes(frame)
        birds_eye_view = perspective_transform(frame_with_lanes)

        cv2.imshow("Frame with Lanes", frame_with_lanes)
        cv2.imshow("Edges", edges)
        cv2.imshow("Bird's Eye View", birds_eye_view)

        if cv2.waitKey(30) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
