# Splunk Macro Management Script

This script manages Splunk macros through the REST API. It can create, update, and delete macros based on definitions in a `macros.conf` file.

## Prerequisites

- Python 3.x
- Required Python packages:
  - requests
  - configparser
- Splunk instance with REST API access
- Valid authentication token
- SSL certificate for Splunk instance

## Directory Structure

```
macros/
├── files/
│   ├── macros.conf      # Macro definitions
│   ├── config.json      # Splunk app and owner configuration
│   └── splunk-8089.crt  # SSL certificate
├── update.py           # Main script
└── README.md          # This file
```

## Configuration Files

### config.json
```json
{
    "app": "your_app_name",
    "owner": "your_owner_name"
}
```

### macros.conf
Example macro definition:
```ini
[macro_name(1)]
definition = eval newfield=$myfield$
description = Description of what the macro does
is_eval = 0
args = myfield
```

## Usage

### Basic Commands

1. Check existing macros (dry run):
```bash
python ./scripts/update_macros.py --conf-path files/cloudtrail.conf
```

2. Update macros (dry run):
```bash
python ./scripts/update_macros.py --conf-path files/cloudtrail.conf --action-flag updateOnly --log-level DEBUG
```


4. Delete macros:
```bash
python ./scripts/update_macros.py --conf-path files/cloudtrail.conf --action-flag updateOnly --log-level DEBUG
```

