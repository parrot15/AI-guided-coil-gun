import os
import supervision as sv
import json
from groundingdino.util.inference import load_model, load_image, predict, annotate
from endpoints import gpu_bounding_box

def segmentation(image_name, prompt):
    CONFIG_PATH = os.path.join("weights", "GroundingDINO_SwinT_OGC.py")
    WEIGHTS_PATH = os.path.join("weights", "groundingdino_swint_ogc.pth")

    model = load_model(CONFIG_PATH, WEIGHTS_PATH)

    IMAGE_PATH = image_name
    #IMAGE_PATH = os.path.join("data", IMAGE_NAME)

    TEXT_PROMPT = "prompt"
    BOX_TRESHOLD = 0.35
    TEXT_TRESHOLD = 0.25

    image_source, image = load_image(IMAGE_PATH)

    boxes, logits, phrases = predict(
        model=model, 
        image=image, 
        caption=TEXT_PROMPT, 
        box_threshold=BOX_TRESHOLD, 
        text_threshold=TEXT_TRESHOLD
    )

    #annotated_frame = annotate(image_source=image_source, boxes=boxes, logits=logits, phrases=phrases)
    #converts a tensor object into json data
    numpy_boxes = boxes.numpy()
    python_boxes = numpy_boxes.tolist()
    json_boxes = json.dumps(python_boxes)

    numpy_logits = logits.numpy()
    python_logits = numpy_logits.tolist()
    json_logits = json.dumps(python_logits)

    json_data = [json_boxes, json_logits]
    return json_data
    

        
