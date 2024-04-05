#!/bin/bash -ex

echo
echo 2030 Stock Hunter
echo
echo auto-generate all possible buy json
echo

for SPEED in "--fast" "--slow"; do
  for CATEGORY in $(seq 8); do
    echo
    echo CATEGORY ${CATEGORY}
    echo SPEED ${SPEED}
    echo "python get_partial_share_trades.py ${SPEED} --category ${CATEGORY} --all"
    python get_partial_share_trades.py ${SPEED} --category ${CATEGORY} --all
    sleep 1
  done
done
