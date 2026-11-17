"""
MODULE 2: IMAGE PROCESSING
Purpose: Resize images and reduce small amounts of image noise.

Input:  images inside the 'frames' folder
Output: processed images inside the 'processed' folder

"""

import cv2
import os

INPUT_FOLDER = "frames"
OUTPUT_FOLDER = "processed"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Read each image saved by the frame extraction module.
for file_name in os.listdir(INPUT_FOLDER):

    # Ignore files that are not common image formats.
    if not file_name.lower().endswith((".jpg", ".jpeg", ".png")):
        continue

    input_path = os.path.join(INPUT_FOLDER, file_name)
    image = cv2.imread(input_path)

    if image is None:
        print("Could not read:", file_name)
        continue

    # Make all images the same size.
    image = cv2.resize(image, (640, 480))

    # Reduce small image noise. A small blur is used so vehicle shapes remain visible.
    image = cv2.GaussianBlur(image, (5, 5), 0)

    output_path = os.path.join(OUTPUT_FOLDER, file_name)
    cv2.imwrite(output_path, image)

    print("Processed:", file_name)

print("Image processing completed.")
