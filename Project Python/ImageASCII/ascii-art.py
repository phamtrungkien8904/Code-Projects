import sys
import numpy as np
from PIL import Image

# Contrast on a scale -10 -> 10
contrast = 10
# R-String (raw string) verhindert den Escape-Fehler bei \|
density = (r'$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|'
           r'()1{}[]?-_+~<>i!lI;:,"^`    \'.            ')
density = density[:-11+contrast]
n = len(density)

img_name = sys.argv[1]
try:
    width = int(sys.argv[2])
except IndexError:
    # Default ASCII image width.
    width = 100

# Read in the image, convert to greyscale.
img = Image.open(img_name)
img = img.convert('L')
# Resize the image as required.
orig_width, orig_height = img.size
r = orig_height / orig_width
# The ASCII character glyphs are taller than they are wide. Maintain the aspect
# ratio by reducing the image height.
height = int(width * r * 0.5)

# BEHOBEN: Resampling-Filter für aktuelle Pillow-Versionen angepasst
img = img.resize((width, height), Image.Resampling.LANCZOS)

# Now map the pixel brightness to the ASCII density glyphs.
arr = np.array(img)
for i in range(height):
    for j in range(width):
        p = arr[i,j]
        k = int(np.floor(p/256 * n))
        print(density[n-1-k], end='')
    print()
