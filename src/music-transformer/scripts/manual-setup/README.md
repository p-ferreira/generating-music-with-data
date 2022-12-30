# Download magenta resources from google

Manual setup to get the original magenta resources from google cloud.

## Setting up the environment

Execute the `run-docker-gutils.sh` file to run a google cloud cli docker image:

```bash
bash run-docker-gutils.sh 
```

The current directory will be mapped to the `music-transformer` folder inside the container.
Go to the `music-transformer` directory inside the created container and execute the `download-magenta-resources.sh` file to download the original magenta resources:

```bash
bash gs-util-download-magenta-resources.sh 
```

This will download the following resources from google cloud:
- Music Transformers models checkpoints
- Primers for music generation
- Yamaha-C5-Salamander soundfont