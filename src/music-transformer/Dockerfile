FROM ubuntu:latest

ENV PATH="/root/miniconda3/bin:${PATH}"
ARG PATH="/root/miniconda3/bin:${PATH}"

# Install conda
RUN apt-get update && apt-get install -y apt-utils wget curl python3-pip git vim

# Install sound dependencies
RUN apt-get install -y fluidsynth libsndfile1 libasound2-dev libjack-dev 

RUN wget \
    https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh \
    && mkdir /root/.conda \
    && bash Miniconda3-latest-Linux-x86_64.sh -b \
    && rm -f Miniconda3-latest-Linux-x86_64.sh 

# Copies conda environment file
COPY music-transformer-env.yml music-transformer-env.yml
COPY create-music-transformer-env.sh create-music-transformer-env.sh
COPY scripts scripts

# Set up conda environment
RUN conda init bash

# Executes the conda environment creation script
RUN bash create-music-transformer-env.sh

# Copy over the gym_utils.py file to the correct broken dependency
RUN cp -rf scripts/gym_utils.py /root/miniconda3/envs/music-transformer-env/lib/python3.7/site-packages/tensor2tensor/rl

# Set up jupyter lab
RUN conda install -c conda-forge jupyterlab nb_conda_kernels
RUN conda install ipykernel ipywidgets 

# Start a new bash with conda installed
CMD ["jupyter", "notebook", "--ip=*", "--port=8888", "--allow-root", "--no-browser"]
EXPOSE 8888