pattern = "CAGATT"
with open("genom.txt", "r", encoding="utf-8") as f:
    count = sum(1 for line in f if pattern in line)
print(count)