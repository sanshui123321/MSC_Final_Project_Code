import os
import csv

SOURCE_DIR = "/Users/sanshui/Documents/Research Project/bose_speaker/server_vs_local"

# Define the local IP ranges
local_ip_ranges = [
    ("10.0.0.0", "10.255.255.255"),
    ("172.16.0.0", "172.31.255.255"),
    ("192.168.0.0", "192.168.255.255")
]

def is_local_ip(ip):
    for start, end in local_ip_ranges:
        if start <= ip <= end:
            return True
    return False

total_local_volume = 0
total_server_volume = 0
local_communication_count = 0
server_communication_count = 0
total_communication_count = 0

for file_name in os.listdir(SOURCE_DIR):
    if file_name.endswith(".csv"):
        file_path = os.path.join(SOURCE_DIR, file_name)

        with open(file_path, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                src_ip = row["ip.src"]
                dst_ip = row["ip.dst"]
                
                if not src_ip or not dst_ip:
                    continue

                frame_len = int(row["frame.len"])
                total_communication_count += 1

                if is_local_ip(src_ip) and is_local_ip(dst_ip):
                    total_local_volume += frame_len
                    local_communication_count += 1
                else:
                    total_server_volume += frame_len
                    server_communication_count += 1

total_volume = total_local_volume + total_server_volume

result = f"""
Local Traffic Volume: {total_local_volume} bytes
Server Traffic Volume: {total_server_volume} bytes
Percentage of Local Traffic Volume to Total: {total_local_volume / total_volume * 100:.2f}%
Percentage of Server Traffic Volume to Total: {total_server_volume / total_volume * 100:.2f}%

Total Communication Count: {total_communication_count}
Local Traffic Communication Count: {local_communication_count}
Server Traffic Communication Count: {server_communication_count}
Percentage of Local Traffic Communication to Total: {local_communication_count / total_communication_count * 100:.2f}%
Percentage of Server Traffic Communication to Total: {server_communication_count / total_communication_count * 100:.2f}%
"""

with open(os.path.join(SOURCE_DIR, "result.txt"), 'w') as output_file:
    output_file.write(result)

print(result)
