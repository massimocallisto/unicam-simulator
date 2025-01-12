#!/bin/sh

echo "Building the docker image.."

BASE_NAME=christianbieri
IMAGE_NAME=data-simulator-temperature
TAG=1.0.1

CMD="docker build -t $BASE_NAME/$IMAGE_NAME:$TAG -f DockerfileTemperature ."

echo $CMD
$CMD

echo "Done!"