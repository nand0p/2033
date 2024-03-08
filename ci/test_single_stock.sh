#!/bin/bash -ex

echo "==> test single stock <=="
sleep 2
curl "http://localhost?cat=9" | grep "finance.yahoo.com/quote" | nl

sleep 1
