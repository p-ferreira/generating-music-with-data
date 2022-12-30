#!/bin/bash

# set URL variables
MUSIC_TRANSFORMERS_WEIGHTS="https://dl.dropboxusercontent.com/s/05jzbhgub7gtyif/music-transformers-model-ckpt.zip"
SOUND_FOUNT_URL="https://dl.dropboxusercontent.com/s/qfi8tfs5ljp68my/Yamaha-C5-sound-font.zip"


# download the assets with curl
echo "Downloading model weights and soundfont..."
curl -L $MUSIC_TRANSFORMERS_WEIGHTS --output "bin/music-transformers-model-ckpt.zip"
curl -L $SOUND_FOUNT_URL --output "bin/sound-font.zip"

# unzip files
echo "Unzipping assets..."
unzip -o "bin/music-transformers-model-ckpt.zip" -d "bin/"
unzip -o "bin/sound-font.zip" -d "bin/soundfont"


# remove zip files
echo "Removing zip files..."
rm -rf "bin/music-transformers-model-ckpt.zip"
rm -rf "bin/sound-font.zip"
