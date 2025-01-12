#!/bin/sh

echo "Building the docker image.."

BASE_NAME=christianbieri
IMAGE_NAME=data-simulator
TAG=1.0.0

CMD="docker build -t $BASE_NAME/$IMAGE_NAME:$TAG ."

echo $CMD
$CMD

echo "Done!"