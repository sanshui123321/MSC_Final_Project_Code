import os
import subprocess
from collections import defaultdict

src_directory = "/Users/sanshui/Documents/Research Project/bose_speaker/server_traffic"
output_file_path = os.path.join(src_directory, "protocol_analysis.txt")

domain_to_ip = {
    "0.bose.pool.ntp.org": ["85.119.83.206", "95.215.175.2", "217.114.59.66", "162.159.200.123"],
    "1.bose.pool.ntp.org": ["51.89.151.183", "217.114.59.3", "85.199.214.98", "85.119.84.153"],
    "id.api.bose.io": ["34.237.118.24"],
    "content.api.bose.io": ["34.237.118.24"],
    "iot.api.bose.io": ["34.237.118.24"],
    "users.api.bose.io": ["34.237.118.89"],
    "ota.cdn.bose.io": ["18.164.68.107", "18.164.68.19", "18.164.68.101", "18.164.68.77"],
    "adhj3uk4ouxyr.iot.us-east-1.amazonaws.com": ["54.167.164.29", "54.242.11.196", "52.7.111.165", "52.54.20.148", "52.2.253.120", "54.226.202.10", "107.23.57.254", "52.2.55.114"],
    "media.bose.io": ["99.84.9.123", "99.84.9.9", "99.84.9.77", "99.84.9.80"],
    "data.api.bose.io": ["3.232.190.0", "54.204.250.0", "54.236.130.172", "35.169.149.17", "52.5.55.32", "3.234.23.184"]
}




ip_to_domain = {}
for domain, ips in domain_to_ip.items():
    for ip in ips:
        ip_to_domain[ip] = domain

protocol_stats = defaultdict(lambda: defaultdict(lambda: {"count": 0, "total_size": 0}))

for pcap_file in os.listdir(src_directory):
    if pcap_file.endswith(".pcap"):
        print(f"Processing {pcap_file} ...")

        # Use tshark to extract application layer protocol data
        command = [
            "tshark",
            "-r", os.path.join(src_directory, pcap_file),
            "-T", "fields",
            "-e", "ip.dst",
            "-e", "_ws.col.Protocol",
            "-e", "ip.len"
        ]
        
        result = subprocess.check_output(command).decode('utf-8').strip().split("\n")
        for line in result:
            values = line.split("\t")
            if len(values) != 3:
                 continue
            ip, protocol, size = values
            if ip in ip_to_domain: 
                domain = ip_to_domain[ip]
                protocol_stats[domain][protocol]["count"] += 1
                protocol_stats[domain][protocol]["total_size"] += int(size)

with open(output_file_path, 'w') as f:
    for domain, data in protocol_stats.items():
        total_packets = sum([stats["count"] for stats in data.values()])
        f.write(f"Domain: {domain}\n")
        f.write(f"Total Packets: {total_packets}\n")
        for protocol, proto_data in data.items():
            f.write(f"  Protocol: {protocol}\n")
            f.write(f"  Packet Ratio: {proto_data['count'] / total_packets * 100:.2f}%\n")
            f.write(f"  Average Packet Size: {proto_data['total_size'] / proto_data['count']:.2f} bytes\n")
            f.write(f"  Total Data Size: {proto_data['total_size']} bytes\n")
        f.write("----------------------\n")

print(f"Analysis completed. Check the results in {output_file_path}.")
