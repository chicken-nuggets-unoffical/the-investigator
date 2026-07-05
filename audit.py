import re
from collections import Counter

# Step 1: Open and read the log file
with open("server_access.log", "r") as log_file:
    lines = log_file.readlines()

# Step 2 & 3: Find FAILED LOGIN lines and extract IP addresses
ip_pattern = re.compile(r"FAILED LOGIN attempt from (\d+\.\d+\.\d+\.\d+)")
failed_ips = []

for line in lines:
    if "FAILED LOGIN" in line:
        match = ip_pattern.search(line)
        if match:
            failed_ips.append(match.group(1))

# Step 4: Count how many times each IP appears
ip_counts = Counter(failed_ips)

# Step 5: Print summary sorted from most to fewest attempts
print("=== Failed Login Summary ===")
for ip, count in ip_counts.most_common():
    print(f"{ip}: {count} failed attempt(s)")
