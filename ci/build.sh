#!/bin/bash -ex


# this is run from the repo root
# bash -ex ci/build.sh


NAME=${git rev-parse --show-toplevel}
REPO=nand0p
AUTHOR=nando
OWNER=hex7
VERSION=$(cat version.txt)

TAG="${REPO}/${NAME}:${VERSION}"

if [ -n ${VERSION} ]; then
  echo "building docker image ${NAME}:${VERSION}"
  docker build --tag ${TAG} \
               --label "repo=${NAME}" \
               --label "version=${VERSION}" \
               --label "owner=${HEX7}" \
               --label "author=${AUTHOR}" \
               --progress plain .
else
  echo "version incorrect. aborting."
  exit 1
fi

docker images --no-trunc --all
docker images
