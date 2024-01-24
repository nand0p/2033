#!/bin/bash -ex


NAME=2030
VERSION=$(cat version.txt)

docker build --tag $NAME --label $NAME:VERSION --progress plain .

docker run -d -p 5000:80 2030

docker ps
