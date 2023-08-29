#!/bin/bash

# Define source and destination folders
SOURCE_DIR="/Users/sanshui/Documents/Research Project/bose_speaker/original_pcap"
OUTPUT_DIR="/Users/sanshui/Documents/Research Project/bose_speaker/device_active_time"
OUTPUT="$OUTPUT_DIR/output.txt"


mkdir -p "$OUTPUT_DIR"

# Delete old output files that may exist
rm -f "$OUTPUT"

# Convert each pcap file to txt and append to OUTPUT
cd "$SOURCE_DIR" || exit
for file in *.pcap; do
    tshark -r "$file" -T fields -e frame.time -e frame.len >> "$OUTPUT"
    echo "Processing $file"
done
