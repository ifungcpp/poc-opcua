#!/bin/bash

# Check if a hostname is provided as an argument
if [ -z "$1" ]; then
  echo "Usage: $0 <hostname>"
  exit 1
fi

hostname=$1

# Use dig to get the IP address
ip_address=$(dig +short "$hostname")

# Check if dig was successful
if [ -z "$ip_address" ]; then
  echo "Failed to resolve hostname: $hostname"
  exit 1
fi

# Output the IP address
echo "The IP address of $hostname is $ip_address"