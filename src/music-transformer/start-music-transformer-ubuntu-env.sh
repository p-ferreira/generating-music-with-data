#!/bin/bash

# This script is used to start a python environment with all the dependencies for the GPT-2 music generation scripts

# Docker run Parameters:
# --rm = automatically remove the container when it exits
# -it = interactive
# -p 8888:8888 = map port 8888 on the host to port 8888 in the container
# -v "${PWD}":/usr/src/app = map the current directory on the host to /usr/src/app in the container
# -w /usr/src/app = set the working directory in the container to /usr/src/app 
# huggingface/transformers-pytorch-gpu = the image to use
# pip install jupyterlab = install jupyterlab
# jupyter notebook --ip 0.0.0.0 --no-browser --allow-root = start jupyter notebook


DOCKER_IMAGE='music-transformer-env'

docker run \
    --rm \
    -it \
    -p 8888:8888 \
    -v "${PWD}":/usr/src/app \
    -w /usr/src/app \
    "${DOCKER_IMAGE}"


