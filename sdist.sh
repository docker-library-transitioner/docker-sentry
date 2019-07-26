#!/usr/bin/env bash
set -e

SDIST_IMAGE_NAME=getsentry/sentry:git-sdist

docker build git --target=sdist -t $SDIST_IMAGE_NAME
id=$(docker create $SDIST_IMAGE_NAME)
docker cp $id:/dist ./dist
docker rm -v $id
