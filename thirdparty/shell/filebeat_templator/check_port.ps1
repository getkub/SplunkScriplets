function Check-Port {
    param (
        [string]$ip,
        [int]$port
    )

    try {
        $result = Test-NetConnection -ComputerName $ip -Port $port -InformationLevel Quiet
        if ($result -eq 'Success') {
            return $true  # Success
        } else {
            return $false  # Failure
        }
    } catch {
        return $false  # Failure (exception)
    }
}

# Set default port (optional)
$port = 22  # Default port is 22 (SSH)

# Function to log message in JSON format
function Log-Message {
    param (
        [string]$module,
        [string]$status,
        [string]$message
    )

    $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
    $logData = @{
        'module'    = $module
        'status'    = $status
        'timestamp' = $timestamp
        'message'   = $message
    } | ConvertTo-Json

    Write-Output $logData
}

# Get the directory of the script
$scriptDirectory = Split-Path -Parent $MyInvocation.MyCommand.Path

# Read CSV file using Import-Csv
$csvPath = Join-Path $scriptDirectory "your_csv_file.csv"  # Replace with your actual CSV file path
$csvData = Import-Csv $csvPath

# Initialize array to track successful connections
$successfulHosts = @()

foreach ($entry in $csvData) {
    $ip = $entry.ip
    $port = $entry.port

    # Check port and log message
    if (Check-Port $ip $port) {
        $successfulHosts += "$ip:$port"
        Log-Message "filebeat" "success" "Successful connection to $ip:$port"
    } else {
        Log-Message "filebeat" "error" "Failed to connect to $ip:$port"
    }
}

# Check if any successful connections and log accordingly
if ($successfulHosts.Count -eq 0) {
    Log-Message "filebeat" "error" "No destinations reachable."
    exit 1  # Exit with error code
}

# Generate final filebeat.yml by replacing placeholder
$logstashHosts = $successfulHosts -join ", "
$filebeatYmlPath = Join-Path $scriptDirectory "filebeat.yml"

(Get-Content (Join-Path $scriptDirectory "filebeat.yml.template")) -replace "{{ LOGSTASH_HOSTS }}", $logstashHosts | Set-Content $filebeatYmlPath

Log-Message "filebeat" "success" "Generated filebeat.yml with Logstash hosts: $logstashHosts"
exit 0
