import time
import threading
import picamera2


class Camera:
    """
    Class for interfacing with the Camera V2 module.
    """

    PROCESSING_DELAY = 0.1

    def __init__(self):
        """
        Initializes the instance and starts the camera.
        """
        self.camera = picamera2.Picamera2()
        self.camera.start()

    def close(self):
        """
        Closes the camera interface.
        """
        if self.camera:
            self.camera.stop()
            self.camera.close()
            self.camera = None

    def get_frame(self):
        """
        Captures and returns a single frame from the camera.
        :return: The captured frame.
        """
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
    """
    Starts a separate thread for streaming camera imagery.
    :param callback: The function to be called on each captured frame.
    """
    camera_imagery_thread = threading.Thread(target=camera.stream, args=(callback,))
    camera_imagery_thread.start()
