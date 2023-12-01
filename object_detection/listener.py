from gevent import monkey

monkey.patch_all()

from flask import Flask, request
from flask_socketio import SocketIO
import cv2
from detector import Detector
from parse_config_file import config

app = Flask(__name__)
app.config["SECRET_KEY"] = config.get("Server", "web_secret_key")
server_socket = SocketIO(app, cors_allowed_origins="*", async_mode="gevent")

detector = Detector()

@server_socket.on("camera-imagery")
def object_detection(frame):
    detections, annotated_frame = detector.detect(frame)
    _, buffer = cv2.imencode(".jpg", annotated_frame)
    byte_data = buffer.tobytes()

    server_socket.emit("object-detection", {"detections": detections, "annotatedFrame": byte_data})

@app.route('/object-detection/prompt', methods=['POST'])
def update_prompt():
    detector.prompt = request.json.get('prompt')
    return {"message": f"Prompt updated to: {detector.prompt}"}

if __name__ == "__main__":
    server_socket.run(app, debug=False, host="0.0.0.0", port=5000)