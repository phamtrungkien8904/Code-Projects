reset
set encoding utf8 

# ============================ Plot Settings ============================

set title 'Characteristic Curve of Laser Diode'
set xlabel 'Laser Diode Current (mA)'
set ylabel 'Photo Diode Current (uA)'
# set grid
# set xrange [-50:50]
# set yrange [-500:500]
set datafile separator ','
set samples 10000

# ---------------- Measurement (instrument) uncertainties ----------------
  

# Linear Regression Fit
# f(x) = a*x+b

# set fit quiet
# fit f(x) 'data.csv' using 1:2 via a,b 


# Styling
set style line 1 lt 1 lw 2 lc rgb '#d62728'
set style line 2 pt 7 ps 1 lc rgb '#111111'


# Plot
plot \
	'data1.csv' using ($1):($2) with points ls 2 title 'Data'
	# f(x) with lines ls 1 title 'Fit'