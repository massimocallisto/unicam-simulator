#!/bin/sh

echo "Building the docker image.."

BASE_NAME=massimocallisto
IMAGE_NAME=unicam-data-simulator-temperature
TAG=0.0.1

CMD="docker build -t $BASE_NAME/$IMAGE_NAME:$TAG -f DockerfileTemperature ."

echo $CMD
$CMD

echo "Done!"