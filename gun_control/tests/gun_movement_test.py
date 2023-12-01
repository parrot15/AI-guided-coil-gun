import serial
import keyboard
import time

arduino = serial.Serial("/dev/cu.usbmodem1442301", 9600)
time.sleep(2)  # wait for the serial connection to initialize

try:
    while True:
        if keyboard.is_pressed("w"):
            arduino.write(b"U")
        elif keyboard.is_pressed("s"):
            arduino.write(b"D")
        elif keyboard.is_pressed("a"):
            arduino.write(b"L")
        elif keyboard.is_pressed("d"):
            arduino.write(b"R")
        time.sleep(0.01)  # general delay to prevent the loop from running too fast

except KeyboardInterrupt:
    arduino.close()  # close the connection
