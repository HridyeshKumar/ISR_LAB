import cv2
import numpy as np

# Initialize Webcam
cap = cv2.VideoCapture(0)

# Window Setup
cv2.namedWindow("Exp 7: Pure OpenCV Gesture Recognition", cv2.WINDOW_AUTOSIZE)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab camera frame.")
        break

    # 1. Preprocessing & Mirroring
    frame = cv2.flip(frame, 1)
    height, width, _ = frame.shape

    # Define Region of Interest (ROI) for gesture detection box
    roi_top_left = (width - 320, 50)
    roi_bottom_right = (width - 20, 350)
    cv2.rectangle(frame, roi_top_left, roi_bottom_right, (255, 100, 0), 2)
    cv2.putText(frame, "Place Hand Inside Box", (roi_top_left[0], roi_top_left[1] - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 100, 0), 1)

    # Extract ROI
    roi = frame[roi_top_left[1]:roi_bottom_right[1], roi_top_left[0]:roi_bottom_right[0]]
    
    # 2. Convert to HSV Color Space for Skin Segmentation
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

    # Broad Skin Color Range in HSV
    lower_skin = np.array([0, 20, 70], dtype=np.uint8)
    upper_skin = np.array([20, 255, 255], dtype=np.uint8)

    # Threshold skin mask & apply Gaussian blur to clean noise
    mask = cv2.inRange(hsv, lower_skin, upper_skin)
    kernel = np.ones((3, 3), np.uint8)
    mask = cv2.dilate(mask, kernel, iterations=2)
    mask = cv2.GaussianBlur(mask, (5, 5), 10)

    # 3. Find Contours (Hand Perimeter)
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    gesture = "No Hand Detected"
    finger_count = 0

    if contours:
        # Get largest contour assuming it's the hand
        max_contour = max(contours, key=cv2.contourArea)

        if cv2.contourArea(max_contour) > 3000:
            # Draw Hand Boundary
            cv2.drawContours(roi, [max_contour], -1, (0, 255, 0), 2)

            # 4. Convex Hull & Convexity Defects (Fingers Detection)
            hull = cv2.convexHull(max_contour, returnPoints=False)

            if len(hull) > 3:
                defects = cv2.convexityDefects(max_contour, hull)

                if defects is not None:
                    finger_count = 0
                    for i in range(defects.shape[0]):
                        s, e, f, d = defects[i, 0]
                        start = tuple(max_contour[s][0])
                        end = tuple(max_contour[e][0])
                        far = tuple(max_contour[f][0])

                        # Calculate triangle sides to measure defect angle
                        a = np.linalg.norm(np.array(end) - np.array(start))
                        b = np.linalg.norm(np.array(far) - np.array(start))
                        c = np.linalg.norm(np.array(end) - np.array(far))

                        # Cosine rule for angle between fingers
                        angle = np.arccos((b**2 + c**2 - a**2) / (2 * b * c + 1e-5))

                        # If angle < 90 degrees and defect is deep enough -> finger gap
                        if angle <= np.pi / 2 and d > 3000:
                            finger_count += 1
                            cv2.circle(roi, far, 5, (0, 0, 255), -1)  # Draw defect (finger dip)

                    # Total extended fingers = number of defects + 1
                    finger_count += 1

            # 5. Gesture Classification Rules based on finger count
            if finger_count <= 1:
                gesture = "Fist / Stop"
            elif finger_count == 2:
                gesture = "Peace / V-Sign (2)"
            elif finger_count == 3:
                gesture = "Three Fingers (3)"
            elif finger_count == 4:
                gesture = "Four Fingers (4)"
            elif finger_count >= 5:
                gesture = "Open Palm (5)"

    # 6. Display Dashboard Overlay
    cv2.rectangle(frame, (20, 20), (380, 100), (30, 30, 30), -1)
    cv2.rectangle(frame, (20, 20), (380, 100), (0, 255, 0), 2)

    cv2.putText(frame, f"Gesture: {gesture}", (35, 55),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    cv2.putText(frame, f"Fingers Detected: {finger_count}", (35, 85),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (50, 215, 120), 2)

    # Show Mask and Camera Feed
    cv2.imshow("Exp 7: Pure OpenCV Gesture Recognition", frame)
    cv2.imshow("Skin Segmentation Mask", mask)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
