import time
import RPi.GPIO as GPIO

# Replace these with the GPIO pins you are using
coil_pins = [17]  # Just first stage for now

# Setup
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)  # Use Broadcom pin numbering
GPIO.setup(coil_pins, GPIO.OUT, initial=GPIO.LOW)

if __name__ == "__main__":
    # First stage
    # while True:
    GPIO.output(17, GPIO.HIGH)
    time.sleep(0.002)  # Adjust the duration as needed
    GPIO.output(17, GPIO.LOW)
    time.sleep(0.002)  # Adjust the duration as needed