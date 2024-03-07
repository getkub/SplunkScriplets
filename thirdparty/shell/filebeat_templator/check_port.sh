#!/bin/bash

# Function to check port with timeout
check_port() {
  local ip="$1"
  local port="$2"
  local timeout=2  # Set timeout in seconds

  # Check if timeout command exists
  if command -v timeout &> /dev/null; then
    timeout "$timeout" bash -c "echo > /dev/tcp/$ip/$port" &> /dev/null
  else
    # Fallback if timeout command not available
    (echo > "/dev/tcp/$ip/$port" &> /dev/null) & pid=$!
    sleep "$timeout"
    if ps -p $pid > /dev/null; then
      kill -9 $pid &>/dev/null
      return 1  # Failure (timeout)
    fi
  fi

  # Check exit code
  return 0  # Success
}

# Function to log message in JSON format
log_message() {
  local module="$1"
  local status="$2"
  local message="$3"

  log_data="{ \"timestamp\": \"$(date -u +"%Y-%m-%dT%H:%M:%SZ")\", \"module\": \"$module\", \"status\": \"$status\", \"message\": \"$message\" }"
  echo "$log_data"
}

# Read CSV file using loop and IFS
skip_header=true
successful_hosts=()  # Array to track successful connections

while IFS=, read -r hostname ip port; do
  # Skip header line
  if [ "$skip_header" = true ]; then
    skip_header=false
    continue
  fi

  # Check port and log message
  if check_port "$ip" "$port"; then
    successful_hosts+=("$ip:$port")
    log_message "filebeat" "success" "Successful connection to $ip:$port"
  else
    log_message "filebeat" "error" "Failed to connect to $ip:$port"
  fi
done < "your_csv_file.csv"  # Replace with your actual CSV file path

# Check if any successful connections and log accordingly
if [[ ${#successful_hosts[@]} -eq 0 ]]; then
  log_message "filebeat" "error" "No destinations reachable."
  exit 1  # Exit with error code
fi

logstash_hosts=""
# Loop through the array and format each element
for host in "${successful_hosts[@]}"; do
  logstash_hosts+="\"$host\", "
done
# Add brackets and remove the trailing comma and space
logstash_hosts="[ ${logstash_hosts%, *} ]"

sed "s/{{ LOGSTASH_HOSTS }}/$logstash_hosts/" filebeat.yml.template > /tmp/filebeat.yml

log_message "filebeat" "success" "Generated filebeat.yml with Logstash hosts: $logstash_hosts"

exit 0

