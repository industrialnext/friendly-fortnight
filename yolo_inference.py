from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator

import cv2
import urllib.request
import numpy as np
import torch


test_img_url = "https://ultralytics.com/images/bus.jpg"
yolo_model = "yolov8n-pose.pt"


def load_test_img_url(url):
    req = urllib.request.urlopen(url)
    arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
    
    return cv2.imdecode(arr, -1)


def get_torch_model(model_name):
    # Load a model
    model = YOLO(model_name)
    
    # Move model to gpu
    model.to("cuda")

    return model


def convert_model_to_engine():
    # Load a model
    model = YOLO(yolo_model)
    model.export(format="engine")


def create_annotator(img_shape):
    return Annotator(np.zeros(img_shape))


def update_annotator_img(annotator, img):
    annotator.im = img


def annotate_keypoints(annotator, kpt_results):
    for r in kpt_results:
        if r.keypoints.xy.nelement() and r.keypoints.conf != None:
            for i in range(r.keypoints.shape[0]):
                conf = torch.unsqueeze(r.keypoints.conf[i], dim=1)
                ktps = torch.cat((r.keypoints.xy[i], conf), 1)
                annotator.kpts(ktps, shape=r.keypoints.orig_shape, kpt_line=True)


if __name__ == "__main__":
    img = load_test_img_url(test_img_url)

    model = get_torch_model(yolo_model)

    # Predict
    results = model(img)
    
    annotator = create_annotator(img.shape)
    update_annotator_img(annotator, img)

    # View results
    annotate_keypoints(annotator, results)
    img = annotator.result()

    cv2.imshow('yolov8_detection', img)
    if cv2.waitKey() & 0xFF == 27:
        pass
