#!/bin/bash

# set URL variables
CUSTOM_GPT2_MODEL_WEIGHTS_URL="https://dl.dropboxusercontent.com/s/o9368dgk4qz482p/custom-gpt2-model-ckpt.zip"
SOUND_FOUNT_URL="https://dl.dropboxusercontent.com/s/qfi8tfs5ljp68my/Yamaha-C5-sound-font.zip"

# download the assets with curl
echo "Downloading model weights and soundfont..."
curl -L $CUSTOM_GPT2_MODEL_WEIGHTS_URL --output "bin/custom-gpt2-model-ckpt.zip"
curl -L $SOUND_FOUNT_URL --output "bin/sound-font.zip"

# unzip files
echo "Unzipping assets..."
unzip "bin/custom-gpt2-model-ckpt.zip" -d "bin/"
unzip "bin/sound-font.zip" -d "bin/soundfont"

# rename checkpoint folder
mv "bin/custom-gpt2-model-ckpt" "bin/checkpoints"

# remove zip files
echo "Removing zip files..."
rm -rf "bin/custom-gpt2-model-ckpt.zip"
rm -rf "bin/sound-font.zip"
