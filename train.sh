#!/bin/sh

docker build . --build-arg UID=$(id -u) --build-arg GID=$(id -g) -t patent-clip:latest 

docker run \
    -it \
    --name patent-clip \
    --rm \
    --runtime=nvidia \
    --gpus all \
    --shm-size=1000gb \
    -v /vast/marco/Data/:/vast/marco/Data/ \
    -v ./docker/cache:/home/pytorch/.cache \
    -v ./docker/models:/models \
    -v ./docker/lightning_logs:/app/lightning_logs \
    -e WANDB_API_KEY=... \
    patent-clip:latest \
    train.py "$@"