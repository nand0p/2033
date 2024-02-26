#!/bin/bash -e


DRY_RUN=0

REPO=nand0p
NAME=x2030
VERSION=$(cat VERSION)
STOCKS=$(cat 2030.txt)
PORTS="80:5000"

#TAG="${NAME}:${VERSION}"
TAG="${REPO}/${NAME}:${VERSION}"

echo "running ${NAME}:${VERSION} with"
STOCKS="\"$(echo ${STOCKS})\""
echo ${STOCKS}



if [ "${DRY_RUN}" == "1" ]; then
  echo
  echo "DRY_RUN = 1"
  echo
  echo "docker run --publish ${PORTS}"
  echo "           --env STOCKS=${STOCKS}"
  echo "           -v data:/data" 
  echo "           ${TAG}"
  echo 
  exit 1

else
  CONTAINER=$(docker run --detach \
              --publish ${PORTS} \
              -v data:/data \
              --env "STOCKS=${STOCKS}" \
              ${TAG})

  echo "=====> container ${CONTAINER}"
  echo "=====> docker logs -f ${CONTAINER}"
  docker logs -f ${CONTAINER}

fi
