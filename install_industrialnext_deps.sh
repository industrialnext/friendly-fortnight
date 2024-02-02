#!/usr/bin/env bash

set -e

ENV_NAME=${ENV_NAME:py310}
PYTHON_BIN=${PYTHON_BIN:=$HOME/.pyenv/versions/$ENV_NAME/bin/python}

# Ensure we have the credentials available
[ -n "$INDUSTRIALNEXT_PY_INDEX" ] || { echo "Error: 'INDUSTRIALNEXT_PY_INDEX' is not set. Please see the documentation" >&2; exit 1; }

${PYTHON_BIN} -m pip install -i ${INDUSTRIALNEXT_PY_INDEX} -r requirements.txt
