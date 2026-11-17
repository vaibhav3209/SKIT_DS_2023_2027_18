"""
MODULE 3: VEHICLE DETECTION USING YOLO
Purpose: Detect cars, motorcycles, buses and trucks in a traffic video.

Run: python vehicle_detection.py

The first run may download the YOLO model file (yolov8n.pt).
Press q in the video window to stop.
"""

import cv2
from ultralytics import YOLO

# Load a small pretrained YOLOv8 model.
model = YOLO("yolov8n.pt")

# Open the traffic video.
cap = cv2.VideoCapture("traffic.mp4")

if not cap.isOpened():
    raise SystemExit("Error: Could not open traffic.mp4.")

# COCO class IDs:
# 2 = car, 3 = motorcycle, 5 = bus, 7 = truck
VEHICLE_CLASSES = [2, 3, 5, 7]

while True:
    success, frame = cap.read()

    if not success:
        break

    # Ask YOLO to detect objects in this frame.
    results = model(frame, verbose=False)

    vehicle_count = 0

    # Go through all detections made by YOLO.
    for result in results:
        for box in result.boxes:

            # Get the detected object's class number.
            class_id = int(box.cls[0])

            # Count it only if it is one of our vehicle classes.
            if class_id in VEHICLE_CLASSES:
                vehicle_count += 1

    # Show the total vehicle count on the video frame.
    cv2.putText(
        frame,
        f"Vehicles: {vehicle_count}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    cv2.imshow("Vehicle Detection", frame)

    # Press q to exit.
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
print("Vehicle detection stopped.")
