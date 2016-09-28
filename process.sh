#!/bin/bash
# Process tweets into OUTPUT file
INPUT="data/raw_2.json"
OUTPUT="data/tweets.txt"
SCRIPT="processing/twitter_processing.py"

python $SCRIPT $INPUT $OUTPUT
