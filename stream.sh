#!/bin/bash
# Stream tweets into OUTPUT file
# Specified arguments will be given to python script, for search keywords
OUTPUT="data/raw.json"
SCRIPT="streaming/twitter_streaming.py"

python $SCRIPT > $OUTPUT $@
