#!/bin/bash -ex


echo download top level html
for SPEED in 'fast' 'slow'; do
  pwd
  echo execute ${SPEED}
  mkdir -pv ${SPEED}
  cd ${SPEED}
  wget --recursive \
       --no-directories \
       --no-host-directories \
       --adjust-extension \
       --no-cache \
       --no-cookies \
       --directory-prefix=${SPEED} \
       --default-page=index.html \
       "localhost?speed=${SPEED}"
  cd ..
  sleep 1
done

echo download sub-site html
for SPEED in 'fast' 'slow'; do
  for BASE in 1 2 3 4 5 6 7 8; do
    pwd
    echo execute ${SPEED} ${BASE}
    mkdir -pv ${SPEED}/${BASE}
    cd ${SPEED}/${BASE}
    wget --recursive \
         --no-directories \
         --no-host-directories \
         --adjust-extension \
         --no-cache \
         --no-cookies \
         --directory-prefix=${SPEED}/${BASE} \
         --default-page=index.html \
         "localhost?cat=${BASE}&speed=${SPEED}"
    cd ../..
    sleep 1
  done
done
