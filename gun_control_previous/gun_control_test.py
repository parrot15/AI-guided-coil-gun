import serial
import keyboard
import time

arduino = serial.Serial("/dev/cu.usbmodem1442301", 9600)
time.sleep(2)  # wait for the serial connection to initialize

try:
    while True:
        if keyboard.is_pressed("w"):
            arduino.write(b"U")
            # time.sleep(
            #     0.05
            # )  # you can adjust this delay based on how often you want to send the commands

        elif keyboard.is_pressed("s"):
            arduino.write(b"D")
            # time.sleep(0.05)

        elif keyboard.is_pressed("a"):
            arduino.write(b"L")
            # time.sleep(0.05)

        elif keyboard.is_pressed("d"):
            arduino.write(b"R")
            # time.sleep(0.05)

        time.sleep(0.01)  # general delay to prevent the loop from running too fast

except KeyboardInterrupt:
    arduino.close()  # close the connection
