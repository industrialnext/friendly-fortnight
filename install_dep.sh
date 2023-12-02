#!/bin/bash

# Install tensorRT
sudo apt install -y tensorrt nvidia-tensorrt-dev

ENV_NAME="py310"

python_bin=$HOME/.pyenv/versions/${ENV_NAME}/bin/python

# Install ultralytics==8.0.176 and onnx
${python_bin} -m pip install --no-deps ultralytics==8.0.176
${python_bin} -m pip install "onnx>=1.12.0"
