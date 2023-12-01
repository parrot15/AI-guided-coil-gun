import time
import picamera2

with picamera2.Picamera2() as camera:
    # config = camera.preview_configuration(main={"format": "RGB888", "size": (640, 480)})
    # config = camera.preview_configuration()
    # camera.configure(config)

    camera.start()

    while True:
        frame = camera.capture_array()

        print(frame.shape)
        # print(frame[:3], frame[:][:3])

        time.sleep(1)