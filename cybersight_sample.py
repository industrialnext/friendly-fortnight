#!/usr/bin/env python3
# Copyright 2023 Industrial Next, Inc.  All rights reserved.
# cybersight_sample.py
# Requires:
# - Python>=3.10.
# - opencv-contrib-python with Gstreamer enabled
# This script is provided with an Industrial Next Cybersight to demonstrate
# camera usage.

import argparse
import cv2

SENSOR: str = "imx283"

ROTATION_OPTS = {0: 0, 90: 3, 180: 2, 270: 1}

# Nano-second
#DEFAULT_EXPO_T_RANGE_LIM = (13000, 683709000) # imx577
DEFAULT_EXPO_T_RANGE_LIM = (52000, 49865000) # imx283
DEFAULT_A_GAIN_RANGE_LIM = (1, 22.25)
DEFAULT_ISP_GAIN_RANGE_LIM = (1, 256.0)
DEFUALT_WB_MODE_RANGE_LIM = (0, 10)  # Inclusive, exclusive
DEFUALT_EE_MODE_RANGE_LIM = (0, 3)  # Inclusive, exclusive
DEFAULT_EE_STRENGTH_RANGE_LIM = (-1, 1)
DEFAULT_EXPO_COMP_RANGE_LIM = (-2, 2)
DEFAULT_SATURATION_RANGE_LIM = (0, 2)
DEFAULT_TNR_MODE_RANGE_LIM = (0, 3)  # Inclusive, exclusive
DEFAULT_TNR_STRENGTH_RANGE_LIM = (-1, 1)
DEFAULT_WBMODE = 0
DEFAULT_EEMODE = 1
DEFAULT_EE_STRENGTH = -1
DEFAULT_EXPO_COMP = 0
DEFAULT_SATURATION = 1
DEFAULT_TNR_MODE = 1
DEFAULT_TNR_STRENGTH = -1


class CaptureMode:
    def __init__(self, width, height, fps, desc):
        self.height = height
        self.width = width
        self.desc = desc
        self.fps = fps

    @property
    def mode_values(self):
        return [self.width, self.height, self.fps]


SENSOR_MODES = {
    "imx283": {
        0: CaptureMode(
            5472,
            3648,
            20,
            "5472 x 3648 @ 20 fps, type 1, 12-bit A/D conversion and length output",
        ),
        1: CaptureMode(
            5472,
            3648,
            25,
            "5472 x 3648 @ 25 fps, type 1, 10-bit A/D conversion and length output",
        ),
        2: CaptureMode(
            2736,
            1824,
            50,
            "2736 x 1824 @ 50 fps, type 1, 10-bit A/D conversion, "
            + "12-bit length output, horizontal/vertical 2/2-line binning",
        ),
        3: CaptureMode(
            1824,
            1216,
            60,
            "1824 x 1216 @ 60 fps, type 1, 9-bit A/D conversion, "
            + "12-bit length output, horizontal/vertical 3/3-line binning",
        ),
        4: CaptureMode(
            3840,
            2160,
            60,
            "3840 x 2160 @ 60 fps, type 1/1.4, 10-bit A/D conversion and length output",
        ),
    },
    "imx577": {
        0: CaptureMode(4056, 3040, 40, "4056 x 3040 @ 40 fps, 10-bit A/D conversion"),
        1: CaptureMode(
            4056, 2288, 40, "4056 x 2288 @ 40 fps, 10-bit A/D conversion, vertical crop"
        ),
        2: CaptureMode(
            2024,
            1144,
            60,
            "2024 x 1144 @ 60 fps, 10-bit A/D conversion, "
            + "vertical crop, horizontal/vertical 2/2 scaling",
        ),
        3: CaptureMode(
            2028,
            1520,
            130,
            "2028 x 1520 @ 130 fps, 10-bit A/D conversion, "
            + "horizontal/vertical 2/2-line binning",
        ),
        4: CaptureMode(
            2028,
            1112,
            240,
            "2028 x 1112 @ 240 fps, 10-bit A/D conversion, "
            + "vertical crop, horizontal/vertical 2/2-line binning",
        ),
        5: CaptureMode(
            4056, 3040, 15, "4056 x 3040 @  15 fps, DOL-HDR, 10-BIT A/D conversion"
        ),
        6: CaptureMode(
            4056,
            2288,
            30,
            "4056 x 2288 @  30 fps, DOL-HDR, 10-BIT A/D conversion vertical crop",
        ),
    },
}

def type_range(mi, ma, data_type):
    if data_type not in (int, float):
        raise argparse.ArgumentTypeError(
            f"Unspported data type in range check: {data_type}"
        )

    def range_checker(value):
        try:
            v = data_type(value)
        except ValueError:
            raise argparse.ArgumentTypeError(f"Value must be an {data_type}")

        if v < mi or v > ma:
            raise argparse.ArgumentTypeError(f"Value must be <= {ma} and >= {mi}")
        return v

    return range_checker


