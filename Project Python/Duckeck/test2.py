pattern = "CAGATT"
with open("genom.txt", "r", encoding="utf-8") as f:
    count = sum(1 for line in f if pattern in line)
print(count)

pattern = "CAGATT"

with open("genom.txt", "r", encoding="utf-8") as f:
    genome = f.read().replace("\n", "").replace("\r", "")

count = genome.count(pattern)  # non-overlapping matches
print(count)