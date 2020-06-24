#!/usr/bin/env bash
set -e

IMAGE_TAG=""

if [ "$IMAGE_TAG" == "" ] ; then
    IMAGE_TAG="build-test"
fi

docker build -t "h8s-horreum:$IMAGE_TAG" --file "./docker/Dockerfile" .