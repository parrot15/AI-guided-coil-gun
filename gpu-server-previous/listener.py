from flask import Flask
from flask_cors import CORS
from parse_config_file import config
from flask_socketio import SocketIO
from process_camera_imagery import process_frame, encode_frame
from segmentation import segmentation

app = Flask(__name__)
app.config["SECRET_KEY"] = config.get("Server", "web_secret_key")
server_socket = SocketIO(app, cors_allowed_origins="*", async_mode="gevent")

@server_socket.on('gpu-bounding-box')
def gpu_bounding_box(json):
    server_socket.emit('gpu-bounding-box', json)

@server_socket.on("camera-imagery")
def camera_imagery(frame):
    """
    Handles the "camera-imagery" event from the UI, processes the
    frame, and emits the processed frame data to the front-end.
    :param frame: The frame data received from the UI
    """
    processed = process_frame(frame)

@server_socket.on("user-input")
def user_input(input):
    boxes = segmentation(input, input)
    gpu_bounding_box(boxes)
    print(f"recieved input: {input}")

if __name__ == "__main__":
    server_socket.run(app, debug=True, host="0.0.0.0", port= "5000")