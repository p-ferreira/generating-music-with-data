# Music Transformers

## Download model weights and soundfont

First of all you need to download the model weights for the model and the soundfont. 

You can set everything up by running the `download-assets.sh` script. This will download the model weights and the soundfont for the MIDI output.

```bash
bash download-assets.sh
```

You can also do it manually, by downloading the model weights from [this link](https://dl.dropboxusercontent.com/s/05jzbhgub7gtyif/music-transformers-model-ckpt.zip), as well as the [SoundFont](https://dl.dropboxusercontent.com/s/qfi8tfs5ljp68my/Yamaha-C5-sound-font.zip) for the MIDI output.

> Note: To download the original model weights from google, check the README file at [scripts/manual-setup](scripts/manual-setup/README.md)


## Setting up the environment

### Docker environment

The easiest way to start the environment is by using docker. 
You can use the following commands to create and start the docker environment:

```bash
# Create docker image
bash build-docker-environment.sh

# Start docker image
bash start-music-transformer-ubuntu-env.sh
```

This will start a docker ubuntu machine with all the dependencies needed. 
The script exposes port 8888, so you can access the jupyter notebooks from your browser.

The best way to interact with the system is through jupyter lab, which you can start by accessing the URL http://localhost:8888/lab/

> Note: Ensure that python interpreter is set to the `music-transformers-env` environment.

### Local environment

Create the conda environment for the music transformer:

**Create python conda environment:**
```bash
conda env create -f music-transformer-env.yml
``` 

**Activate the created environment:**
```bash
conda activate music-transformer-env
```

This will set the environment with the right versions of the dependencies.
 > Note:
> The version of the dependencies are based on the original notebook [Generating Piano Music with Transformer.ipynb](https://colab.research.google.com/notebooks/magenta/piano_transformer/piano_transformer.ipynb)

Unfortunately, the `tensor2tensor` library does not work out of the box with the given dependencies.

The current workaround is to apply the changes directly at the downloaded library source code as implemented in the [PR 1908](https://github.com/tensorflow/tensor2tensor/pull/1908/files)

You can get the main directory of the repository with the following command

```bash
python -m site --user-site tensor2tensor
```

The file `tensor2tensor/rl/gym_utils` should be replaced with the file `gym_utils.py` located at the root of the `src/music-transformer/scripts` directory.

If you are running on linux, you will need to install some other dependencies with the following command:
```bash
apt-get install -y fluidsynth libsndfile1 libasound2-dev libjack-dev
```


After creating the environment and replacing the mentioned file, you should be set to run the notebook without further problems.

## How to generate music with the model

To explore the models and generate samples with it, open the notebook
located at [`notebooks/generate-music-with-transformers.ipynb`](notebooks/generate-music-with-transformer.ipynb).