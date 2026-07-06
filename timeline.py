"""Merge auth and file events into a single chronological timeline."""

from datetime import datetime

AUTH_LOG = "auth_events.log"
FILE_LOG = "file_events.log"

KEY_MARKERS = ("SUCCESS LOGIN", ".locked", "READ_ME")

# Step 1: Read all events from both log files
events = []
for log_file in (AUTH_LOG, FILE_LOG):
    with open(log_file) as f:
        for line in f:
            line = line.strip()
            if line:
                events.append(line)

# Step 2: Sort events chronologically (date and time are at the start of each line)
events.sort(key=lambda line: line[:19])

# Step 3: Print the merged timeline, flagging key events
for event in events:
    if any(marker in event for marker in KEY_MARKERS):
        print(f"{event}  *** KEY EVENT ***")
    else:
        print(event)

# Step 4: Calculate dwell time from first malicious login to first locked file
first_login = next(e for e in events if "SUCCESS LOGIN" in e)
first_locked = next(e for e in events if ".locked" in e)

login_time = datetime.strptime(first_login[:19], "%Y-%m-%d %H:%M:%S")
locked_time = datetime.strptime(first_locked[:19], "%Y-%m-%d %H:%M:%S")
dwell = locked_time - login_time

total_seconds = int(dwell.total_seconds())
minutes, seconds = divmod(total_seconds, 60)
hours, minutes = divmod(minutes, 60)

if hours:
    dwell_str = f"{hours} hours {minutes} minutes {seconds} seconds"
elif minutes:
    dwell_str = f"{minutes} minutes {seconds} seconds"
else:
    dwell_str = f"{seconds} seconds"

print()
print(f"Dwell time (first malicious login -> first locked file): {dwell_str}")
