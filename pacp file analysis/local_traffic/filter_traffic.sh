#!/bin/bash

src_directory="/Users/sanshui/Documents/Research Project/bose_speaker/original_pcap"
dst_directory="/Users/sanshui/Documents/Research Project/bose_speaker/local_traffic"

# Create target directory
mkdir -p "$dst_directory"

for pcap_file in "$src_directory"/*.pcap; do
    base_name=$(basename "$pcap_file")
    # Define a new save path
    new_path="$dst_directory/$base_name"
    # Use tshark to filter traffic
    tshark -r "$pcap_file" -w "$new_path" "(ip.src >= 10.0.0.0 and ip.src <= 10.255.255.255 or ip.src >= 172.16.0.0 and ip.src <= 172.31.255.255 or ip.src >= 192.168.0.0 and ip.src <= 192.168.255.255) and (ip.dst >= 10.0.0.0 and ip.dst <= 10.255.255.255 or ip.dst >= 172.16.0.0 and ip.dst <= 172.31.255.255 or ip.dst >= 192.168.0.0 and ip.dst <= 192.168.255.255)"
done
