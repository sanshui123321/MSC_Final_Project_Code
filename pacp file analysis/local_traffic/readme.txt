The calculation of this folder first filters out all local traffic, and then calculates the proportion of each protocol package in the local traffic.
The data input when running the code is the original pcap file, and the generated local traffic pcap file is saved to this folder.
First run the filter_traffic.sh script to filter out all local traffic and generate a new pcap file.
Then run calculate_protocol.py to calculate the corresponding proportion of each protocol type in the local traffic, and finally generate a txt file.