#!/bin/sh

echo "Pushing the docker image.."

BASE_NAME=massimocallisto
IMAGE_NAME=unicam-data-simulator-temperature
TAG=0.0.1

CMD="docker push $BASE_NAME/$IMAGE_NAME:$TAG"

echo $CMD
$CMD

echo "Done!"