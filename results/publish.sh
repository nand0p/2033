#!/bin/bash -ex


echo download top level html
SHA=$(git rev-parse HEAD)
OUT=results
mkdir -pv ${OUT}

wget --no-directories \
     --no-host-directories \
     --adjust-extension \
     --span-hosts \
     --page-requisites \
     --no-cache \
     --no-cookies \
     --directory-prefix=${OUT} \
     --default-page=index.html \
       "localhost?cat=0"

mv -v "${OUT}/index.html?cat=0.html" ${OUT}/index.html
sed -i.b1 "s/\/static/http:\/\/2033.hex7.com\/results/g" ${OUT}/index.html
sed -i.b2 "s/SEDME/${SHA}/g" ${OUT}/index.html
rm -vf ${OUT}/index.html.b1 ${OUT}/index.html.b2
sleep 1


echo download sub-site html
for BASE in 1 2 3 4 5 6 7 8; do
  pwd
  echo execute ${BASE}
  mkdir -pv ${OUT}/${BASE}
  wget --no-directories \
       --no-host-directories \
       --adjust-extension \
       --no-cache \
       --no-cookies \
       --directory-prefix=${OUT}/${BASE} \
       --default-page=index.html \
       "localhost?cat=${BASE}"

  mv -v "${OUT}/${BASE}/index.html?cat=${BASE}.html" ${OUT}/${BASE}/index.html
  sed -i.b1 "s/\/static/http:\/\/2033.hex7.com\/results/g" ${OUT}/${BASE}/index.html
  sed -i.b2 "s/SEDME/${SHA}/g" ${OUT}/${BASE}/index.html
  rm -vf ${OUT}/index.html.b1 ${OUT}/${BASE}/index.html.b2
  sleep 1
done

echo publish to s3
aws s3 sync --acl public-read ${OUT} s3://2033.hex7.com/${OUT}
