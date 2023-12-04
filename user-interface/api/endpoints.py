from flask import Flask, request
from flask_cors import CORS
from flask_socketio import SocketIO
import socketio
import requests
from parse_config_file import config
from frame_utils import FrameStreamer, calculate_center_points

app = Flask(__name__)
app.config["SECRET_KEY"] = config.get("Server", "web_secret_key")
CORS(app)
server_socket = SocketIO(app, cors_allowed_origins="*", async_mode="gevent")

# Connect to the Raspberry Pi web socket server
raspberry_pi_socket = socketio.Client()
raspberry_pi_socket.connect(
    config.get("Raspberry Pi", "url"),
    wait_timeout=config.getint("Raspberry Pi", "connection_timeout"),
)

# Connect to the GPU web socket server
gpu_socket = socketio.Client()
gpu_socket.connect(
    config.get("GPU", "url"), wait_timeout=config.getint("GPU", "connection_timeout")
)

# Initialize the FrameStreamer
frame_streamer = FrameStreamer(server_socket, gpu_socket)


@server_socket.on("gun-movement")
def gun_movement(direction):
    """
    Handles the "gun-movement" event and forwards it to the Raspberry Pi.
    :param direction: Direction to move the gun ('left', 'right', 'up',
                      'down', 'stop').
    """
    raspberry_pi_socket.emit("gun-movement", direction)


@raspberry_pi_socket.on("camera-imagery")
def camera_imagery(frame):
    """
    Handles the "camera-imagery" event from the Raspberry Pi, and forwards
    the frame (still as bytes) to the frame streamer.
    :param frame: The frame data received from the Raspberry Pi.
    """
    frame_streamer.stream_camera_imagery(frame)


@gpu_socket.on("object-detection")
def object_detection(result):
    """
    Handles the "object-detection" event from the GPU server. Processes the
    detections, sends the coordinates to the Pi, and sends the annotated
    frame to the UI.
    :param result: The object detection results including detections and the
                   annotated frame.
    """
    detections = result["detections"]
    annotated_frame = result["annotatedFrame"]

    center_points = calculate_center_points(detections)

    # Send sorted center points to Pi
    raspberry_pi_socket.emit("gun-movement/auto-aim", {"centerPoints": center_points})

    # Send annotated frame to frontend
    frame_streamer.send_to_UI(annotated_frame)


@app.route("/object-detection/prompt", methods=["POST"])
def object_detection_prompt():
    """
    Handles POST request to update the object detection prompt. Forwards the
    prompt to the GPU server.
    :return: JSON response from the GPU server.
    """
    prompt = request.json.get("prompt")
    frame_streamer.prompt = prompt
    response = requests.post(
        f'{config.get("GPU", "url")}/object-detection/prompt',
        json={"prompt": frame_streamer.prompt},
    )
    return response.json()


@app.route("/fire-projectile", methods=["POST"])
def fire_projectile():
    """
    Handles POST request to trigger the firing mechanism. Forwards the control
    mode to the Raspberry Pi server.
    :return: JSON response from the Raspberry Pi server.
    """
    control_mode = request.json.get("controlMode")
    response = requests.post(
        f'{config.get("Raspberry Pi", "url")}/fire-projectile',
        json={"controlMode": control_mode},
    )
    return response.json()
