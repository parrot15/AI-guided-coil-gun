import base64
from pprint import pprint
from flask import Flask, request
from flask_cors import CORS
from parse_config_file import config
from flask_socketio import SocketIO
import socketio
import requests
from process_camera_imagery import process_frame, encode_frame
from frame_streamer import FrameStreamer

app = Flask(__name__)
app.config["SECRET_KEY"] = config.get("Server", "web_secret_key")
CORS(app)
server_socket = SocketIO(app, cors_allowed_origins="*", async_mode="gevent")

# Connect to the Raspberry Pi web socket server
raspberry_pi_socket = socketio.Client()
raspberry_pi_socket.connect(config.get("Raspberry Pi", "url"), wait_timeout=10)

# Connect to the GPU web socket server
gpu_socket = socketio.Client()
gpu_socket.connect(config.get("GPU", "url"), wait_timeout=10)

# Initialize the FrameStreamer
frame_streamer = FrameStreamer(server_socket, gpu_socket)


@server_socket.on("gun-movement")
def gun_movement(direction):
    """
    Handles the "gun-movement" event and forwards it to the Raspberry Pi.
    :param direction: Direction to move the gun ('left', 'right', or 'stop')
    """
    print(f"Sending direction: {direction}")
    raspberry_pi_socket.emit("gun-movement", direction)


# @server_socket.on("user-input")
# def user_input(input):
#     filename = input + ".jpeg"
#     with open(filename, "w") as f:
#         f.write(base64.b64decode(curr_frame))
#     # sendToGPU(filename)


@raspberry_pi_socket.on("camera-imagery")
def camera_imagery(frame):
    """
    Handles the "camera-imagery" event from the Raspberry Pi, processes 
    the frame, and emits the processed frame data to the frontend and 
    the GPU server.
    :param frame: The frame data received from the Raspberry Pi
    """
    # print(frame)

    # server_socket.emit("camera-imagery", frame)
    # gpu_socket.emit("camera-imagery", frame)
    frame_streamer.stream_camera_imagery(frame)


@gpu_socket.on('object-detection')
def object_detection(result):
    """
    [{'bbox': [0.5119307637214661, 0.6944025754928589, 0.08959539979696274, 0.31756800413131714], 'label': 'water bottle', 'confidence': 0.6070525646209717}, {'bbox': [0.6543914079666138, 0.692597508430481, 0.08025311678647995, 0.3114539682865143], 'label': 'water bottle', 'confidence': 0.4869263768196106}]
    """
    detections = result["detections"]
    annotated_frame = result["annotatedFrame"]
    print(detections)
    print(annotated_frame[:5])

    # Process detections to extract and sort center points by confidence
    center_points = []
    for detection in detections:
        bbox = detection["bbox"]
        confidence = detection["confidence"]

        # Calculate center point
        center_x = (bbox[0] + bbox[2]) / 2
        center_y = (bbox[1] + bbox[3]) / 2
        center_points.append((center_x, center_y, confidence))
    print(f'center points: {center_points}')

    # Sort center points by confidence
    center_points.sort(key=lambda x: x[2], reverse=True)
    print(f'center points sorted: {center_points}')

    # Send sorted center points to Pi
    raspberry_pi_socket.emit("gun-movement/auto-aim", {'centerPoints': center_points})

    # # Process detections to calculate center points and sort by confidence
    # centers = [(calculate_center(d["bbox"]), d["confidence"]) for d in detections]
    # centers_sorted = sorted(centers, key=lambda x: x[1], reverse=True)  # Sort by confidence

    # # Extract and send only the center points to the Raspberry Pi server
    # centers_only = [center for center, _ in centers_sorted]
    # raspberry_pi_socket.emit("object-centers", {"centers": centers_only})

    # Send annotated frame to frontend
    frame_streamer.send_frame(annotated_frame)


# def calculate_center(bbox):
#     x_center = (bbox[0] + bbox[2]) / 2
#     y_center = (bbox[1] + bbox[3]) / 2
#     return x_center, y_center


@app.route('/object-detection/prompt', methods=['POST'])
def object_detection_prompt():
    prompt = request.json.get('prompt')
    print(f"received prompt: \"{prompt}\"")
    frame_streamer.prompt = prompt
    response = requests.post(f'{config.get("GPU", "url")}/object-detection/prompt', json={'prompt': frame_streamer.prompt})
    pprint(f'=== [prompt] response ===\n{response.json()}')
    return response.json()
    # return {"prompt": prompt}

    # response = requests.post(f'{config.get("GPU", "url")}/object-detection/prompt', json={'prompt': prompt})
    # Actually, make frame_streamer handle it instead
    # frame_streamer.prompt = prompt


@app.route('/fire-projectile', methods=['POST'])
def fire_projectile():
    control_mode = request.json.get('controlMode')
    print(f"received control mode: {control_mode}")
    response = requests.post(f'{config.get("Raspberry Pi", "url")}/fire-projectile', json={'controlMode': control_mode})
    pprint(f'=== [fire] response ===\n{response.json()}')
    return response.json()
    # return {"controlMode": control_mode}

# @gpu_socket.on('gpu-bounding-box')
# def gpu_bounding_box(boundingBoxList):
#     server_socket.emit('gpu-bounding-box', boundingBoxList)
