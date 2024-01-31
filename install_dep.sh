#!/bin/bash

set -e

# Use pyenv python3.10 by default
ENV_NAME=${ENV_NAME:=py310}
PYTHON_BIN=${PYTHON_BIN:=$HOME/.pyenv/versions/${ENV_NAME}/bin/python}

# Install tensorRT
SUDO=$(if which sudo &>/dev/null; then echo "sudo"; else echo ""; fi)
$SUDO apt install -y tensorrt nvidia-tensorrt-dev python3-pip

# Install ultralytics==8.0.176 and onnx
${PYTHON_BIN} -m pip install --no-deps ultralytics==8.0.176
${PYTHON_BIN} -m pip install "onnx>=1.12.0"
