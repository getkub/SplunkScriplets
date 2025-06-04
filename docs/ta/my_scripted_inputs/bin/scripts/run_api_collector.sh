#!/bin/bash

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
APP_DIR="$(dirname "$SCRIPT_DIR")"
APP_DIR="$(dirname "$APP_DIR")"

# Set up Python environment
export PYTHONPATH="${APP_DIR}/bin:${PYTHONPATH}"

# Run the Python script
python3 "${SCRIPT_DIR}/api_collector.py" 