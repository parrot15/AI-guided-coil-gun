import io
from PIL import Image
from gevent import monkey

monkey.patch_all()

from flask import Flask
from flask_socketio import SocketIO
import numpy as np
from parse_config_file import config
import gun_movement as gun
import camera_imagery as imagery

app = Flask(__name__)
app.config["SECRET_KEY"] = config.get("Server", "web_secret_key")
server_socket = SocketIO(app, cors_allowed_origins="*", async_mode="gevent")

@server_socket.on("gun-movement")
def gun_movement(direction):
    print(f"Received direction: {direction}")
    gun.move(direction)

# @server_socket.on("camera-imagery")
def camera_imagery(frame):
    # print(frame.shape)
    image = Image.fromarray(frame.astype(np.uint8)).convert('RGB')
    buffer = io.BytesIO()
    image.save(buffer, format='JPEG', quality=85)
    byte_data = buffer.getvalue()
    server_socket.emit("camera-imagery", byte_data)

imagery.start_stream(camera_imagery)

if __name__ == "__main__":
    server_socket.run(app, debug=False, host="0.0.0.0", port=5000)