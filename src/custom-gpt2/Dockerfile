FROM ubuntu:latest

ENV PATH="/root/miniconda3/bin:${PATH}"
ARG PATH="/root/miniconda3/bin:${PATH}"

# Install OS dependencies
RUN apt-get update && apt-get install -y apt-utils wget curl python3-pip git vim

# Install sound dependencies
RUN apt-get install -y fluidsynth libsndfile1 

# Install conda
RUN wget \
    https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh \
    && mkdir /root/.conda \
    && bash Miniconda3-latest-Linux-x86_64.sh -b \
    && rm -f Miniconda3-latest-Linux-x86_64.sh 

# Copies conda environment file
COPY custom-gpt2-env.yml custom-gpt2-env.yml
COPY create-custom-gpt2-env.sh create-custom-gpt2-env.sh


# Set up conda environment
RUN conda init bash

# Executes the conda environment creation script
RUN bash create-custom-gpt2-env.sh

# Set up jupyter lab
RUN conda install -c conda-forge jupyterlab nb_conda_kernels
RUN conda install ipykernel ipywidgets 


# Start a new bash with conda installed
CMD ["jupyter", "notebook", "--ip='*'", "--port=8888", "--allow-root", "--no-browser", "--NotebookApp.token=''","--NotebookApp.password=''"]
EXPOSE 8888