import os
import json
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Directory containing JSON files
directory = r"/home/kien/Desktop/embe-ig"


# Initialize a list to store all message timestamps
timestamps = []

# Iterate through all JSON files in the directory
for root, _, files in os.walk(directory):
    for filename in files:
        if filename.endswith(".json"):
            filepath = os.path.join(root, filename)
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as file:
                data = json.load(file)
                # Extract timestamps from the messages
                for message in data.get("messages", []):
                    timestamp_ms = message.get("timestamp_ms")
                    if timestamp_ms:  # Check if timestamp exists
                        timestamps.append(int(timestamp_ms) // 1000)  # Convert ms to seconds


# Convert timestamps to datetime
dates = [datetime.fromtimestamp(ts) for ts in timestamps]

# Create a DataFrame to aggregate messages by month
df = pd.DataFrame({"date": dates})
df["year_month"] = df["date"].dt.to_period("M")  # Group by year and month

# Count messages per month
message_counts = df["year_month"].value_counts().sort_index()

# Calculate the total number of messages
total_messages = message_counts.sum()
print(f"Total number of messages: {total_messages}")
# Convert the index and values of the message_counts to lists
year_month_list = list(message_counts.index.astype(str))
message_count_list = list(message_counts.values)

print("Year-Months:", year_month_list)
print("Message Counts:", message_count_list)

# Plot a bar chart
plt.figure(figsize=(12, 6))
message_counts.plot(kind="bar", color="skyblue")
plt.title("Number of Messages Per Month", fontsize=16)
plt.xlabel("Month", fontsize=14)
plt.ylabel("Number of Messages", fontsize=14)
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle="--", alpha=0.7)
plt.tight_layout()

# Show the plot
plt.show()
