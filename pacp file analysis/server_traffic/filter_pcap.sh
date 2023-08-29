#!/bin/bash

src_directory="/Users/sanshui/Documents/Research Project/bose_speaker/original_pcap"
dst_directory="/Users/sanshui/Documents/Research Project/bose_speaker/server_traffic"

# Create target directory
mkdir -p "$dst_directory"

# IP address list
IP_ADDRESSES="85.119.83.206 95.215.175.2 217.114.59.66 162.159.200.123 51.89.151.183 217.114.59.3 85.199.214.98 85.119.84.153 34.237.118.24 34.237.118.89 18.164.68.107 18.164.68.19 18.164.68.101 18.164.68.77 54.167.164.29 54.242.11.196 52.7.111.165 52.54.20.148 52.2.253.120 54.226.202.10 107.23.57.254 52.2.55.114 99.84.9.123 99.84.9.9 99.84.9.77 99.84.9.80 3.232.190.0 54.204.250.0 54.236.130.172 35.169.149.17 52.5.55.32 3.234.23.184"

for pcap_file in "$src_directory"/*.pcap; do
    # Get the base name of the file
    base_name=$(basename "$pcap_file")

    # Define a new save path
    new_path="$dst_directory/$base_name"

    FILTER=""

    for ip in $IP_ADDRESSES; do
        if [ "$FILTER" = "" ]; then
            FILTER="ip.addr == $ip"
        else
            FILTER="$FILTER || ip.addr == $ip"
        fi
    done

    # Use tshark to filter traffic and save to new location
    tshark -r "$pcap_file" -w "$new_path" "$FILTER"
done

echo "Filtering completed."
