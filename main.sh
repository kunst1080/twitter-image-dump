#!/bin/bash

set -eu

mkdir -p .tmp
cat list.txt | xargs python3 collect.py true > .tmp/download.txt

cat .tmp/download.txt | while read ID USER URL
do
    FILENAME=$(basename $URL)
    OUTPUT=out/$USER
    echo $ID, $USER, $URL
    mkdir -p $OUTPUT
    wget "$URL:large" -O $OUTPUT/$FILENAME
done 2>> log.txt
