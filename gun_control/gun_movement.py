import time
import serial

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
    
    if direction != command_mappings["stop"]:
        gun_movement.rotate_motors(command_mappings[direction])


def auto_aim_motors(coords):
    if not coords:
        return
    
    for coord in coords:
        target_x, target_y, _ = coord
        
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
            gun_movement.rotate_motors(command_mappings["right"])
        elif diff_x < -threshold_x:
            gun_movement.rotate_motors(command_mappings["left"])

        # Determine vertical movement
        if diff_y > threshold_y:
            gun_movement.rotate_motors(command_mappings["up"])
        elif diff_y < -threshold_y:
            gun_movement.rotate_motors(command_mappings["down"])

        # Additional logic to stop


def fire():
    pass