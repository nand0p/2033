#!/bin/bash -ex


echo download top level html
PATH=rez

wget --no-directories \
     --no-host-directories \
     --adjust-extension \
     --no-cache \
     --no-cookies \
     --directory-prefix=${PATH} \
     --default-page=index.html \
       "localhost?cat=0"
mv -v "${PATH}/index.html?cat=0.html" ${PATH}/index.html
sleep 1


echo download sub-site html

for BASE in 1 2 3 4 5 6 7 8; do
  pwd
  echo execute ${BASE}
  mkdir -pv ${PATH}/${BASE}
  wget --no-directories \
       --no-host-directories \
       --adjust-extension \
       --no-cache \
       --no-cookies \
       --directory-prefix=${PATH}/${BASE} \
       --default-page=index.html \
       "localhost?cat=${BASE}"

  mv -v "${PATH}/${BASE}/index.html?cat=${BASE}.html" ${PATH}/${BASE}/index.html
  sleep 1
done
