#!/bin/bash
source /vol1/1000/开发/python3.11/bin/activate
# Define source and destination paths
SOURCE="/vol3/1000/Media"
DESTINATION="/vol2/1000/docker/clouddrive2/shared/115/Media"

# Run the Python script with the specified arguments
python3 main.py -s="$SOURCE" -d="$DESTINATION"