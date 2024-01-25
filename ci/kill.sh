#!/bin/bash -ex


NAME=2030
VERSION=$(cat version.txt)

KILL=$(docker container ls --filter label=repo=${NAME} --format {{.ID}})

for CONTAINER in ${KILL}; do
  docker kill ${CONTAINER}
done

docker ps
