"""
DYNAMIC TIMING ALGORITHM
Purpose: Select the direction with the highest vehicle count and calculate
a simple green-light duration.

Run: python dynamic_timing.py

"""

# Sample vehicle counts for four directions.
traffic = {
    "North": 15,
    "South": 5,
    "East": 10,
    "West": 3
}

# Find the direction having the highest vehicle count.
selected_direction = max(traffic, key=traffic.get)

# Get the number of vehicles in that direction.
vehicle_count = traffic[selected_direction]

# Simple example formula:
# Base green time = 10 seconds
# Add 2 seconds for every detected vehicle.
green_time = 10 + (vehicle_count * 2)

# Do not allow green time to exceed 40 seconds.
green_time = min(green_time, 40)

print("Vehicle counts:", traffic)
print("Selected direction:", selected_direction)
print("Green signal time:", green_time, "seconds")