def gstreamer_pipeline(args) -> str:
    width, height, fps = SENSOR_MODES[SENSOR][args.sensor_mode].mode_values

    if args.frame_rate > 0:
        fps = args.frame_rate

    exposure_time_range = args.exposure_range
    has_exposure_range = exposure_time_range
    if has_exposure_range:
        exposure_min, exposure_max = args.exposure_range
        exposure_time_range = (
            f'exposuretimerange="{exposure_min} {exposure_max}"'
        )
        print(exposure_time_range)

    digital_gain_range = ""
    if args.isp_d_gain_range is not None:
        digital_gain_min, digital_gain_max = args.isp_d_gain_range
        digital_gain_range = f'ispdigitalgainrange="{digital_gain_min} {digital_gain_max}"'
        print(digital_gain_range)

    gain_range = ""
    has_gain = args.a_gain_range is not None
    if has_gain:
        gain_min, gain_max = args.a_gain_range
        gain_range = f'gainrange="{gain_min} {gain_max}"'
        print(digital_gain_range)

    assert args.flip in ROTATION_OPTS

    return (
        f"nvarguscamerasrc sensor-mode={args.sensor_mode} "
        f"wbmode={args.wb_mode} "
        f"ee-mode={args.ee_mode} ee-strength={args.ee_strength} "
        f"tnr-mode={args.tnr_mode} tnr-strength={args.tnr_strength} "
        f"{digital_gain_range} {gain_range} "
        f"saturation={args.saturation} "
        f"exposurecompensation={args.expo_compensation} aelock={args.aelock} {exposure_time_range} ! "
        f"video/x-raw(memory:NVMM), "
        f"width=(int){width}, height=(int){height}, "
        f"format=(string)NV12, framerate=(fraction){fps}/1 ! "
        f"nvvidconv flip-method={ROTATION_OPTS[args.flip]} ! "
        f"video/x-raw, width=(int){width}, height=(int){height}, format=(string)BGRx ! "
        f"videoconvert ! "
        f"video/x-raw, format=(string)BGR ! appsink max-buffers=1 drop=True"
    )


def print_cybersight_modes():
    print("Showing all available Cybersight sensor modes:\n")
    for sensor, modes in SENSOR_MODES.items():
        print(f"{sensor}: ")
        for mode_ind, mode in SENSOR_MODES[sensor].items():
            print(f"    {mode_ind}: {mode.desc}")
        print()


