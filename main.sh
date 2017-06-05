#!/bin/bash

set -eu

mkdir -p .tmp
cat list.txt | xargs python3 collect.py true > .tmp/download.txt

grep -v -f .tmp/downloaded.txt .tmp/download.txt | while read ID USER URL
do
    FILENAME=$(basename $URL)
    OUTPUT=out/$USER
    echo $ID, $USER, $URL
    mkdir -p $OUTPUT
    wget "$URL:large" -O $OUTPUT/$FILENAME
    echo $ID >> .tmp/downloaded.txt
done 2>> log.txt
