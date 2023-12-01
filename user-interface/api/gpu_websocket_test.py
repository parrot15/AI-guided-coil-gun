import base64
from gevent import monkey

monkey.patch_all()

from flask import Flask
from flask_cors import CORS
from parse_config_file import config
from flask_socketio import SocketIO
import socketio
from process_camera_imagery import process_frame, encode_frame

app = Flask(__name__)
app.config["SECRET_KEY"] = config.get("Server", "web_secret_key")
CORS(app)
server_socket = SocketIO(app, cors_allowed_origins="*", async_mode="gevent")

# Connect to GPU web socket server
gpu_socket = socketio.Client()
gpu_socket.connect(config.get("GPU", "url"))


def camera_imagery():
    """
    Handles the "camera-imagery" event from the Raspberry Pi, processes the
    frame, and emits the processed frame data to the front-end.
    :param frame: The frame data received from the Raspberry Pi
    """
    frame = [1, 2, 3]
    server_socket.emit("camera-imagery", frame)


@gpu_socket.on('object-detection')
def object_detection(coordinates):
    print(coordinates)

if __name__ == "__main__":
    server_socket.run(app, debug=True, host="0.0.0.0", port=8000)