#!/bin/bash -ex


sleep 3
API=http://localhost/test
TEST=$(curl ${API})
echo
echo RESPONSE ${API}:
echo ${TEST}
echo

if echo ${TEST} | grep -q "success"; then
  echo
  echo success
  echo
else
  echo
  echo "service not available"
  echo
  exit 1
fi
