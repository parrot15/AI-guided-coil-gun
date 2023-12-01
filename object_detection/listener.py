import io
from pprint import pprint
from gevent import monkey

monkey.patch_all()

from flask import Flask, request
from flask_socketio import SocketIO
from PIL import Image
import numpy as np
import supervision as sv
import cv2
import torch
import GroundingDINO.groundingdino.datasets.transforms as T
from GroundingDINO.groundingdino.util.inference import load_model, load_image, predict, annotate
# from GroundingDINO.groundingdino.util.inference import Model
from parse_config_file import config

app = Flask(__name__)
app.config["SECRET_KEY"] = config.get("Server", "web_secret_key")
server_socket = SocketIO(app, cors_allowed_origins="*", async_mode="gevent")

CONFIG_PATH = "GroundingDINO/groundingdino/config/GroundingDINO_SwinT_OGC.py"
WEIGHTS_PATH = "GroundingDINO/weights/groundingdino_swint_ogc.pth"
# model = Model(CONFIG_PATH, WEIGHTS_PATH)
model = load_model(CONFIG_PATH, WEIGHTS_PATH)
current_prompt = "human face"

# def load_frame(frame):
#     image = Image.open(io.BytesIO(frame))
#     image_np = np.array(image)
#     image_bgr = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
#     return image_bgr

def load_frame(frame):
    transform = T.Compose(
        [
            T.RandomResize([800], max_size=1333),
            T.ToTensor(),
            T.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
        ]
    )
    image_rgb = Image.open(io.BytesIO(frame)).convert('RGB')
    image_np = np.array(image_rgb)
    image_transformed, _ = transform(image_rgb, None)
    return image_np, image_transformed

@server_socket.on("camera-imagery")
def object_detection(frame):
    # print frame shape
    print(frame[:5])

    # # load frame
    # image = load_frame(frame)

    # # do prediction
    # TEXT_PROMPT = "a dog holding a bone"
    # detections, phrases = model.predict_with_caption(
    #     image=image,
    #     caption=TEXT_PROMPT
    # )

    # # format results
    # coords = []
    # # annotator = sv.BoxAnnotator()
    # for (bbox, _, confidence, _, _), phrase in zip(detections, phrases):
    #     detection = {
    #         "bbox": bbox.tolist(),
    #         "label": phrase,
    #         "confidence": float(confidence) if confidence is not None else None
    #     }
    #     # label = f"{phrase} {confidence:.2f}"
    #     coords.append(detection)
    #     # annotator.draw_box(image, bbox, label=label)
    # # _, buffer = cv2.imencode(".jpg", image)
    # # bytes_data = buffer.tobytes()
    # pprint(f'=== coords ===\n{coords}')

    # load and transform frame
    original_image, image = load_frame(frame)
    # image = Image.open(io.BytesIO(frame)).convert('RGB')
    # transform = T.Compose(
    #     [
    #         T.RandomResize([800], max_size=1333),
    #         T.ToTensor(),
    #         T.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
    #     ]
    # )
    # image_transformed, _ = transform(image, None)

    # do prediction
    # TEXT_PROMPT = "human face"
    BOX_TRESHOLD = 0.35
    TEXT_TRESHOLD = 0.25
    boxes, logits, phrases = predict(
        model=model,
        image=image,
        # caption=TEXT_PROMPT,
        caption=current_prompt,
        box_threshold=BOX_TRESHOLD,
        text_threshold=TEXT_TRESHOLD
    )
    detections = []
    for bbox, phrase, confidence in zip(boxes, phrases, logits):
        detection = {
            "bbox": bbox.tolist(),
            "label": phrase,
            "confidence": float(confidence) if confidence is not None else None
        }
        detections.append(detection)
    pprint(f'=== detections ===\n{detections}')
    # print(f'=== boxes ===\n{boxes}')
    # print(f'=== logits ===\n{logits}')
    # print(f'=== phrases ===\n{phrases}')

    annotated_frame = annotate(
        image_source=original_image,
        boxes=boxes,
        logits=logits,
        phrases=phrases
    )
    _, buffer = cv2.imencode(".jpg", annotated_frame)
    byte_data = buffer.tobytes()

    server_socket.emit("object-detection", {"detections": detections, "annotatedFrame": byte_data})

@app.route('/object-detection/prompt', methods=['POST'])
def update_prompt():
    global current_prompt
    current_prompt = request.json.get('prompt', current_prompt)
    return {"message": f"Prompt updated to: {current_prompt}"}

if __name__ == "__main__":
    server_socket.run(app, debug=False, host="0.0.0.0", port=5000)