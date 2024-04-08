#!/bin/bash

# Navigate to the directory containing the script
cd "$(dirname "$0")"

# Set the PYTHONPATH to the project directory
export PYTHONPATH=$(pwd)

python3 server.py --dir public