import io
from PIL import Image
import numpy as np
import GroundingDINO.groundingdino.datasets.transforms as T
from GroundingDINO.groundingdino.util.inference import load_model, predict, annotate
from parse_config_file import config


class Detector:
    """
    Class to manage object detection.
    """

    def __init__(self):
        """
        Initializes the instance and loads the pre-trained model.
        """
        self.model = load_model(
            config.get("Model", "config_path"), config.get("Model", "weights_path")
        )
        self.prompt = ""

    def detect(self, frame):
        """
        Detects objects in the provided frame using the model.
        :param frame: The frame data to be processed for object detection.
        :return: A tuple containing the detections and the annotated frame.
        """
        # Load and transform frame.
        original_image, image = self._load_frame(frame)

        # Do prediction.
        BOX_THRESHOLD = config.getfloat("Detection", "box_threshold")
        TEXT_THRESHOLD = config.getfloat("Detection", "text_threshold")
        boxes, logits, phrases = predict(
            model=self.model,
            image=image,
            caption=self.prompt,
            box_threshold=BOX_THRESHOLD,
            text_threshold=TEXT_THRESHOLD,
        )

        # Format predictions.
        detections = []
        for bbox, phrase, confidence in zip(boxes, phrases, logits):
            detection = {
                "bbox": bbox.tolist(),
                "label": phrase,
                "confidence": float(confidence) if confidence is not None else None,
            }
            detections.append(detection)

        # Annotate original frame with predictions.
        annotated_frame = annotate(
            image_source=original_image, boxes=boxes, logits=logits, phrases=phrases
        )

        return detections, annotated_frame

    def _load_frame(self, frame):
        """
        Loads and transforms the frame for processing.
        :param frame: The raw frame data to be transformed.
        :return: A tuple containing the loaded and transformed image data.
        """
        image_rgb = Image.open(io.BytesIO(frame)).convert("RGB")
        image_np = np.array(image_rgb)

        transform = T.Compose(
            [
                T.RandomResize([800], max_size=1333),
                T.ToTensor(),
                T.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
            ]
        )
        image_transformed, _ = transform(image_rgb, None)

        return image_np, image_transformed
