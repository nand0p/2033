#!/bin/bash

bash ci/build.sh

bash ci/run.sh daemon

bash ci/test_single_stock.sh

bash ci/upload_scores.sh