def parse_cam_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--show-sensor-modes",
        action="store_true",
        help="Print all sensor modes and exit",
    )
    parser.add_argument(
        "-sm",
        "--sensor-mode",
        type=int,
        default=0,
        help="Specify a sensor mode number",
    )
    parser.add_argument(
        "-fps",
        "--frame-rate",
        default=0,
        type=int,
        help="Specify capture frame rate (fps)",
    )
    parser.add_argument(
        "-ael",
        "--aelock",
        action="store_true",
        help=f"Provide this flag to enable auto-exposure lock, default disabled",
    )
    parser.add_argument(
        "-er",
        "--exposure-range",
        default=DEFAULT_EXPO_T_RANGE_LIM ,
        nargs=2,
        type=int,
        metavar=("LOW", "HIGH"),
        help=(
            f"Set exposure time range low and high in nano-sec. If low and high are the same, "
            f"it's set to that specific value. e.g 50000000 50000000 or 34000 358733000, "
            f"[min, max] = {list(DEFAULT_EXPO_T_RANGE_LIM)}"
        ),
    )
    parser.add_argument(
        "-ag",
        "--a-gain-range",
        default=None,
        nargs=2,
        type=float,
        metavar=("LOW", "HIGH"),
        help=(
            f"Set gain range low and high. e.g 15 15 or 1 16, "
            f"[min, max] = {list(DEFAULT_A_GAIN_RANGE_LIM)}"
        ),
    )
    parser.add_argument(
        "-dg",
        "--isp-d-gain-range",
        default=None,
        nargs=2,
        type=float,
        metavar=("LOW", "HIGH"),
        help=(
            f"Set ISP digital gain range low and high. e.g 12 12 or 1 256, "
            f"[min, max] = {list(DEFAULT_ISP_GAIN_RANGE_LIM)}"
        ),
    )
    parser.add_argument(
        "-wbm",
        "--wb-mode",
        default=DEFAULT_WBMODE,
        type=int,
        choices=range(*DEFUALT_WB_MODE_RANGE_LIM),
        metavar="wb_mode (0-9)",
        help=(
            "Set white balance mode. "
            "0: off (default), "
            "1: auto, "
            "2: incandescent, "
            "3: fluorescent, "
            "4: warm-fluorescent, "
            "5: daylight, "
            "6: cloudy-daylight, "
            "7: twilight, "
            "8: shade, "
            "9: manual"
        ),
    )
    parser.add_argument(
        "-em",
        "--ee-mode",
        default=DEFAULT_EEMODE,
        type=int,
        choices=range(*DEFUALT_EE_MODE_RANGE_LIM),
        metavar="ee_mode",
        help=(
            f"Set edge enhnacement mode. "
            f"Defualt: {DEFAULT_EEMODE}, available values: "
            f"0: EdgeEnhancement_Off, "
            f"1: EdgeEnhancement_Fast, "
            f"2: EdgeEnhancement_HighQuality"
        ),
    )
    parser.add_argument(
        "-es",
        "--ee-strength",
        type=type_range(
            DEFAULT_EE_STRENGTH_RANGE_LIM[0],
            DEFAULT_EE_STRENGTH_RANGE_LIM[1],
            float,
        ),
        default=DEFAULT_EE_STRENGTH,
        help=(
            f"Adjust edge enhancement strength, value is between "
            f"{DEFAULT_EE_STRENGTH_RANGE_LIM}"
        ),
    )
    parser.add_argument(
        "-ec",
        "--expo-compensation",
        type=type_range(
            DEFAULT_EXPO_COMP_RANGE_LIM[0],
            DEFAULT_EXPO_COMP_RANGE_LIM[1],
            float,
        ),
        default=DEFAULT_EXPO_COMP,
        help=(
            f"Adjust exposure compensation, value is between "
            f"{DEFAULT_EXPO_COMP_RANGE_LIM}"
        ),
    )
    parser.add_argument(
        "-sa",
        "--saturation",
        type=type_range(
            DEFAULT_SATURATION_RANGE_LIM[0],
            DEFAULT_SATURATION_RANGE_LIM[1],
            float,
        ),
        default=DEFAULT_SATURATION,
        help=(
            f"Adjust saturation, value is between "
            f"{DEFAULT_SATURATION_RANGE_LIM}"
        ),
    )
    parser.add_argument(
        "-tm",
        "--tnr-mode",
        default=DEFAULT_TNR_MODE,
        type=int,
        choices=range(*DEFAULT_TNR_MODE_RANGE_LIM),
        metavar="tnr_mode",
        help=(
            f"Set temporal noise reduction mode. "
            f"Defualt: {DEFAULT_TNR_MODE}, available values: "
            f"0: NoiseReduction_Off, "
            f"1: NoiseReduction_Fast, "
            f"2: NoiseReduction_HighQuality"
        ),
    )
    parser.add_argument(
        "-ts",
        "--tnr-strength",
        type=type_range(
            DEFAULT_TNR_STRENGTH_RANGE_LIM[0],
            DEFAULT_TNR_STRENGTH_RANGE_LIM[1],
            float,
        ),
        default=DEFAULT_TNR_STRENGTH,
        help=(
            f"Adjust temporal noise reduction strength, value is between "
            f"{DEFAULT_TNR_STRENGTH_RANGE_LIM}"
        ),
    )
    parser.add_argument(
        "--flip",
        type=type_range(
            min(ROTATION_OPTS.keys()),
            max(ROTATION_OPTS.keys()),
            int
        ),
        default=0,
        help=(
            "Specify flip of the image in 90-degree increments"
        ),
    )

    try:
        args = parser.parse_args()
    except AttributeError:
        print("Bad usage.")
        traceback.print_exc()
        parser.print_help()

    if args.show_sensor_modes:
        print_cybersight_modes()
        exit()

    if args.sensor_mode < 0 or args.sensor_mode >= len(
        SENSOR_MODES["imx577"]
    ):
        print(f"Invalid sensor mode {args.sensor_mode} for {args.sensor_model}")
        exit()

    return args


def open_stream(pipeline_str: str) -> cv2.VideoCapture | None:
    print("Opening gstreamer pipeline with:")
    print(pipeline_str)
    return cv2.VideoCapture(pipeline_str, cv2.CAP_GSTREAMER)


if __name__ == "__main__":
    args = parse_cam_args()
    pipeline = gstreamer_pipeline(args)
    cap = open_stream(pipeline)
    if not cap.isOpened():
        print("Failed to open stream")
        exit()
    try:
        while cap.isOpened():
            ret, frame = cap.read()
            cv2.imshow("Video stream", frame)
            # if the 'q' key was pressed, break from the loop
            if cv2.waitKey(10) & 0xFF == ord("q"):
                break
    except cv2.error as e:
        print(e)
        if "Can't initialize GTK backend" in str(e):
            print("Unable to open window for showing stream preview. Is a display available?")
