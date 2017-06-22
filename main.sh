#!/bin/bash

set -u

mkdir -p .tmp
cat list.txt | xargs python3 collect.py true > .tmp/download.txt

touch .tmp/downloaded.txt

grep -v -f .tmp/downloaded.txt .tmp/download.txt | while read ID USER URL
do
    FILENAME=$(basename $URL)
    OUTPUT=out/$USER
    echo $ID, $USER, $URL
    mkdir -p $OUTPUT
    wget "$URL:large" -O $OUTPUT/$FILENAME
    if [ $? -eq 0 ]; then
        echo $ID >> .tmp/downloaded.txt
    else
        echo $ID >> .tmp/error.txt
    fi
done 2>> log.txt
