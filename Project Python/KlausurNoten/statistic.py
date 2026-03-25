import numpy as np
import matplotlib.pyplot as plt
import csv
from matplotlib.patches import Patch
plt.style.use('classic')
# plt.rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
# plt.rc('text', usetex=True) 


note = np.array([])
with open('T2-hauptklausur.csv', 'r') as rf:
    reader = csv.reader(rf, delimiter=',')
    next(reader)  # Skip header
    for row in reader:
      note = np.append(note, float(row[1]))

# Schema T2 haupt
cutoff = 25
top = 55
def grade_for_points(points):
  # Notenschema 
  if points >= 55:
    return '1.0'
  if points >= 45:
    return '2.0'
  if points >= 35:
    return '3.0'
  if points >= 25:
    return '4.0'
  return '5.0 (NB)'

# cutoff = 10.5
# top = 33
# def grade_for_points(points):
#   # Notenschema 
#   if points >= top:
#     return '1.0'
#   if points >= 22.5:
#     return '2.0'
#   if points >= 18:
#     return '3.0'
#   if points >= cutoff:
#     return '4.0'
#   return '5.0 (NB)'

grade_colors = {
  '1.0': '#1b9e77',
  '2.0': '#a6d96a',
  '3.0': '#fdae61',
  '4.0': '#a50026',
  '5.0 (NB)': '#6a3d9a'
}

# Analysis
Kien_Punkte = 20.0
mu = np.mean(note)
sigma = np.std(note)

Max = 79.0
print('Total number of students: ', len(note))
print(f'Number of blank papers (not come): {np.sum(note == 0)} ({np.sum(note == 0) / len(note) * 100:.1f}%)')
print(f'Number of failed students: {np.sum(note < cutoff)} ({np.sum(note < cutoff) / len(note) * 100:.1f}%)')
print(f'Number of top students: {np.sum(note >= top)} ({np.sum(note >= top) / len(note) * 100:.1f}%)')
print(f'Mean: {mu:.2f} (Note: {grade_for_points(mu)})')
print(f'Standard Deviation: {sigma:.2f}')
print("---------------------------")
print(f'Kien Punkte: {Kien_Punkte} (Note: {grade_for_points(Kien_Punkte)})')

stats_text = (
  f'Total students: {len(note)}\n'
  f'Failed (<{cutoff}): {np.sum(note < cutoff)} ({np.sum(note < cutoff) / len(note) * 100:.1f}%)\n'
  f'Nerd (>= {top}): {np.sum(note >= top)} ({np.sum(note >= top) / len(note) * 100:.1f}%)\n'
  f'Mean: {mu:.2f} ({grade_for_points(mu)})\n'
  f'Std: {sigma:.2f}'
)

plt.figure(figsize=(8, 8))

bins = np.arange(0, 80, 0.5)
weights = np.ones_like(note) * 100.0 / len(note)
counts, bin_edges, patches = plt.hist(note, bins=bins, weights=weights, edgecolor='black', align='mid', density=False)

for left, right, patch in zip(bin_edges[:-1], bin_edges[1:], patches):
  midpoint = (left + right) / 2
  patch.set_facecolor(grade_colors[grade_for_points(midpoint)])

plt.axvline(mu, color='navy', linestyle='--', linewidth=1)
plt.text(mu - 0.4, np.max(counts) * 0.95, rf'$\mu = {mu:.2f}$', rotation=90, color='navy', ha='right', va='top' ,fontsize=15)

# plt.axvline(Kien_Punkte, color='navy', linestyle='--', linewidth=1)
# plt.text(Kien_Punkte - 0.4, np.max(counts) * 0.95, f'$Kien = {Kien_Punkte:.2f}$', rotation=90, color='navy', ha='right', va='top')

# Gaussian fit scaled to histogram counts

x = np.linspace(bin_edges[0], bin_edges[-1], 600)
bin_width = bin_edges[1] - bin_edges[0]
gaussian = (1 / (sigma * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mu) / sigma) ** 2)
gaussian_scaled = gaussian * bin_width * 100
plt.plot(x, gaussian_scaled, color='black', linewidth=3, label='Gaussian')

plt.xlabel('Points (0-80)')
plt.ylabel('Students [%]')
plt.title('Distribution of Points in QM Exam at LMU')
plt.text(
  0.5,
  0.6,
  stats_text,
  transform=plt.gca().transAxes,
  ha='left',
  va='top',
  fontsize=15,
  bbox=dict(boxstyle='round,pad=0.50', facecolor='white', edgecolor='gray', alpha=0.75)
)
legend_handles = [plt.Line2D([0], [0], color=color, lw=4, label=grade) for grade, color in grade_colors.items()]
legend_handles.append(plt.Line2D([0], [0], color='black', lw=2, label='Gaussian'))
plt.legend(handles=legend_handles, title='Notenschema', loc='upper right')
# plt.grid(axis='y', alpha=0.3)
plt.show()


