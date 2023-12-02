# friendly-fortnight

Sample code that runs yolov8 pose model on CyberSight camera stream

## Scripts
- pyenv_setup.sh: a shell script that installs or sets up a pyenv environment
- install_dep.sh: a shell script that installs YoloV8 dependencies
- yolo_inference.py: a script that has function wrappers and a sample yolov8 test on an example image
- cybersight_sample.py: an example script that gets a continuous image stream from the cybersight camera using gstreamer
- cybersight_yolo.py: an example script that runs yolov8 model inference on an image stream from the cybersight camera

## Usage
```sh
# To set up pyenv
$ ./pyenv_setup.sh -i|-s

# To install YoloV8 dependencies
$ ./install_dep.sh

# To run scripts
$ pyenv activate py310
$ python cybersight_yolo.py

# See help menu
$ python cybersight_yolo.py -h
```
