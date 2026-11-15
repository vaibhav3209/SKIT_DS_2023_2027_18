DYNAMIC TRAFFIC LIGHT PROJECT — EASY BEGINNER CODE
=================================================

WHAT IS INCLUDED?
-----------------
1. frame_extraction.py  - Extract images from a traffic video.
2. image_processing.py  - Resize images and reduce image noise.
3. vehicle_detection.py - Detect and count vehicles using YOLO.
4. dynamic_timing.py    - Select the busiest direction and calculate green time.
5. traffic_signal.py    - Operate red, yellow and green LEDs using Raspberry Pi GPIO.
6. requirements.txt     - Python packages needed by the project.

FOLDER SETUP
------------
Keep the files in one project folder:

Dynamic_Traffic_Light_Easy_Code/
    traffic.mp4
    frame_extraction.py
    image_processing.py
    vehicle_detection.py
    dynamic_timing.py
    traffic_signal.py
    requirements.txt

The frames/ and processed/ folders are created by the programs.

INSTALLATION ON WINDOWS (FOR MODULES 1, 2 AND 3)
------------------------------------------------
1. Install Python.
2. Open Command Prompt in this project folder.
3. Install packages:

   pip install -r requirements.txt

4. Put your traffic video in this folder and name it traffic.mp4.

RUN THE MODULES IN ORDER
------------------------
Module 1:
   python frame_extraction.py

Module 2:
   python image_processing.py

Module 3:
   python vehicle_detection.py

Module 3 uses YOLO and may download yolov8n.pt the first time.
A camera/video preview opens. Press q to close it.

Module 4 — Dynamic timing example:
   python dynamic_timing.py

This uses sample vehicle counts. It demonstrates the decision logic.
It is not yet connected automatically to the YOLO count.

Module 5 — Hardware LED demonstration:
   python traffic_signal.py

Run this only on a Raspberry Pi with the LEDs wired correctly.
The gpiozero library is designed to control Raspberry Pi GPIO; this script
will not operate Raspberry Pi pins on an ordinary Windows laptop.

IMPORTANT PROJECT LIMITATIONS
------------------------------
- The YOLO example counts vehicles in the entire video frame. It does NOT yet
  separate North, South, East and West.
- The timing example uses manually entered sample counts. It is not yet
  connected to the YOLO program.
- The GPIO example controls one set of three LEDs, not a complete four-way
  intersection.
- These files are intentionally kept separate and simple so each module can
  be understood and demonstrated independently.

NEXT DEVELOPMENT STEP
---------------------
For the final four-way prototype, the next step is to define four lane regions
(ROIs) in the camera image, count vehicles separately in each region, pass
those four counts into the timing algorithm, and control all four signal sets
with a safety rule that prevents conflicting green lights.

SAFETY
------
Use only a low-voltage tabletop LED prototype under supervision.
Use suitable current-limiting resistors. Never connect high-current lamps,
12V modules, relays or motors directly to Raspberry Pi GPIO. Use an appropriate
driver circuit and separate power supply. Do not connect this student
prototype to public-road traffic signals.
