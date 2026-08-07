from ultralytics import YOLO
import cv2

# Load pretrained YOLOv8 model
model = YOLO("yolov8n.pt")

# Read image
image = cv2.imread("test.jpg")

# Detect objects
results = model(image)

# Display results
annotated = results[0].plot()

cv2.imshow("Object Detection", annotated)

cv2.waitKey(0)
cv2.destroyAllWindows()