import matplotlib.pyplot as plt
import numpy as np

# Merge the two lists of year-months and message counts
# Instagram data
total_messages_1 = 69107 
year_month_list_1 = ['2024-06', '2024-07', '2024-08', '2024-09', '2024-10', '2024-11', '2024-12', '2025-01']
message_count_list_1 = [np.int64(1803), np.int64(13559), np.int64(14280), np.int64(19320), np.int64(18736), np.int64(635), np.int64(67), np.int64(707)]
# Facebook data
total_messages_2 = 127427
year_month_list_2 = ['2024-06', '2024-07', '2024-08', '2024-09', '2024-10', '2024-11', '2024-12', '2025-01']
message_count_list_2 = [np.int64(300),np.int64(2426), np.int64(454), np.int64(1939), np.int64(17333), np.int64(44090), np.int64(27967), np.int64(33011)]

# Merge the two lists of message counts
total_messages = total_messages_1 + total_messages_2
message_count_list = [count1 + count2 for count1, count2 in zip(message_count_list_1, message_count_list_2)]

print("Total number of messages:", total_messages)
print("Year-Months:", year_month_list_1)
print("Message Counts:", message_count_list)

import matplotlib.pyplot as plt

# Merge the two lists of message counts
total_messages = total_messages_1 + total_messages_2
message_count_list = [count1 + count2 for count1, count2 in zip(message_count_list_1, message_count_list_2)]

print("Total number of messages:", total_messages)
print("Year-Months:", year_month_list_1)
print("Message Counts:", message_count_list)

# Create bar chart with merged data
plt.figure(figsize=(12, 6))
ax = plt.gca()

# Plot bar chart
ax.bar(year_month_list_1, message_count_list, color="skyblue", label="Messages")

# Plot trend line connecting the columns (peak line)
ax.plot(year_month_list_1, message_count_list, color="orange", marker="o", linestyle="-", linewidth=2, label="Trend Line")

# Rotate x-axis labels by 45 degrees
plt.xticks(rotation=45)

# Annotate total number of messages at the top-right corner of the plot
plt.text(0.95, 0.95, f"Total Messages: {total_messages}",
         transform=ax.transAxes,
         horizontalalignment="right",
         verticalalignment="top",
         fontsize=12)

plt.title("Merged Number of Messages Per Month (em be Anh)", fontsize=16)
plt.xlabel("Month", fontsize=14)
plt.ylabel("Number of Messages", fontsize=14)
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.legend()
plt.tight_layout()
plt.show()