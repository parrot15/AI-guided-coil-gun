import time
import threading
import picamera2

class Camera:
    """
    Class for interfacing with Camera V2 module.
    """
    PROCESSING_DELAY = 0.1

    def __init__(self):
        self.camera = picamera2.Picamera2()
        self.camera.start()
    
    def close(self):
        if self.camera:
            self.camera.stop()
            self.camera.close()
            self.camera = None

    def get_frame(self):
        return self.camera.capture_array()
    
    def stream(self, callback):
        while True:
            try:
                callback(self.get_frame())
                time.sleep(Camera.PROCESSING_DELAY)
            except KeyboardInterrupt:
                self.close()
                return

camera = Camera()

def start_stream(callback):
    camera_imagery_thread = threading.Thread(
        target=camera.stream, args=(callback,)
    )
    camera_imagery_thread.start()