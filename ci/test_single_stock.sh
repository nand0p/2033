#!/bin/bash

echo "==>hit endpoint"
sleep 2
curl -s -o /dev/null localhost?cat=7
sleep 1
