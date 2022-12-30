#!/bin/bash

echo "Downloading primers..."
gsutil -q -m cp -r gs://magentadata/models/music_transformer/primers/* bin/primers
echo "Primers downloaded"

echo "Downloading checkpoints..."
gsutil -q -m cp -r gs://magentadata/models/music_transformer/checkpoints/* bin/checkpoints
echo "Checkpoints downloaded"

echo "Downloading Soundfont..."
gsutil -q -m cp gs://magentadata/soundfonts/Yamaha-C5-Salamander-JNv5.1.sf2 bin/soundfonts