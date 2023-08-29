#!/bin/bash

# Set input folder path and output file path
input_folder="/Users/sanshui/Documents/Research Project/bose_speaker/original_pcap"
output_file="/Users/sanshui/Documents/Research Project/bose_speaker/IP_DNS/IP_DNS.txt"

# Iterate over all pcap files in the input folder
for pcap_file in "$input_folder"/*.pcap; do
    echo "Processing file: $pcap_file"

    # Extract date and time from filename
    filename=$(basename "$pcap_file")
    datetime="${filename%%_*}"

    # Add the filename to the output file
    tshark -r "$pcap_file" -Y 'dns.flags.response == 1' -T fields -e dns.qry.name -e dns.a -E separator=, >> "$output_file"

    echo "Finished processing file: $pcap_file"
done

