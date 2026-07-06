"""Analyze network traffic log for beaconing suspects."""

from collections import defaultdict

LOG_FILE = "network_traffic.log"

# Step 1: Read the log file line by line
with open(LOG_FILE) as f:
    lines = f.readlines()

# Step 2: Parse each line and count (source -> destination:port) pairs
pair_counts = defaultdict(int)
pair_timestamps = defaultdict(list)

for line in lines:
    line = line.strip()
    if not line:
        continue

    # Format: time  source_ip -> dest_ip:port  N bytes
    parts = line.split()
    timestamp = parts[0]
    source_ip = parts[1]
    dest = parts[3]  # destination IP:port (skip the '->' token)
    pair = f"{source_ip} -> {dest}"

    pair_counts[pair] += 1
    pair_timestamps[pair].append(timestamp)

# Step 3: Find the pair with the most connections
top_pair = max(pair_counts, key=pair_counts.get)
top_count = pair_counts[top_pair]
top_timestamps = pair_timestamps[top_pair]

# Step 4: Print the beaconing suspect report
print("=== Beaconing Suspect ===")
print(f"Pair: {top_pair}")
print(f"Connections: {top_count}")
print(f"Timestamps: {top_timestamps}")
