#!/bin/bash

echo "==> test full site <=="
sleep 1
curl http://localhost?cat=0&speed=fast
sleep 1
curl http://localhost?cat=0&speed=slow
sleep 1
