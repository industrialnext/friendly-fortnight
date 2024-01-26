import argparse
import logging
from pathlib import Path
from time import sleep
import sys

import cv2
import industrialnext.alpha_camera as camlib
import tomli as toml
from ultralytics import YOLO

import yolo_inference

logger = logging.getLogger(__name__)

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
        config = None
    return config

def camera_setup(config):
    cfg = camlib.Config(config)
    my_camera = camlib.Camera.from_config(cfg)
    my_camera.start()
    return my_camera

def run(camera) -> None:
    model = yolo_inference.get_torch_model(yolo_inference.yolo_model)
    while camera.running():
        frame = camera.latest_frame()
        results = model(frame)
        print(results)
        sleep(1)
    print("Stream is not open; exiting...")


def main():
    args = parse_args()
    if args.print_camera_modes:
        camera.print_cybersight_modes()
        return
    elif args.config is not None:
        config = read_config(args.config)
        if config is not None:
            print("Launching application...")
            camera = camera_setup(config["cameras"]["cybersight-cam-0"])
            run(camera)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()

