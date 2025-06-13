# Secure API Collector for Splunk

This Splunk Technical Add-on (TA) provides a secure way to collect data from APIs using Splunk's credential management system. It's designed to work on Splunk Heavy Forwarders.

## Features

- Secure credential management using Splunk's password storage
- REST API-based credential retrieval (no splunklib dependency)
- JSON-formatted logging
- Configurable API endpoints and authentication
- Works on Splunk Heavy Forwarders
- Modular design for easy extension

## Directory Structure

```
my_scripted_inputs/
├── bin/
│   ├── api_collector.py        # Basic API collector
│   ├── api_collector_2.py      # Time series API collector
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
- `requests` Python package

## Installation

1. Copy the TA to your Splunk apps directory:
   ```bash
   cp -r my_scripted_inputs $SPLUNK_HOME/etc/apps/
   ```

2. Install required Python packages:
   ```bash
   pip3 install requests
   ```

3. Set up credentials in Splunk:
   ```bash
   splunk add credentials -realm api_credentials -username api_user -password your_api_key
   ```

## Configuration

### Input Configuration

The scripts are configured through Splunk's `inputs.conf`. Example configurations:

```ini
# Basic API Collector
[script://./bin/api_collector.py --url "https://api.example.com/endpoint" --realm "api_credentials" --username "api_user"]
disabled = 0
interval = 300
index = main
passAuth = splunk-system-user

# Time Series API Collector
[script://./bin/api_collector_2.py --url "https://api.example.com/timeseries" --realm "api_credentials" --username "api_user" --days 1]
disabled = 0
interval = 3600
index = main
passAuth = splunk-system-user
```

### Environment Variables

The following environment variables can be configured:

- `SPLUNK_MGMT_PORT`: Splunk management port (default: 8089)
- `SPLUNK_MGMT_HOST`: Splunk management host (default: localhost)

## Available Collectors

### 1. Basic API Collector (`api_collector.py`)
- Simple API data collection
- Basic authentication
- JSON response handling
- Parameters:
  - `--url`: API endpoint URL
  - `--realm`: Credential realm
  - `--username`: Credential username

### 2. Time Series API Collector (`api_collector_2.py`)
- Time series data collection
- Date range parameters
- Extended timeout for large datasets
- Per-entry logging
- Parameters:
  - `--url`: API endpoint URL
  - `--realm`: Credential realm
  - `--username`: Credential username
  - `--days`: Number of days to look back

## Usage

The API collectors are automatically run by Splunk based on the configured interval. They will:

1. Retrieve credentials from Splunk's password storage
2. Make authenticated API calls
3. Log results in JSON format

### Manual Testing

You can test the collectors manually:

```bash
# Set the session key
export SPLUNK_SESSION_KEY=your_session_key

# Run the basic collector
python3 ./bin/api_collector.py --url "https://api.example.com/endpoint" --realm "api_credentials" --username "api_user"

# Run the time series collector
python3 ./bin/api_collector_2.py --url "https://api.example.com/timeseries" --realm "api_credentials" --username "api_user" --days 7
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
2. No sensitive data is exposed in environment variables or logs
3. Uses Splunk's session key for authentication
4. SSL verification is disabled by default (should be properly configured in production)

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
5. Add the new collector to `inputs.conf` with appropriate parameters in the script path

## Troubleshooting

1. Check Splunk's internal logs for script execution issues
2. Verify credentials are properly stored in Splunk
3. Ensure network access to both Splunk management port and target API
4. Check Python dependencies are installed correctly

## Support

For issues or questions, please contact your Splunk administrator or raise an issue in the repository.