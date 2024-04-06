#!/bin/bash -e


DRY_RUN=0

REPO=nand0p
NAME=x2033
VERSION=$(cat VERSION)
STOCKS=$(cat 2033.txt)
PORTS="80:5000"

#TAG="${NAME}:${VERSION}"
TAG="${REPO}/${NAME}:${VERSION}"
RUN="${REPO}-${NAME}-${VERSION}-$$"

echo "running ${NAME}:${VERSION} with"
STOCKS="\"$(echo ${STOCKS})\""
echo ${STOCKS}



if [ "${DRY_RUN}" == "1" ]; then
  echo
  echo "DRY_RUN = 1"
  echo
  echo "docker run --name ${RUN}"
  echo "           --publish ${PORTS}"
  echo "           --env STOCKS=${STOCKS}"
  echo "           ${TAG}"
  echo 
  exit 1

else
  CONTAINER=$(docker run --detach \
                         --name ${RUN} \
                         --publish ${PORTS} \
                         --env "STOCKS=${STOCKS}" \
                         ${TAG})


fi

if [ -z "$1" ]; then
  docker logs -f ${CONTAINER}
else
  echo "=====> container ${CONTAINER}"
  echo "=====> docker logs -f ${CONTAINER}"
fi
