reset
set encoding utf8 

# set terminal epslatex color
# set out 'TV1.tex' #################

# ============================ Plot Settings ============================

set title 'Stehende Wellen in einer Luftsäule'
set ylabel 'Mikrofonspannung (mV)'
set xlabel 'Auslenkung (mm)'
# set grid
set xrange [50:300]
set yrange [0:100]
set datafile separator ','
set samples 10000




set fit quiet
f(x) = a*abs(sin(2*pi/lambda*x + phi))
a = 73.830
lambda = 140
fit f(x) 'data-1.csv' using 1:2 via a, lambda, phi


# ---------------------- Konstruktion der äußeren Minima ----------------------
# 5 symmetrische Strecken um das linke Minimum
$pairs_left << EOD
89,94,10.0630
87,96,16.5250
85,98,22.5065
83,100,28.2660
81,102,35.9305
EOD

# 5 symmetrische Strecken um das rechte Minimum
$pairs_right << EOD
228,234,11.1495
226,236,17.6655
224,238,23.4985
222,240,29.4385
220,242,35.8290
EOD

# Senkrechte Ausgleichsgerade x = const durch Mittelpunkte
xmin_left = (89 + 94 + 87 + 96 + 85 + 98 + 83 + 100 + 81 + 102)/10.0
xmin_right = (228 + 234 + 226 + 236 + 224 + 238 + 222 + 240 + 220 + 242)/10.0

# Zeichnerisch geschätzter Fehler der Positionsbestimmung
dx_left = 0.5
dx_right = 0.5

print sprintf('Äußeres Minimum links:  x = %.2f ± %.2f mm', xmin_left, dx_left)
print sprintf('Äußeres Minimum rechts: x = %.2f ± %.2f mm', xmin_right, dx_right)
print sprintf('Wellenlänge = (%.2f ± %.2f) mm', lambda, lambda_err)


# Styling
# Use valid color syntax and distinct colors per dataset
set style line 1 lw 1.5 pt 7 ps 0.5 lc rgb 'black' dt 4
set style line 2 lw 1.5 pt 7 ps 0.5 lc rgb 'blue' 
set style line 3 lw 1.5 pt 7 ps 0.5 lc rgb 'purple'
set style line 4 lw 1.5 pt 4 lc rgb 'red' 
set style line 5 lw 1.5 lc rgb 'dark-green'
set style line 6 pt 7 ps 0.8 lc rgb 'dark-green'

set arrow 11 from xmin_left, graph 0 to xmin_left, graph 1 nohead dt 2 lw 1.3 lc rgb 'dark-green'
set arrow 12 from xmin_right, graph 0 to xmin_right, graph 1 nohead dt 2 lw 1.3 lc rgb 'dark-green'

# set label 11 sprintf('x_{min,l} = %.1f ± %.1f mm', xmin_left, dx_left) at xmin_left - 34, 8 tc rgb 'dark-green'
# set label 12 sprintf('x_{min,r} = %.1f ± %.1f mm', xmin_right, dx_right) at xmin_right + 3, 8 tc rgb 'dark-green'




# Plot
plot \
    'data-1.csv' using 1:2 with point ls 4 title 'Messdaten', \
    f(x) with lines ls 2 title 'Fitkurve', \
    $pairs_left using 1:3:(($2-$1)):(0.0) with vectors nohead ls 5 title 'symm. Strecken', \
    $pairs_right using 1:3:(($2-$1)):(0.0) with vectors nohead ls 5 notitle, \
    $pairs_left using (($1+$2)/2.0):3 with points ls 6 title 'Mittelpunkte', \
    $pairs_right using (($1+$2)/2.0):3 with points ls 6 notitle

# set out