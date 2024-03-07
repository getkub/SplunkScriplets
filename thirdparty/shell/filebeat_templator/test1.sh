#!/bin/bash

# Dummy array for testing
successful_hosts=("127.0.0.1:22" "::1:22" "192.168.1.1:22")

# Initialize an empty string
logstash_hosts=""

# Loop through the array and format each element
for host in "${successful_hosts[@]}"; do
  logstash_hosts+="\"$host\", "
done

# Add brackets and remove the trailing comma and space
logstash_hosts="[ ${logstash_hosts%, *} ]"

# Print the result
echo "logstash_hosts: $logstash_hosts"
