#!/bin/bash -ex

SPEED=fast
echo download sub-site html ${SPEED}

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

  mv -v "index.html?cat=${BASE}&speed=${SPEED}.html" index.html
  cd ../..
  sleep 1
done
