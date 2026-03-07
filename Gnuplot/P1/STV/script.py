import numpy as np
import csv

# Parameters
n = 12  # number of coins to pick
p = 0.22  # probability of a certain coin type
N = 20  # number of repetitions

# Perform N trials
results = []
for trial in range(N):
    # Pick n coins with probability p of being a certain type
    coins = np.random.binomial(n, p)
    results.append(coins)

# Calculate frequency distribution
unique, counts = np.unique(results, return_counts=True)
frequency_dist = dict(zip(unique, counts))

# Save to CSV
with open('data.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Number of Coins', 'Frequency'])
    for coin_num in sorted(frequency_dist.keys()):
        writer.writerow([coin_num, frequency_dist[coin_num]])

print("Data saved to data.csv")
print("Probability Distribution:")
for coin_num in sorted(frequency_dist.keys()):
    print(f"Coins: {coin_num}, Frequency: {frequency_dist[coin_num]}")
