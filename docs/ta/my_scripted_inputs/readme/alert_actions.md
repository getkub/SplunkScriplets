# Splunk Alert Actions

This document explains how to use and configure custom alert actions in this Splunk Technical Add-on.

## Overview

Alert actions in Splunk allow you to perform custom actions when alerts are triggered. Our implementation provides a framework for creating custom alert actions using Python scripts.

## Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │
│  Splunk Alert   │────▶│  Alert Action   │────▶│  Python Script  │
│                 │     │  Configuration  │     │                 │
└─────────────────┘     └─────────────────┘     └─────────────────┘
         │                        │                        │
         │                        │                        │
         ▼                        ▼                        ▼
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │
│  alert_actions  │     │   commands.conf │     │  weather_alert  │
│      .conf      │     │                 │     │      .py        │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

## Implementation Steps

1. **Create Python Script**
   - Place script in `bin/alert_actions/`
   - Use common libraries from `bin/common/`
   - Implement alert processing logic

2. **Configure Alert Action**
   - Define alert action in `alert_actions.conf`
   - Specify command and parameters
   - Set up parameter mapping

3. **Define Command**
   - Add command definition in `commands.conf`
   - Specify Python version and script location
   - Map command-line arguments

4. **Use in Splunk**
   - Create saved search
   - Enable alerts
   - Select custom alert action

## Available Alert Actions

### Weather Alert
- Processes weather-related alerts
- Uses Open-Meteo API data
- Sends notifications based on weather conditions

## Best Practices

1. **Error Handling**
   - Use try-except blocks
   - Log errors with context
   - Return appropriate exit codes

2. **Logging**
   - Use structured logging
   - Include relevant context
   - Log both success and failure

3. **Security**
   - Validate input parameters
   - Handle sensitive data appropriately
   - Follow least privilege principle

## Troubleshooting

1. **Common Issues**
   - Script not found
   - Parameter mismatches
   - Execution errors

2. **Debug Steps**
   - Check Splunk internal logs
   - Verify script permissions
   - Test script independently

## Creating New Alert Actions

1. Create new Python script in `bin/alert_actions/`
2. Add configuration to `alert_actions.conf`
3. Add command definition to `commands.conf`
4. Update this documentation 