import time
from parse_config_file import config


class FrameStreamer:
    """
    Class to manage streaming of frames to the UI and GPU server.
    """

    def __init__(
        self,
        server_socket,
        gpu_socket,
        interval=config.getint("GPU", "detection_interval"),
    ):
        """
        Initializes the instance with sockets and transmission interval.
        :param server_socket: The socket connection to the UI server.
        :param gpu_socket: The socket connection to the GPU server.
        :param interval: Time interval in seconds to wait before sending the
                         next frame to the GPU server.
        """
        self.server_socket = server_socket
        self.gpu_socket = gpu_socket
        self.interval = interval
        self.last_time_sent = 0
        self.prompt = ""

    def stream_camera_imagery(self, frame):
        """
        Streams the camera imagery to the UI, and to the GPU server at
        specified intervals.
        :param frame: The frame to be streamed.
        """
        # Emit frame to the front-end without interruption
        self.send_to_UI(frame)

        # If user hasn't actually searched for anything, do nothing
        if self.prompt == "":
            return

        # Check if the specified interval has passed since the last frame was sent to the GPU
        current_time = time.time()
        if current_time - self.last_time_sent >= self.interval:
            # Send the frame to the GPU server
            self.send_to_GPU(frame)
            # Update the last sent time
            self.last_time_sent = current_time

    def send_to_UI(self, frame):
        """
        Sends the frame to the UI server.
        :param frame: The frame to be sent.
        """
        self.server_socket.emit("camera-imagery", frame)

    def send_to_GPU(self, frame):
        """
        Sends the frame to the GPU server.
        :param frame: The frame to be sent.
        """
        self.gpu_socket.emit("camera-imagery", frame)


def calculate_center_points(detections):
    """
    Calculates the center points of the bounding boxes, then sorts them
    baed on their confidence level.
    :param detections: A list of detections, each with a bounding box and
                       confidence level.
    :return: A list of center points sorted by confidence level.
    """
    center_points = []
    # Sort detections by confidence, so that higher-confidence
    # targets are hit first.
    for detection in sorted(detections, key=lambda x: x["confidence"], reverse=True):
        x1, y1, x2, y2 = detection["bbox"]
        center_point = ((x1 + x2) / 2, (y1 + y2) / 2)
        center_points.append(center_point)

    return center_points
