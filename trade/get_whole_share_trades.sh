#!/bin/bash -ex

echo
echo 2033 Stock Hunter
echo
echo auto-generate all possible buy json
echo

for SPEED in "fast" "slow"; do
  for CATEGORY in $(seq 8); do
    echo
    echo SPEED ${SPEED}
    echo CATEGORY ${CATEGORY}
    echo "python get_whole_share_trades.py --speed ${SPEED} --category ${CATEGORY} --all"
    python get_whole_share_trades.py --speed ${SPEED} --category ${CATEGORY} --all
    sleep 1
  done
done
