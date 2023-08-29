import os
from collections import defaultdict
import subprocess

def analyze_protocols(pcap_directory):
    # Get all .pcap files
    pcap_files = [f for f in os.listdir(pcap_directory) if f.endswith('.pcap')]

    # Defaultdict use to record the number of each protocol
    protocol_counts = defaultdict(int)

    # Traverse each .pcap file for analysis
    for pcap_file in pcap_files:
        pcap_path = os.path.join(pcap_directory, pcap_file)
        
        # Use the tshark command line tool to get the protocol of each packet
        cmd = ['tshark', '-r', pcap_path, '-T', 'fields', '-e', '_ws.col.Protocol']
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        for line in result.stdout.splitlines():
            protocol_counts[line.strip()] += 1
    
    # Calculate the total number of packets
    total_packets = sum(protocol_counts.values())
    
   # The analysis result is saved as a string
    output = []
    for protocol, count in protocol_counts.items():
        percentage = (count / total_packets) * 100
        output.append(f"{protocol}: {count} packets, {percentage:.2f}%")


    output_file_path = os.path.join(pcap_directory, "protocol_analysis.txt")
    with open(output_file_path, 'w') as f:
        f.write("\n".join(output))

    print(f"Analysis saved to {output_file_path}")

# Analyze pcap files in the specified directory
analyze_protocols("/Users/sanshui/Documents/Research Project/bose_speaker/local_traffic")
