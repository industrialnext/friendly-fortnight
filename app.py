""" Customer's application for Alpha SDK.

This file contains a function imported and run by the SDK. All that is required
is a function named "run" that takes two arguments, one for a camera handle
and for a dictionary containing configuration values.

Any customer dependencies should also be imported here. The sample runs a YoloV8
sample model.
"""

import logging
import os
from pathlib import Path
from time import sleep

import cv2

import yolo_inference

logger = logging.getLogger("sdk")
logger.setLevel(logging.INFO)

def run(camera, config) -> None:

    """
    Perform configuration validation
    """
    expected_params = {
        "iterations": int,
        "output-dir": str,
    }
    for param, t in expected_params.items():
        try:
            t(config[param])
        except (KeyError, TypeError):
            logger.fatal("Expected config to contain a %s named %s",
                      t, param)
            return

    iters = int(config["iterations"])
    output_dir = config["output-dir"]

    # Check our output dir is real
    if not os.path.exists(output_dir):
        logger.fatal("Expected output path to exist; exiting")
        return

    """
    YOLO prep
    """
    model = yolo_inference.get_torch_model(yolo_inference.yolo_model)
    if camera.running():
        try:
            img_shape = camera.latest_frame().shape[:1]
        except AttributeError:
            logger.fatal("Failed to acquire frame. Try restarting Argus daemon.")
            return
        annotator = yolo_inference.create_annotator(img_shape)
    else:
        logger.fatal("Camera not open, exiting")

    """
    Application loop
    """
    for i in range(iters):
        if camera.running():
            frame = camera.latest_frame()
            results = model(frame)
            logger.info(results)
            yolo_inference.update_annotator_img(annotator, frame)
            yolo_inference.annotate_keypoints(annotator, results)
            frame = annotator.result()
            cv2.imwrite(str(Path(output_dir, f"{i + 1}.png")), frame)
            logger.info("Write %d...", i)
            sleep(1)
        else:
            logger.warn("Stream is not open; exiting...")
