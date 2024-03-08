#!/bin/bash -ex

echo "==> test single stock <=="
sleep 2
curl "http://localhost?cat=9&speed=fast" | grep "rolling fast"
curl "http://localhost?cat=9&speed=slow" | grep "rolling slow"
sleep 1
