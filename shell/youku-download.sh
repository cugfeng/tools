#!/bin/bash

while read link; do
    if [ $(echo "$link" | grep -c ^#) -ne 0 ]; then
        continue
    fi

    echo "you-get $link"
    you-get -c $(pwd)/cookies.sqlite "$link"
    #you-get "$link"
    if [ $? -ne 0 ]; then
        echo "Failed to download $link"
    fi
done
