#!/bin/bash

# Navigate to the directory containing the script
cd "$(dirname "$0")"

# Set the PYTHONPATH to the project directory
export PYTHONPATH=$(pwd)

# Run the Python script
python3 src/main.py