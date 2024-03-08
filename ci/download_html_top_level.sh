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
  mv -v "index.html?speed=fast.html" index.html
  cd ..
  sleep 1
done
