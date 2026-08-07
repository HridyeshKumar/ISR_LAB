from ultralytics import YOLO
import cv2

model = YOLO("yolov8n.pt")

image = cv2.imread("test.jpg")

results = model(image)

for result in results:

    boxes = result.boxes

    for box in boxes:

        cls = int(box.cls[0])

        confidence = float(box.conf[0])

        label = model.names[cls]

        print("Object:", label)
        print("Confidence:", round(confidence,2))