# Performance RNN

This directory contains an example notebook of how to use the model described in the paper [Performance RNN: Generating Music with Expressive Timing and Dynamics](https://magenta.tensorflow.org/performance-rnn).


# Download model weights

To download the model weights, you can use the `download-assets.sh` script. This will download the model weights from the [official repository](https://github.com/magenta/magenta/blob/main/magenta/models/performance_rnn/README.md#pre-trained)

```bash
bash download-assets.sh
```

> Note: You can also download the model weights manually from [this link](http://download.magenta.tensorflow.org/models/performance_with_dynamics.mag)


## Setting up the environment

### Local environment

Create the conda environment for the music transformer:

**Create python conda environment:**
```bash
conda env create -f performance-rnn-env.yml
``` 

**Activate the created environment:**
```bash
conda activate performance-rnn-env
```

If you are running on linux, you will need to install some other dependencies with the following command:
```bash
apt-get install -y fluidsynth libsndfile1 libasound2-dev libjack-dev
```


This will set the environment with the right versions of the dependencies.


## How to generate music with the model

To explore the models and generate samples with it, open the notebook
located at [`notebooks/generate-midi-performance-rnn.ipynb`](notebooks/generate-midi-performance-rnn.ipynb).