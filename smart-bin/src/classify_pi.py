#!/usr/bin/env python3
"""
Real-time image classification using TFLite.

Loads the TFLite model at models/model.tflite, captures frames from the default webcam,
performs inference to classify waste into one of four bins,
prints the class names, and dispatches hardware control via
hardware_control.pick_bin().

Use `--debug` to display the video with overlaid predictions (press 'q' to quit).
"""
import time
import argparse
from pathlib import Path
import cv2
import numpy as np

# Attempt to use tflite_runtime if installed, otherwise fall back to TensorFlow's Interpreter
try:
    from tflite_runtime.interpreter import Interpreter as TFLiteInterpreter
    print("[Info] Using tflite_runtime Interpreter")
    import tensorflow as tf  # needed for preprocess (float32 path)
except ImportError:
    import tensorflow as tf
    TFLiteInterpreter = tf.lite.Interpreter
    print("[Info] Using TensorFlow Lite Interpreter")

import hardware_control as hw

# Constants
IMG_SIZE = 224
LABELS = Path("data/labels.txt").read_text().splitlines()

# Load TFLite model
tflite_model_path = "models/model.tflite"
interpreter = TFLiteInterpreter(model_path=tflite_model_path)
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
input_index = input_details[0]['index']
output_index = output_details[0]['index']
input_dtype = input_details[0]['dtype']

# Prepare preprocessing function based on expected dtype
def preprocess_image(img: np.ndarray) -> np.ndarray:
    """Resize and cast image to the model's expected dtype, applying scaling if float32."""
    img_resized = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
    if input_dtype == np.uint8:
        return img_resized.astype(np.uint8)
    else:
        # Convert to float32 and apply MobileNetV3 preprocessing
        img_f32 = img_resized.astype(np.float32)
        return tf.keras.applications.mobilenet_v3.preprocess_input(img_f32)


def predict(frame: np.ndarray) -> int:
    """Preprocesses the frame, runs inference, and returns the class index."""
    tensor = preprocess_image(frame)
    tensor = np.expand_dims(tensor, axis=0).astype(input_dtype)
    interpreter.set_tensor(input_index, tensor)
    interpreter.invoke()
    output = interpreter.get_tensor(output_index)[0]
    return int(np.argmax(output))


def main(debug: bool = False):
    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        print("Error: Unable to open camera")
        return
    try:
        while True:
            ret, frame = cam.read()
            if not ret:
                continue
            cls_id = predict(frame)
            cls_name = LABELS[cls_id]
            print(f"Predicted: {cls_name}")
            hw.pick_bin(cls_name)

            if debug:
                cv2.putText(frame, cls_name, (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv2.imshow("Classification", frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                time.sleep(0.5)
    finally:
        cam.release()
        if debug:
            cv2.destroyAllWindows()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action="store_true",
                        help="Display camera feed with overlay")
    args = parser.parse_args()
    main(debug=args.debug)
