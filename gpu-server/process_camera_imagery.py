import base64
import numpy as np
import cv2
from skimage import color


def normalize_data(frame, vmin, vmax):
    """
    Normalize the frame data based on the minimum and maximum temperature values.
    :param frame: Input frame data
    :param vmin: Minimum temperature value
    :param vmax: Maximum temperature value
    :return: Normalized frame data
    """
    frame = np.array(frame).reshape(24, 32)
    return (frame - vmin) / (vmax - vmin)


def apply_colormap(norm_frame, colormap):
    """
    Apply a colormap to the normalized frame data.
    :param norm_frame: Normalized frame data
    :param colormap: Colormap function to apply
    :return: Colored frame data
    """
    vec_colormap = np.vectorize(colormap, otypes=[np.uint8, np.uint8, np.uint8])
    img_data_r, img_data_g, img_data_b = vec_colormap(norm_frame, colormap)
    return np.stack((img_data_r, img_data_g, img_data_b), axis=-1)


def map_colors(val):
    """
    Map input values to RGB colors using the HSV color space.
    :param val: Input value
    :return: Tuple with RGB color components
    """
    return tuple(color.hsv2rgb(1 - val, 1, 1) * 255)


def smooth_image(img, new_size=(64, 48)):
    """
    Smooth the input image using interpolation and Gaussian blur.
    :param img: Input image
    :param new_size: Tuple with the desired output size
    :return: Smoothed image
    """
    interpolated = cv2.resize(img, new_size, interpolate=cv2.INTER_CUBIC)
    return cv2.GaussianBlur(interpolated, (3, 3), 0)


def create_image(img_data):
    """
    Create an image from the RGB data.
    :param img_data: Input RGB data
    :return: Image in BGR format
    """
    return cv2.cvtColor(img_data, cv2.COLOR_RGB2BGR)


def process_frame(frame, min_temp=0, max_temp=60):
    """
    Process the input frame data by normalizing, applying a colormap, and
    smoothing the image.
    :param frame: Input frame data
    :param min_temp: Minimum temperature value
    :param max_temp: Maximum temperature value
    :return: Processed image
    """
    normalized = normalize_data(frame, min_temp, max_temp)
    mapped = apply_colormap(normalized, map_colors)
    smoothed = smooth_image(mapped)
    return create_image(smoothed)


def encode_frame(frame):
    """
    Encode the input frame as a JPEG image and return it as a base64-encoded
    string.
    :param frame: Input frame
    :return: Base64-encoded JPEG image
    """
    frame_str = cv2.imencode(".jpg", frame)[1].tostring()
    return base64.b64encode(frame_str).decode("utf-8")