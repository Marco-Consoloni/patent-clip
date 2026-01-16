#!/bin/sh

docker build . --build-arg UID=$(id -u) --build-arg GID=$(id -g) -t patent-clip:latest 

docker run \
    -it \
    --name patent-clip \
    --rm \
    --runtime=nvidia \
    --gpus all \
    --shm-size=1000gb \
    -v /vast/marco/Data_Google_Patent/:/vast/marco/Data_Google_Patent/ \
    -v ./docker/cache:/home/pytorch/.cache \
    -v ./docker/models:/models \
    -v ./docker/database:/database \
    -v ./docker/results:/results \
    -v ./docker/vectors:/vectors \
    patent-clip:latest \
    retrieve_vectors.py "$@"