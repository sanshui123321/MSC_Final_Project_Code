#!/bin/bash

TRAFFIC_DIR='/home/tao/test_code_tao_blocked/traffic_pcap' # File for saving pcap file
experiment_name='google_nest'
mac_address='38:86:f7:79:1d:15'

# Start the moniotr 
cd /opt/moniotr
/opt/moniotr/bin/tag-experiment.sh start $mac_address $experiment_name
sleep 5



