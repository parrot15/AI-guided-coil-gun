import time
import RPi.GPIO as GPIO

# Set up GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Motor control pins
IN1 = 16
IN2 = 12

# Set up pins
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)

# Set up PWM for each motor
pwm_frequency = 1000  # Change this to set the desired PWM frequency
motor_pwm = [
    GPIO.PWM(IN1, pwm_frequency),
    GPIO.PWM(IN2, pwm_frequency)
]


# Function to control motor direction and speed
def control_motor(direction, speed):
    if direction == "forward":
        motor_pwm[0].start(speed)
        motor_pwm[1].stop()
    elif direction == "backward":
        motor_pwm[0].stop()
        motor_pwm[1].start(speed)
    else:
        raise ValueError("Invalid direction.")


def get_direction():
    direction = input("Enter direction (forward or backward): ").lower()

    while True:
        if direction not in ["forward", "backward", "f", "b"]:
            print("Invalid direction entered.")
            continue

        if direction == "f":
            direction = "forward"
            break
        if direction == "b":
            direction = "backward"
            break
    
    return direction


if __name__ == "__main__":
    try:
        while True:
            # Get user input for direction
            direction = get_direction()

            # Control the motor according to user input
            control_motor(
                direction, 100
            )  # Change the speed value (0-100) as desired
            time.sleep(8)  # Change the duration of rotation as desired

            # Stop the motor
            control_motor("forward", 0)

    except KeyboardInterrupt:
        print("Exiting...")

    finally:
        # Clean up GPIO and stop all motors
        for motor in motor_pwm:
            motor.stop()
        GPIO.cleanup()