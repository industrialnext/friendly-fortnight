# syntax = docker/dockerfile:1
ARG CUDA_TAG=11.4.19-devel
FROM nvcr.io/nvidia/l4t-cuda:$CUDA_TAG

WORKDIR /app

COPY . .

RUN apt update -qq
RUN ./pyenv_setup.sh -i
ENV PATH=$HOME/.pyenv/bin:$PATH
RUN  ./pyenv_setup.sh -s
#
RUN ./install_dep.sh
RUN pyenv activate py310

# reduce image size
#RUN apt-get clean autoclean; apt-get autoremove --yes; rm -rf /var/lib/{apt,dpkg,cache,log}/
#CMD ["python", "cybersight_sample.h", "-h"]
