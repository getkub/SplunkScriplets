# Secure API Collector for Splunk

This Splunk Technical Add-on (TA) provides a secure way to collect data from APIs using Splunk's credential management system. It's designed to work on Splunk Heavy Forwarders.

## Features

- Secure credential management using Splunk's password storage
- Uses Splunk's official SDK (splunklib) for credential management
- JSON-formatted logging
- Configurable API endpoints and authentication
- Works on Splunk Heavy Forwarders
- Modular design for easy extension

## Directory Structure

```
my_scripted_inputs/
├── bin/
│   ├── api_collector.py        # Weather API collector
│   ├── api_collector_unsecure.py # Weather API collector (no auth)
│   ├── cred_checker.py         # Credential verification tool
│   ├── splunklib/             # Splunk SDK libraries
│   └── common/
│       ├── splunk_common.py    # Common utilities and logging
│       └── splunk_secrets.py   # Secure credential management
├── default/
│   └── inputs.conf            # Splunk input configuration
└── metadata/
    └── default.meta           # Splunk metadata configuration
```

## Prerequisites

- Splunk Heavy Forwarder
- Python 3.x
- Splunk SDK (splunklib) in the bin/ directory

## DEV purpose copying

```
SPLUNK_HOME="/opt/splunk"

rsync -avz --size-only --checksum \
  --exclude='__pycache__' \
  --exclude='*.pyc' \
  --exclude='*.pyo' \
  --exclude='*.pyd' \
  --exclude='.DS_Store' \
  --exclude='.pytest_cache' \
  --delete \
  my_scripted_inputs ${SPLUNK_HOME}/etc/apps/ --dry-run
```

## Installation

1. Copy the TA to your Splunk apps directory:
   ```bash
   cp -r my_scripted_inputs $SPLUNK_HOME/etc/apps/
   ```

2. Ensure splunklib is present in the bin/ directory:
   ```bash
   # The splunklib directory should be in bin/splunklib/
   ls $SPLUNK_HOME/etc/apps/my_scripted_inputs/bin/splunklib/
   ```

3. Set up credentials in Splunk:
   ```bash
   splunk add credentials -realm weather_api -username weather_api -password your_api_key
   ```

## Configuration

### Input Configuration

The scripts are configured through Splunk's `inputs.conf`. Example configurations:

```ini
# Weather API Collector (Secure)
[script://./bin/api_collector.py --city "Sydney" --realm "weather_api" --username "weather_api"]
disabled = 0
interval = 300
index = main
passAuth = splunk-system-user

# Weather API Collector (Unsecure)
[script://./bin/api_collector_unsecure.py --city "Sydney"]
disabled = 0
interval = 300
index = main

# Credential Checker
[script://./bin/cred_checker.py --realm "weather_api" --username "weather_api"]
sourcetype = cred_checker
index = main
disabled = 0
interval = 300
passAuth = splunk-system-user
```

### Environment Variables

The following environment variables can be configured:

- `SPLUNK_MGMT_PORT`: Splunk management port (default: 8089)
- `SPLUNK_MGMT_HOST`: Splunk management host (default: localhost)

## Available Collectors

### 1. Weather API Collector (`api_collector.py`)
- Fetches weather data using Open-Meteo API
- Secure credential management using Splunk SDK
- JSON response handling
- Parameters:
  - `--city`: City name for weather data
  - `--realm`: Credential realm
  - `--username`: Credential username

### 2. Weather API Collector (Unsecure) (`api_collector_unsecure.py`)
- Same functionality as secure collector but without credential management
- Uses Open-Meteo API (no API key required)
- Parameters:
  - `--city`: City name for weather data

### 3. Credential Checker (`cred_checker.py`)
- Verifies credential storage and retrieval
- Uses Splunk SDK for credential management
- Parameters:
  - `--realm`: Credential realm to check
  - `--username`: Credential username to check

## Usage

The collectors are automatically run by Splunk based on the configured interval. They will:

1. Retrieve credentials from Splunk's password storage (secure version)
2. Make API calls to fetch weather data
3. Log results in JSON format

### Manual Testing

You can test the collectors manually:

```bash
# Test the secure collector
python3 ./bin/api_collector.py --city "Sydney" --realm "weather_api" --username "weather_api"

# Test the unsecure collector
python3 ./bin/api_collector_unsecure.py --city "Sydney"

# Test credential checker
python3 ./bin/cred_checker.py --realm "weather_api" --username "weather_api"
```

## Logging

The collectors use JSON-formatted logging with the following fields:
- `ts`: Timestamp
- `level`: Log level (INFO, ERROR)
- `module`: Module name
- `message`: Log message
- `status`: Success/failure status

## Security Considerations

1. Credentials are stored in Splunk's encrypted password storage
2. Uses Splunk's official SDK for credential management
3. No sensitive data is exposed in environment variables or logs
4. Uses Splunk's session key for authentication
5. SSL verification is disabled by default (should be properly configured in production)

## Creating New Collectors

To create a new API collector:

1. Create a new Python script in the `bin` directory
2. Import the common modules:
   ```python
   from common import splunk_common
   from common.splunk_secrets import SplunkSecrets
   ```
3. Use the `SplunkSecrets` class for credential management
4. Implement your specific API collection logic
5. Add the new collector to `inputs.conf` with appropriate parameters

## Troubleshooting

1. Check Splunk's internal logs for script execution issues
2. Verify credentials are properly stored in Splunk
3. Ensure splunklib is present in the bin/ directory
4. Check network access to both Splunk management port and target API
5. Verify Python dependencies are installed correctly

## Support

For issues or questions, please contact your Splunk administrator or raise an issue in the repository.