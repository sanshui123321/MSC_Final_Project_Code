#!/bin/bash

SOURCE_DIR="/Users/sanshui/Documents/Research Project/bose_speaker/original_pcap"
DEST_DIR="/Users/sanshui/Documents/Research Project/bose_speaker/server_vs_local"

for file in "$SOURCE_DIR"/*.pcap; do
    base_name=$(basename "$file" .pcap)
    tshark -r "$file" -T fields -e ip.src -e ip.dst -e frame.len -E header=y -E separator=, -E quote=d -E occurrence=f > "$DEST_DIR/${base_name}.csv"
done
