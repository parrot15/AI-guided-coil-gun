import time
import picamera2

with picamera2.Picamera2() as camera:
    camera.start()

    while True:
        frame = camera.capture_array()
        print(frame.shape)
        time.sleep(1)
