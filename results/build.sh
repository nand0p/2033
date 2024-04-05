#!/bin/bash -ex


# this is run from the repo root
# bash -ex ci/build.sh


NAME=X2033-results
REPO=nand0p
AUTHOR=nando
OWNER=hex7
VERSION=$(cat VERSION)


#TAG="${NAME}:${VERSION}"
TAG="${REPO}/${NAME}:${VERSION}"

cp -v ../2033.txt 2033.txt
cp -v ../categories.json categories.json
cp -v ../utils/stocks.py utils/stocks.py

if [ -n ${VERSION} ]; then
  echo "building docker image ${NAME}:${VERSION}"
  docker build --tag ${TAG} \
               --label "repo=${NAME}" \
               --label "version=${VERSION}" \
               --label "owner=${OWNER}" \
               --label "author=${AUTHOR}" \
               --progress plain .
else
  echo "version incorrect. aborting."
  exit 1
fi

rm -fv 2033.txt
rm -fv categories.json
rm -fv utils/stocks.py

docker images --no-trunc --all
docker images
