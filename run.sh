#!/bin/bash

bash ci/build.sh

bash kill.sh

if [ -z "$1" ]; then
  bash ci/run.sh
else
  bash ci/run.sh daemonize
fi
