import argparse
from pathlib import Path
import logging

import cv2
import industrialnext.alpha_camera as camera
import tomli as toml
from ultralytics import YOLO


def parse_args():
    parser = argparse.ArgumentParser(
        description="SDK 1.0 Alpha",
    )
    parser.add_argument(
        "-c",
        "--config",
        type=Path,
        help="Path to config file",
    )
    parser.add_argument(
        "--print-camera-modes",
        action="store_true",
        help="Print camera modes and exit"
    )
    return parser.parse_args()


def read_config(file_path: str):
    mode: str = "rb"
    try:
        with open(file_path, mode) as f:
            config = toml.load(f)
    except FileNotFoundError as _ex:
        logger.error("Config file [%s] not found.", file_path)
    return config

def camera_setup(config):
    _, params = config["cameras"].items()[0]
    cfg = CameraConfig()
    cfg.configure(params)
    camera = Camera.from_config(cfg)
    return camera

def run(camera) -> None:
    model = yolo_inference.get_torch_model(yolo_inference.yolo_model)
    while True:
        frame = frame_buf.peek()
        results = model(frame)

        # Customer logic here!


def main():
    args = parse_args()
    if args.print_camera_modes:
        camera.print_cybersight_modes()
        return
    elif args.config is not None:
        config = read_config(args.conf)
        print("Success!")
    else:
        parser.print_help()
    #cam_buf = camera_setup(config["camera"])
    #run(cam_buf)

if __name__ == "__main__":
    main()

