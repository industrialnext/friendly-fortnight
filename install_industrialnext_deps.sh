#!/usr/bin/env bash

set -e

ENV_NAME=${ENV_NAME:py310}
PYTHON_BIN=${PYTHON_BIN:$HOME/.pyenv/versions/$ENV_NAME/bin/python}

# Ensure we have the credentials available
[ -n "$INDUSTRIALNEXT_PY_INDEX" ] || { echo "Error: 'INDUSTRIALNEXT_PY_INDEX' is not set. Please see the README.md" >&2; exit 1; }

echo Using $PYTHON_BIN
${PYTHON_BIN} -m pip install -i ${INDUSTRIALNEXT_PY_INDEX} \
    opencv-contrib-python==4.7.0.72+industrialnext \
    industrialnext.alpha_camera
