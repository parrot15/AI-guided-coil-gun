import time
import requests

class FrameStreamer:
    def __init__(self, server_socket, gpu_socket, interval=0.5):
        self.server_socket = server_socket
        self.gpu_socket = gpu_socket
        self.interval = interval
        self.last_time_sent_to_gpu = 0
        self.prompt = ""

    def stream_camera_imagery(self, frame):
        """
        Handles the "camera-imagery" event from the Raspberry Pi, processes the
        frame, and emits the processed frame data to the front-end and the GPU server.
        :param frame: The frame data received from the Raspberry Pi
        """
        # Emit frame data to the front-end without interruption
        self.server_socket.emit("camera-imagery", frame)

        # If user hasn't actually searched for anything, do nothing
        if self.prompt == "":
            return

        # Check if the specified interval has passed since the last frame was sent to the GPU
        current_time = time.time()
        if current_time - self.last_time_sent_to_gpu >= self.interval:
            # Send the frame to the GPU server
            self.gpu_socket.emit("camera-imagery", frame)
            # Update the last sent time
            self.last_time_sent_to_gpu = current_time

    def send_frame(self, frame):
        self.server_socket.emit("camera-imagery", frame)

    def send_to_UI(self, frame):
        self.server_socket.emit("camera-imagery", frame)

    def send_to_GPU(self, frame):
        self.gpu_socket.emit("camera-imagery", frame)
