import io
from PIL import Image
from gevent import monkey

monkey.patch_all()

from flask import Flask, request
from flask_socketio import SocketIO
import numpy as np
from parse_config_file import config
from gun import Gun
import camera_imagery as imagery

app = Flask(__name__)
app.config["SECRET_KEY"] = config.get("Server", "web_secret_key")
server_socket = SocketIO(app, cors_allowed_origins="*", async_mode="gevent")

gun = Gun()

@server_socket.on("gun-movement")
def gun_movement(direction):
    print(f"Received direction: {direction}")
    gun.move(direction)

@server_socket.on("gun-movement/auto-aim")
def gun_movement_auto_aim(center_points):
    coords = center_points['centerPoints']
    print(f'Received {len(coords)} coordinates.')
    gun.auto_aim(coords)

def camera_imagery(frame):
    image = Image.fromarray(frame.astype(np.uint8)).convert('RGB')
    buffer = io.BytesIO()
    image.save(buffer, format='JPEG', quality=config.get('Camera', 'image_quality'))
    byte_data = buffer.getvalue()
    server_socket.emit("camera-imagery", byte_data)

@app.route("/fire-projectile", methods=["POST"])
def fire_projectile():
    control_mode = request.json.get('controlMode')
    print(f"Received control mode: {control_mode}")
    gun.fire()
    return {"controlMode": control_mode}

imagery.start_stream(camera_imagery)

if __name__ == "__main__":
    server_socket.run(app, debug=config.getboolean('Server', 'debug'), host=config.get('Server', 'host'), port=config.getint('Server', 'port'))