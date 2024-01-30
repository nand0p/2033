#!/bin/bash -e


# 0 or 1
if [ -z "$1" ]; then
  DAEMONIZE=0
else
  DAEMONIZE=1
fi


DRY_RUN=0


NAME=$(basename "${PWD}")
VERSION=$(cat version.txt)
STOCKS=$(cat 2030.txt)
PORTS="80:5000"

TAG="${NAME}:${VERSION}"
#TAG="${REPO}/${NAME}:${VERSION}"

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
  if [ "${DAEMONIZE}" == "1" ]; then
    CONTAINER=$(docker run --detach \
                --publish ${PORTS} \
                -v data:/data \
                --env "STOCKS=${STOCKS}" \
                ${TAG})
    echo container ${CONTAINER}
    sleep 3

    echo hit endpoint
    curl -s -o /dev/null localhost
    sleep 3

    echo get container scores
    docker cp ${CONTAINER}:/data/ data
    rm data/data/stocks -rf

    echo docker containers
    docker ps
  else
    CONTAINER=$(docker run --interactive \
                --tty \
                --publish ${PORTS} \
                -v data:/data \
                --env "STOCKS=${STOCKS}" \
                ${TAG})
  fi
fi

