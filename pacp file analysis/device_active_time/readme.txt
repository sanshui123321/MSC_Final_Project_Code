This folder is used to analyze the active status of iot devices.
The input is the raw pcap file.
First run the extract_pcap_info.sh file to process the original pcap file, and the generated txt file is stored in this file.
Then run the device_active_time.py file to process the txt file and generate the device_active_time file record result.
The Txt file stores the communication times (frequency) of each time period and the proportion of the communication times in this time period to the total times.
Simultaneously output a line chart.