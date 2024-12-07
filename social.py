import os
import json
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Directory containing JSON files
directory = r"D:\Chat log\test"

# Initialize a list to store all message timestamps
timestamps = []

# Iterate through all JSON files in the directory
for filename in os.listdir(directory):
    if filename.endswith(".json"):
        filepath = os.path.join(directory, filename)
        with open(filepath, 'r', encoding='utf-8') as file:
            data = json.load(file)
            # Extract timestamps from the messages
            for message in data.get("messages", []):
                timestamp_ms = message.get("timestamp")
                if timestamp_ms:  # Check if timestamp exists
                    timestamps.append(timestamp_ms // 1000)  # Convert ms to seconds

# Convert timestamps to datetime
dates = [datetime.fromtimestamp(ts) for ts in timestamps]

# Create a DataFrame to aggregate messages by month
df = pd.DataFrame({"date": dates})
df["year_month"] = df["date"].dt.to_period("M")  # Group by year and month

# Count messages per month
message_counts = df["year_month"].value_counts().sort_index()

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
