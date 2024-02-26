#!/bin/bash

bash ci/build.sh

bash kill.sh

bash ci/run.sh daemon
