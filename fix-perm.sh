#!/bin/sh

docker run -it --rm -v $(pwd):/storage busybox chown $(id -u):$(id -u) -R /storage/docker
