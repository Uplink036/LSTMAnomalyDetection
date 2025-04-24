#!/bin/bash
set -e

DESTIONATION_FOLDER="data/"
DIR_PATH="./"$DESTIONATION_FOLDER
mkdir -p $DIR_PATH
# Get data
if [ ! -f  $DIR_PATH"network-anamoly-detection.zip" ]; then
    curl -L -o $DIR_PATH"network-anamoly-detection.zip"\
        https://www.kaggle.com/api/v1/datasets/download/anushonkar/network-anamoly-detection

    # Uncompress data
    dataset=$(find $DIR_PATH*.zip)
    unzip $dataset -d $DIR_PATH
fi

# Send all data to database
# python3 load_data.py