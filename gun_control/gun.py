import time
import serial
import RPi.GPIO as GPIO
from parse_config_file import config

class Gun:
    INIT_DELAY = 2
    PROCESSING_DELAY = 0.01
    COMMAND_MAPPINGS = {
        "left": b"L",
        "right": b"R",
        "up": b"U",
        "down": b"D",
        "stop": b"S"
    }
    COIL_PINS = [17, 27, 22, 23, 24]  # All 5 stages

    def __init__(self):
        self.direction = None

        self.arduino = serial.Serial(config.get('Arduino', 'port'), config.get('Arduino', 'baudrate'))
        # Wait for the serial connection to initialize.
        time.sleep(Gun.INIT_DELAY)

        # GPIO Setup
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)  # Use Broadcom pin numbering
        GPIO.setup(Gun.COIL_PINS, GPIO.OUT, initial=GPIO.LOW)


    def move(self, direction):
        if self.direction not in Gun.COMMAND_MAPPINGS:
            raise ValueError("Invalid direction.")

        if self.direction == "stop":
            self.stop_movement()
        else:
            self.direction = direction
            while self.direction == direction:
                self.arduino.write(Gun.COMMAND_MAPPINGS[direction])
                time.sleep(Gun.PROCESSING_DELAY)


    def stop_movement(self):
        self.arduino.write(Gun.COMMAND_MAPPINGS["stop"])


    def auto_aim(self, coords):
        if not coords:
            return
        
        for coord in coords:
            target_x, target_y = coord
            
            # Assuming 0.5, 0.5 is the center of the frame
            frame_center_x, frame_center_y = 0.5, 0.5

            # Calculate the difference
            diff_x = target_x - frame_center_x
            diff_y = target_y - frame_center_y

            # Define thresholds for movements
            threshold_x = 0.1  # Adjust as needed
            threshold_y = 0.1  # Adjust as needed

            # Determine horizontal movement
            if diff_x > threshold_x:
                self.move("right")
            elif diff_x < -threshold_x:
                self.move("left")

            # Determine vertical movement
            if diff_y > threshold_y:
                self.move("up")
            elif diff_y < -threshold_y:
                self.move("down")


    def fire(self):
        try:
            for pin in Gun.COIL_PINS:
                self._fire_coil(pin)
                # Adjust delay between each coil firing as needed
                time.sleep(0.1)
        finally:
            # Reset the GPIO pins to a safe state
            GPIO.cleanup()


    def _fire_coil(self, pin):
        GPIO.output(pin, GPIO.HIGH)
        time.sleep(0.002)  # Adjust the duration as needed
        GPIO.output(pin, GPIO.LOW)
        time.sleep(0.002)  # Adjust the duration as needed