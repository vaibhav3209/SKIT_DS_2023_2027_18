"""
MODULE 1: FRAME EXTRACTION
Purpose: Read a traffic video and save every 10th frame as an image.

Before running:
1. Put your video in this folder.
2. Rename it to traffic.mp4, or change VIDEO_PATH below.
3. Run: python frame_extraction.py
"""

import cv2
import os

VIDEO_PATH = "traffic.mp4"
OUTPUT_FOLDER = "frames"
SAVE_EVERY = 10  # Save one frame after every 10 video frames

# Create the output folder if it does not already exist.
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Open the video file.
video = cv2.VideoCapture(VIDEO_PATH)

if not video.isOpened():
    raise SystemExit("Error: Could not open traffic.mp4. Check the video path.")

frame_number = 0
saved_number = 0

while True:
    # Read the next frame.
    success, frame = video.read()

    # Stop when the video has ended.
    if not success:
        break

    # Save only every 10th frame to avoid saving too many images.
    if frame_number % SAVE_EVERY == 0:
        file_name = f"frame_{saved_number:04d}.jpg"
        file_path = os.path.join(OUTPUT_FOLDER, file_name)

        cv2.imwrite(file_path, frame)
        print("Saved:", file_path)
        saved_number += 1

    frame_number += 1

video.release()
print(f"Finished. Saved {saved_number} frames.")
