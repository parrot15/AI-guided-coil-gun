import time
import RPi.GPIO as GPIO

# Replace these with the GPIO pins you are using
coil_pins = [17, 27, 22, 23, 24]  # All 5 stages

# Setup
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)  # Use Broadcom pin numbering
GPIO.setup(coil_pins, GPIO.OUT, initial=GPIO.LOW)


def fire_coil(pin):
    print(f"Firing coil connected to GPIO {pin}")
    GPIO.output(pin, GPIO.HIGH)
    time.sleep(0.02)  # Adjust the duration as needed
    GPIO.output(pin, GPIO.LOW)


if __name__ == "__main__":
    try:
        for pin in coil_pins:
            fire_coil(pin)
            time.sleep(0.1)  # Adjust delay between each coil firing as needed
    finally:
        GPIO.cleanup()  # Reset the GPIO pins to a safe state
