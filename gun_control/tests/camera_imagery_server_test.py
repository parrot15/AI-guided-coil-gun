import time
import threading
from PIL import Image
import io
import numpy as np
from gevent import monkey

monkey.patch_all()

from flask import Flask
from flask_socketio import SocketIO
import picamera2
from parse_config_file import config

app = Flask(__name__)
app.config["SECRET_KEY"] = config.get("Server", "web_secret_key")
server_socket = SocketIO(app, cors_allowed_origins="*", async_mode="gevent")

def camera_imagery(frame):
    image = Image.fromarray(frame.astype(np.uint8)).convert('RGB')
    buffer = io.BytesIO()
    image.save(buffer, format='JPEG', quality=85)
    byte_data = buffer.getvalue()
    server_socket.emit("camera-imagery", byte_data)

def stream(callback):
    camera = picamera2.Picamera2()
    camera.start()

    while True:
        try:
            frame = camera.capture_array()
            callback(frame)
            time.sleep(1)
        except KeyboardInterrupt:
            camera.stop()
            camera.close()
            return

camera_imagery_thread = threading.Thread(
    target=stream, args=(camera_imagery,)
)

if __name__ == "__main__":
    camera_imagery_thread.start()
    server_socket.run(app, debug=False, host="0.0.0.0", port=5000)