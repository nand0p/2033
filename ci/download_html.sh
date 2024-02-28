#!/bin/bash

for BASE in 1 2 3 4 5 6 7; do
  pwd
  echo execute ${BASE}
  mkdir -pv ${BASE}
  cd ${BASE}
  wget --recursive \
       --level 2 \
       --page-requisites \
       --convert-links \
       localhost?cat=${BASE}
  mv -v localhost/index.html\?cat\=${BASE} localhost/index.html
  mv -v localhost/index.html .
  mv -v localhost/static .
  cd ..
  sleep 1
done
