#!/bin/bash

# Navigate to the directory containing the script
cd "$(dirname "$0")"

# Set the PYTHONPATH to the project directory
export PYTHONPATH=$(pwd)

# run the tests
python3 -m unittest discover -s test