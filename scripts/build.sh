#!/usr/bin/env bash
set -e

if [[ -z "$IMAGE_TAG" ]] ; then
    echo "No tag provided. Assigning latest."
    IMAGE_TAG="latest"
fi

IMAGE_NAME_TAG="stopa323/h8s-horreum:$IMAGE_TAG"

docker build -t "$IMAGE_NAME_TAG" --file "./docker/Dockerfile" .
