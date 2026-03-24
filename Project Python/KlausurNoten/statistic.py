import numpy as np
import matplotlib.pyplot as plt
import csv


note = np.array([])
with open('T2-hauptklausur.csv', 'r') as rf:
    reader = csv.reader(rf, delimiter=',')
    next(reader)  # Skip header
    for row in reader:
      note = np.append(note, float(row[1]))



print('Number of students: ', len(note))

# Plot histogram: x = note, y = number of students with that note
plt.hist(note, bins='auto', edgecolor='black')
plt.xlabel('Note')
plt.ylabel('Anzahl der Studierenden')
plt.title('Notenverteilung')
plt.grid(axis='y', alpha=0.3)
plt.show()