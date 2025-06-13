# Splunk Weather API Collectors

This Splunk app provides two weather data collectors that fetch weather information from the Open-Meteo API:

1. **Secure Collector** (`api_collector.py`): Uses Splunk credential management
2. **Unsecure Collector** (`api_collector_unsecure.py`): Simple version without credential management

## Features

- Fetches current weather data including:
  - Temperature (°C)
  - Humidity (%)
  - Wind Speed (km/h)
  - Weather Description
  - City and Country Information
  - Timestamp
- Automatic geocoding of city names
- Structured JSON output for easy Splunk parsing
- Error handling with detailed error messages
- Configurable collection interval

## Installation

1. Copy the app to your Splunk apps directory:
   ```bash
   cp -r my_scripted_inputs $SPLUNK_HOME/etc/apps/
   ```

2. Restart Splunk:
   ```bash
   $SPLUNK_HOME/bin/splunk restart
   ```

## Configuration

### Secure Collector

The secure collector requires Splunk credential management setup:

1. Create a credential realm:
   ```bash
   $SPLUNK_HOME/bin/splunk add credentials -realm api_credentials -username api_user -password your_password
   ```

2. Configure the collector in `inputs.conf`:
   ```ini
   [script://./bin/api_collector.py --city "Sydney" --realm "api_credentials" --username "api_user"]
   disabled = 0
   interval = 300
   index = main
   passAuth = splunk-system-user
   ```

### Unsecure Collector

The unsecure collector is simpler to set up:

1. Configure in `inputs.conf`:
   ```ini
   [script://./bin/api_collector_unsecure.py --city "Sydney"]
   disabled = 0
   interval = 300
   index = main
   ```

## Usage

### Command Line Testing

Test the secure collector:
```bash
python3 ./bin/api_collector.py --city "Sydney" --realm "api_credentials" --username "api_user"
```

Test the unsecure collector:
```bash
python3 ./bin/api_collector_unsecure.py --city "Sydney"
```

### Output Format

Both collectors output JSON in this format:
```json
{
    "city": "Sydney",
    "country": "Australia",
    "temperature": 20.5,
    "humidity": 65,
    "wind_speed": 15.2,
    "description": "Partly cloudy",
    "timestamp": "2025-06-13T20:45"
}
```

Error responses:
```json
{
    "error": "Error message here"
}
```

## API Information

The collectors use the Open-Meteo API:
- Geocoding API: https://geocoding-api.open-meteo.com/v1/search
- Weather API: https://api.open-meteo.com/v1/forecast

No API key is required for either API.

## Troubleshooting

1. Check Splunk logs for error messages
2. Verify city names are correct
3. For secure collector, ensure credentials are properly set up
4. Check network connectivity to the Open-Meteo API

## Support

For issues or questions, please contact your Splunk administrator. 