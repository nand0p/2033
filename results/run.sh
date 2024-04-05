#!/bin/bash -e


DRY_RUN=0
TEST_RUN=0


REPO=nand0p
NAME=x2033-results
VERSION=$(cat VERSION)
PORTS=80:5000

#PLATFORM=linux/x86_64
PLATFORM=linux/arm64/v8

#TAG=${NAME}:${VERSION}
TAG=${REPO}/${NAME}:${VERSION}
RUN=${REPO}_${NAME}_${VERSION}_$$

echo
echo "running ${TAG}"
echo



if [ "${DRY_RUN}" == "1" ]; then

  echo
  echo "DRY_RUN = 1"
  echo
  echo "docker run --name ${RUN}"
  echo "           --publish ${PORTS}"
  echo "           --platform ${PLATFORM}"
  echo "             ${TAG}"
  echo 
  exit 1


elif [ "${TEST_RUN}" == "1" ]; then

  docker run \
    --attach STDIN \
    --attach STDOUT \
    --attach STDERR \
    --platform ${PLATFORM} \
    --cidfile /tmp/docker.${RUN}.cid \
    --env NAME=${NAME} \
    --label NAME=${NAME} \
    --label RUN=${RUN} \
    --health-cmd health \
    --publish ${PORTS} \
    --name ${RUN} \
      ${TAG}

  exit 0


else
  CONTAINER=$(docker run --detach \
                         --publish ${PORTS} \
                           ${TAG})

  echo "=====> container ${CONTAINER}"
  echo "=====> docker logs -f ${CONTAINER}"
fi

if [ -z "$1" ]; then
  docker logs -f ${CONTAINER}
fi

sleep 3
docker logs ${CONTAINER}
