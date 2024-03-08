#!/bin/bash -ex

SPEED=slow
echo download sub-site html ${SPEED}

for BASE in 1 2 3 4 5 6 7 8; do
  pwd
  echo execute ${SPEED} ${BASE}
  mkdir -pv ${SPEED}/${BASE}
  wget --no-directories \
       --no-host-directories \
       --adjust-extension \
       --no-cache \
       --no-cookies \
       --directory-prefix=${SPEED}/${BASE} \
       --default-page=index.html \
       "localhost?cat=${BASE}&speed=${SPEED}"

  mv -v "${SPEED}/${BASE}/index.html?cat=${BASE}&speed=${SPEED}.html" ${SPEED}/${BASE}/index.html
  sleep 1
done
