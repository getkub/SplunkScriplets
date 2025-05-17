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
[macro_name]
definition = your_search_or_eval_definition
description = Description of what the macro does
is_eval = 0
args = 
```

## Usage

### Basic Commands

1. Check existing macros (dry run):
```bash
python update.py
```

2. Update macros (dry run):
```bash
python update.py --action-flag updateOnly
```

3. Update macros (actual execution):
```bash
python update.py --action-flag updateOnly --dry-run false
```

4. Delete macros:
```bash
python update.py --action-flag deleteOnly --dry-run false
```

### Command Line Arguments

- `--action-flag`: Specifies the action to perform
  - `updateOnly`: Create or update macros
  - `deleteOnly`: Delete existing macros
  - (default): Check existence of macros

- `--dry-run`: Perform a dry run without making changes
  - `true`: (default) Show what would be done without making changes
  - `false`: Actually perform the operations

- `--log-level`: Set the logging verbosity
  - `DEBUG`: Detailed debugging information
  - `INFO`: (default) General information
  - `WARNING`: Warning messages
  - `ERROR`: Error messages only

### Examples

1. Debug mode with update:
```bash
python update.py --action-flag updateOnly --log-level DEBUG
```

2. Force update without dry run:
```bash
python update.py --action-flag updateOnly --dry-run false
```

3. Delete macros with warnings:
```bash
python update.py --action-flag deleteOnly --log-level WARNING
```

## Macro Definition Format

### Simple Search Macro
```ini
[get_error_events]
definition = sourcetype=* error OR fail* OR critical OR fatal
description = Search for error events across all sourcetypes
is_eval = 0
args = 
```

### Parameterized Macro
```ini
[get_web_events(1)]
definition = sourcetype=access_* $arg1$
description = Search for web access events with a specific pattern
is_eval = 0
args = pattern
```

### Eval Macro
```ini
[calculate_avg_response_time]
definition = eval avg_time=avg(response_time)
description = Calculate average response time
is_eval = 1
args = 
```

## Error Handling

The script includes error handling for:
- SSL verification failures
- API connection issues
- Invalid macro definitions
- Missing configuration files

All errors are logged with appropriate severity levels.

## Logging

The script provides detailed logging of all operations:
- 🔧 Mode information
- ✏️ Update operations
- 🗑️ Delete operations
- ✅ Successful operations
- ❌ Failed operations
- ❓ Not found items
- 📬 New items to be created 