import board
import digitalio
import random
import math
import time
import busio
from adafruit_mpu6050 import MPU6050

# Constants
BUZZER_PIN = board.GP18

# Initialize onboard buzzer
buzzer = digitalio.DigitalInOut(BUZZER_PIN)
buzzer.direction = digitalio.Direction.OUTPUT

# Initialize MPU-6050 sensor
i2c = busio.I2C(board.GP1, board.GP0)
mpu = MPU6050(i2c)

# Variables
duration = 1
tone = 500
chk_time = 3

# Angle fun
last_angle = 0  # Initialize the last recorded angle
last_angle_change_time = time.monotonic()  # Initialize the time of the last angle change

# Function to generate a random tone
def random_tone():
    return random.randint(200, 2000)

# Function to play a tone via buzzer
def play_tone(tone, duration):
    buzzer.value = True
    time.sleep(duration)
    buzzer.value = False

# Main loop
while True:
    # Read MPU-6050
    accel_x, accel_y, accel_z = mpu.acceleration

    # Calculate tilt angle
    tilt_angle = math.atan2(accel_y, accel_z) * (180 / math.pi)

    # Check for change in tilt direction
    if abs(tilt_angle - last_angle) > 20:  # Adjust as needed
        # Generate random tone and play 
        tone = random_tone()
        play_tone(tone, 0.2)  # Adjust as needed

        # Update the time of the last angle change
        last_angle_change_time = time.monotonic()

    # Check if angle changed in defined time period (chk_time variable)
    if time.monotonic() - last_angle_change_time > chk_time:
        # Stop tone
        buzzer.value = False

    last_angle = tilt_angle  # Update last recorded angle

    time.sleep(0)  # Adjust duration to smooth tone/performance

