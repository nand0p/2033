#!/bin/bash -ex

echo
echo 2030 Stock Hunter
echo
echo auto-generate all possible buy json
echo

for CATEGORY in $(seq 8); do
  echo
  echo CATEGORY ${CATEGORY}
  echo "python get_partial_share_trades.py --category ${CATEGORY} --all"
  python get_partial_share_trades.py --category ${CATEGORY} --all
  sleep 1
done
