""" Industrial Next "Alpha" SDK

DO NOT MODIFY.

This file contains simple scaffolding for running a Cybersight application.
Unless you need to change functionality related to command line arguments,
the configuration file, or opening the camera, this file should NOT need
to be modified.

"""
import argparse
import logging
from pathlib import Path
import sys
from time import sleep
from typing import Optional

import industrialnext.alpha_camera as camlib
import tomli as toml

from app import run

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def parse_args() -> Optional[dict]:
    """
    Parse configuration based on CLI args.
    Return config dict if we can, else None.
    """
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
        "--print-camera-modes", action="store_true", help="Print camera modes and exit"
    )
    args = parser.parse_args()
    if args.print_camera_modes:
        camlib.print_cybersight_modes()
        return None
    config = read_config(args.config)
    return config


def read_config(file_path: str) -> Optional[dict]:
    """
    Given a toml file, return the dictionary contained.
    """
    mode: str = "rb"
    try:
        with open(file_path, mode) as f:
            config = toml.load(f)
    except FileNotFoundError as _ex:
        logger.error("Config file [%s] not found.", file_path)
        config = None
    return config


def camera_setup(config: dict) -> camlib.Camera:
    """
    Given a camera configuration dict, return camera instance.
    """
    cfg = camlib.Config(config)
    my_camera = camlib.Camera.from_config(cfg)
    my_camera.start()
    return my_camera


def main() -> None:
    config = parse_args()
    if config is None:
        return
    if "application" not in config:
        logger.fatal("No application section in config, exiting")
    else:
        logger.info("Launching application...")
        camera = camera_setup(config["cameras"]["cybersight-cam-0"])
        run(camera, config["application"])
        logger.info("Stopping imager")
        camera.stop()


if __name__ == "__main__":
    main()
