""" Customer's application for Alpha SDK.

This file contains a method imported and run by the SDK. All that is required 
is a function named "run" that takes two arguments, one for a camera handle 
and for a dictionary containing configuration values.

Any customer dependencies should also be imported here. The sample runs a YoloV8
sample model. 
"""

import logging
from time import sleep

import yolo_inference

logger = logging.getLogger(__name__)

def run(camera, config) -> None:
    model = yolo_inference.get_torch_model(yolo_inference.yolo_model)

    try:
        iters = int(config["iterations"])
    except TypeError:
        logger.fatal("iterations must be an integer")
        return

    for i in range(iters):
        if camera.running():
            frame = camera.latest_frame()
            results = model(frame)
            logger.info(results)
            sleep(1)
        else:
            logger.warn("Stream is not open; exiting...")