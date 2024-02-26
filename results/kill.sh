#!/bin/bash -ex


NAME=x2030-results
VERSION=$(cat VERSION)

KILL=$(docker container ls --filter label=repo=${NAME} --format {{.ID}})

for CONTAINER in ${KILL}; do
  docker kill ${CONTAINER}
done

docker ps
