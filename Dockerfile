# syntax = docker/dockerfile:1
ARG CUDA_TAG=11.4.19-devel
FROM nvcr.io/nvidia/l4t-cuda:$CUDA_TAG

#
# Base image prep
#
ARG INDUSTRIALNEXT_PY_INDEX=""
ARG PYTHON_VERSION=3.10
ARG PYTHON_BIN=python$PYTHON_VERSION

RUN apt-get update -qq
RUN apt-get install -qqy software-properties-common

# Install deadsnakes ppa for a real python
RUN add-apt-repository -y ppa:deadsnakes/ppa
RUN apt-get update -qq && apt-get upgrade -qqy
RUN apt install -qqy build-essential python$PYTHON_VERSION python$PYTHON_VERSION-dev \
        python3-setuptools python3-wheel python$PYTHON_VERSION-distutils
RUN apt install -qqy libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev libgtk2.0-dev

# Update pip
ARG PIP_LOCAL=/tmp/get-pip.py
ADD https://bootstrap.pypa.io/get-pip.py $PIP_LOCAL
RUN $PYTHON_BIN $PIP_LOCAL; rm -f $PIP_LOCAL

RUN apt-get clean autoclean; apt-get autoremove --yes; rm -rf /var/lib/{apt,dpkg,cache,log}/
WORKDIR /app

#
# Copy in and run setup scripts
# Copy them separately so changes in one don't rerun both
#
COPY ./install_dep.sh .
RUN PYTHON_BIN=$PYTHON_BIN ./install_dep.sh
COPY ./install_industrialnext_deps.sh .
COPY ./requirements.txt .
RUN PYTHON_BIN=$PYTHON_BIN INDUSTRIALNEXT_PY_INDEX=$INDUSTRIALNEXT_PY_INDEX ./install_industrialnext_deps.sh
RUN rm -v *.sh requirements.txt

#
# Cleanup and setup running application
#
COPY *.py .
ENTRYPOINT ["python3.10", "run.py"]
