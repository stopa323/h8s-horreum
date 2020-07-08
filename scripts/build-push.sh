#!/usr/bin/env bash
set -e

IMAGE_NAME_TAG="stopa323/h8s-horreum:$IMAGE_TAG"

bash scripts/build.sh

bash scripts/docker-login.sh

docker push "$IMAGE_NAME_TAG"
