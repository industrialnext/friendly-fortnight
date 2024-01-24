import argparse
from pathlib import Path
import logging

import cv2
from industrialnext.camera import config as CameraConfig, Camera
from industrialnext.camera import print_cybersight_modes
import tomli as toml
import yolo_inference

def parse_args():
    parser = argparse.ArgumentParser(
        description="SDK 1.0 Alpha",
    )
    parser.add_argument(
        "-c",
        "--config",
        type=Path,
        required=True,
        help="Path to config file",
    )
    parser.add_argument(
        "--print-camera-codes",
        action="store_true",
        help="Print camera modes and exit"
    )
    return args


def read_config(file_path: str):
    mode: str = "rb"
    try:
        with open(file_path, mode) as f:
            config = toml.load(f)
    except FileNotFoundError as _ex:
        logger.error("Config file [%s] not found.", file_path)
    return config

def camera_setup(config) -> buffer:
    _, params = config["cameras"].items()[0]
    cfg = CameraConfig()
    cfg.configure(params)
    camera = Camera.from_config(cfg)
    camera.start()
    return camera.buffer()

def main():
    args = parse_args()
    if args.print_camera_modes:
        print_cybersight_modes()
        return
    config = read_config(args.conf)
    cam_buf = camera_setup(config["camera"])
    run(cam_buf)

def run(cam_buf: buffer) -> None:
    model = yolo_inference.get_torch_model(yolo_inference.yolo_model)
    while True:
        frame = frame_buf.peek()
        results = model(frame)

        # Customer logic here!


if __name__ == "__main__":
    main()

