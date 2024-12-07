import os
import json
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Directory containing JSON files
<<<<<<< Updated upstream:Project Python/SocialMedia/facebook.py
directory = r"D:\Chat log\specific"
=======
directory = r"/home/kien/Desktop/test"
>>>>>>> Stashed changes:facebook.py

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

# Calculate the total number of messages
total_messages = message_counts.sum()
print(f"Total number of messages: {total_messages}")

# Plot a bar chart
plt.figure(figsize=(12, 6))
ax = message_counts.plot(kind="bar", color="skyblue", label='Messages')
plt.title("Number of Messages Per Month", fontsize=16)
plt.xlabel("Month", fontsize=14)
plt.ylabel("Number of Messages", fontsize=14)
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle="--", alpha=0.7)
plt.tight_layout()

# Add a line connecting the columns
ax.plot(message_counts.index.astype(str), message_counts.values, color='orange', marker='o', linestyle='-', linewidth=2, label='Trend Line')

# Add total number of messages as text annotation
plt.text(0.2, 0.95, f'Total Messages: {total_messages}', 
         horizontalalignment='right', 
         verticalalignment='top', 
         transform=plt.gca().transAxes, 
         fontsize=12, 
         bbox=dict(facecolor='white', alpha=0.5))

# Add legend
plt.legend()

# Show the plot
plt.show()
