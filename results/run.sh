#!/bin/bash -e


bash kill.sh
bash build.sh

# 0 or 1
if [ -z "$1" ]; then
  DAEMONIZE=0
else
  DAEMONIZE=1
fi


DRY_RUN=0


REPO=nand0p
NAME=x2030-results
VERSION=$(cat VERSION)
PORTS="80:5000"

TAG="${NAME}:${VERSION}"
#TAG="${REPO}/${NAME}:${VERSION}"

echo
echo "running ${NAME}:${VERSION}"
echo



if [ "${DRY_RUN}" == "1" ]; then
  echo
  echo "DRY_RUN = 1"
  echo
  echo "docker run --publish ${PORTS}"
  echo "           ${TAG}"
  echo 
  exit 1

else
  CONTAINER=$(docker run --detach \
              --publish ${PORTS} \
              ${TAG})

  echo "=====> container ${CONTAINER}"
  echo "=====> docker logs -f ${CONTAINER}"
  docker logs -f ${CONTAINER}
fi
