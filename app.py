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