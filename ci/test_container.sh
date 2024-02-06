#!/bin/bash -x


TEST=$(curl http://localhost/test)

if [ -z ${TEST} ]; then
  echo
  echo "service not available"
  echo
  exit 1
elif [[ "success" == *${TEST}* ]]; then
  echo
  echo success
  echo
fi

