# Custom GPT-2

## Directory

```bash
├── bin # folder where you should add the model weights
├── build-docker-environment.sh # builds the docker image with all the python dependencies
├── create-custom-gpt2-env.sh # script to create a conda environment using an .yml env file
├── custom-gpt2-env.yml # Conda environment for custom-gpt2
├── Dockerfile # Dockerfile for construction of custom-gpt2-env image
├── make_maestro_split_raw_dataset.py # Script to engineer split in training data
├── make_token_sequence_dataset.py # Script to create a token sequence dataset
├───notebooks   
   ├── model-metrics.csv # table with metrics obtained in the experiments, ordered by training checkpoints
   ├── model-usage-gpt2.ipynb  # model usage notebook
   └── utils # notebooks with utils for midi manipulation, such as encoding, decoding and data augmentation
       ├── midi_data_augmentation.ipynb
       ├── midi_decoder.ipynb
       └── midi_encoder.ipynb
├── start-custom-gpt2-ubuntu-env.sh # Starts custom-gpt2-env using docker
├── token_sequence_to_midi.py # Script to transform token sequence to midi
└── trainer.py # Script for training the model
```



## Download model weights and soundfont

First of all you need to download the model weights for the model and the soundfont. 

You can set everything up by running the `download-assets.sh` script. This will download the model weights and the soundfont for the MIDI output.
```bash
bash download-assets.sh
```

You can also do it manually, by downloading the model weights from [this link](https://dl.dropboxusercontent.com/s/o9368dgk4qz482p/custom-gpt2-model-ckpt.zip), as well as the [SoundFont](https://dl.dropboxusercontent.com/s/qfi8tfs5ljp68my/Yamaha-C5-sound-font.zip) for the MIDI output.




## Starting the environment

### Docker environment

The easiest way to start the environment is by using docker. 
You can use the following commands to create and start the docker environment:

```bash
# Create docker image
bash build-docker-environment.sh

# Start docker image
bash start-custom-gpt2-ubuntu-env.sh
```

This will start a docker ubuntu machine with all the dependencies needed. 
The script exposes port 8888, so you can access the jupyter notebooks from your browser.

The best way to interact with the system is through jupyter lab, which you can start by accessing the URL http://localhost:8888/lab/

### Local environment

1. Create a new environment (e.g. conda, venv, etc.) with python 3.8 and install all the dependencies on `requirements.txt`. Bellow some examples of how to create an environment with conda:

    **Create python conda environment:**
    ```bash
    bash create-custom-gpt2-env.sh
    ```

    **Activate the created environment:**
    ```bash
    conda activate custom-gpt2-env
    ```

If you are running on linux, you will also need to install `fluidsynth` and `libsndfile1`:

```bash
apt-get install -y fluidsynth libsndfile1
```


## How to generate music with the model

You can check with the [Custom-GPT2-Usage.ipynb](notebooks/model-usage-gpt2.ipynb) notebook how to generate music with the model. Essentially you need to load the model and then call the `generate` method in a hugging face 🤗 `pipeline`.

