#!/bin/bash -e


# 0 or 1
DAEMONIZE=0
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
  echo "           ${TAG}"
  echo 
  exit 1
else
  if [ "${DAEMONIZE}" == "1" ]; then
    docker run --daemon \
               --publish ${PORTS} \
               --env "STOCKS=${STOCKS}" \
               ${TAG}
  elif [ "${DAEMONIZE}" == "0" ]; then
    docker run --interactive \
               --tty \
               --publish ${PORTS} \
               --env "STOCKS=${STOCKS}" \
               ${TAG}
  fi
fi

docker ps
