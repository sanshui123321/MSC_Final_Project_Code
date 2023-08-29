import os
from collections import defaultdict
import subprocess

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


ip_to_domain = {ip: domain for domain, ips in domain_to_ip.items() for ip in ips}

directory = "/Users/sanshui/Documents/Research Project/bose_speaker/server_traffic"
stats = defaultdict(lambda: {"count": 0, "total_size": 0})

total_count = 0
total_data_size = 0

for filename in os.listdir(directory):
    if filename.endswith(".pcap"):
        filepath = os.path.join(directory, filename)
        print(f"\nProcessing {filepath} ...\n")

        # Use the tshark command
        result = subprocess.run(['tshark', '-r', filepath, '-T', 'fields', '-e', 'ip.src', '-e', 'ip.dst', '-e', 'ip.len'], capture_output=True, text=True)
        lines = result.stdout.splitlines()
        for line in lines:
            parts = line.strip().split("\t")
            if len(parts) == 3:
                ip_src, ip_dst = parts[0], parts[1]
        
                # If ip.len contains a comma, skip this data
                if ',' in parts[2]:
                    print(f"Skipping line with multiple ip.len values in file {filename}.")
                    continue

                try:
                    size = int(parts[2])
                except ValueError:
                    print(f"Error processing size value '{parts[2]}' in file {filename}. Skipping this line.")
                    continue

                for ip in [ip_src, ip_dst]:
                    domain = ip_to_domain.get(ip, None)
                    if domain:
                        stats[domain]["count"] += 1
                        stats[domain]["total_size"] += size
                        total_count += 1
                        total_data_size += size


print("\nResults:")
for domain, data in stats.items():
    avg_size = data["total_size"] / data["count"]
    packet_ratio = data["count"] / total_count * 100
    data_size_ratio = data["total_size"] / total_data_size * 100

    print(f"Domain: {domain}")
    print(f"Average Packet Size: {avg_size:.2f} bytes")
    print(f"Total Data Size: {data['total_size']} bytes")
    print(f"Packet Ratio: {packet_ratio:.2f}%")
    print(f"Data Size Ratio: {data_size_ratio:.2f}%")
    print("----------------------\n")


with open("/Users/sanshui/Documents/Research Project/bose_speaker/server_traffic/results.txt", "w") as output_file:
    for domain, data in stats.items():
        avg_size = data["total_size"] / data["count"]
        packet_ratio = data["count"] / total_count * 100
        data_size_ratio = data["total_size"] / total_data_size * 100
        
        output_file.write(f"Domain: {domain}\n")
        output_file.write(f"Average Packet Size: {avg_size:.2f} bytes\n")
        output_file.write(f"Total Data Size: {data['total_size']} bytes\n")
        output_file.write(f"Packet Ratio: {packet_ratio:.2f}%\n")
        output_file.write(f"Data Size Ratio: {data_size_ratio:.2f}%\n")
        output_file.write("----------------------\n")

print("\nAnalysis complete. Results saved.")
