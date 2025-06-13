#!/bin/bash

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Set up Python path
export PYTHONPATH="${SCRIPT_DIR}:${PYTHONPATH}"

# Run the API collector with secure credentials
python3 "${SCRIPT_DIR}/api_collector.py" \
    --url "$1" \
    --realm "api_credentials" \
    --username "api_user" 