import time
import serial

# arduino = serial.Serial("/dev/cu.usbmodem1442301", 9600)
# time.sleep(2)  # Wait for the serial connection to initialize.

command_mappings = {
    "left": b"L",
    "right": b"R",
    "up": b"U",
    "down": b"D",
    "stop": b"S"
}

class GunMovement:
    INIT_DELAY = 2
    PROCESSING_DELAY = 0.01

    def __init__(self):
        self.arduino = serial.Serial("/dev/ttyACM0", 9600)
        # Wait for the serial connection to initialize.
        time.sleep(GunMovement.INIT_DELAY)
        self.direction = None

    def rotate_motors(self, direction):
        self.direction = direction

        while self.direction == direction:
            self.arduino.write(direction)
            time.sleep(GunMovement.PROCESSING_DELAY)

gun_movement = GunMovement()

def move(direction):
    if direction not in command_mappings:
        raise ValueError("Invalid direction.")
    
    if direction == command_mappings["stop"]:
        pass
    else:
        gun_movement.rotate_motors(command_mappings[direction])