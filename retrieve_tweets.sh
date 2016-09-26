#!/bin/bash

OUTPUT="data/raw.json"
SCRIPT="streaming/twitter_streaming.py"

python $SCRIPT > $OUTPUT
