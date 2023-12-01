import time
import threading
import picamera2

class Camera:
    """
    Class for interfacing with Camera V2 module.
    Follows singleton pattern to ensure only one instance of
    the class is created (cannot have multiple instances at
    once.)
    """

    PROCESSING_DELAY = 0.1
    # _instance = None

    # def __new__(cls):
    #     if cls._instance is None:
    #         cls._instance = super(Camera, cls).__new__(cls)
    #         cls._instance.__initialized = False
    #     return cls._instance

    def __init__(self):
        # if self.__initialized:
        #     return
        self.camera = picamera2.Picamera2()
        self.camera.start()
        # self.__initialized = True
    
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
                # time.sleep(1)
            except KeyboardInterrupt:
                self.close()
                return

camera = Camera()

def start_stream(callback):
    camera_imagery_thread = threading.Thread(
        target=camera.stream, args=(callback,)
    )
    camera_imagery_thread.start()