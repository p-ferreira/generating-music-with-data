#!/bin/bash

# Create directories
mkdir -p bin/checkpoints
mkdir -p bin/primers
mkdir -p bin/soundfonts

docker run --rm -v `pwd`/:/music-transformers -it gcr.io/google.com/cloudsdktool/google-cloud-cli
