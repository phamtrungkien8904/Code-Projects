reset
set encoding utf8 

# ============================ Plot Settings ============================

set title 'Characteristic Curve of Laser Diode'
set xlabel 'Vout (V)'
set ylabel 'Vin - Vref (mV)'
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
# Use valid color syntax and distinct colors per dataset
set style line 1 pt 7 ps 0.5 lc rgb 'black'
set style line 2 pt 7 ps 0.5 lc rgb 'blue' 
# set style line 3 pt 7 ps 0.5 lc rgb 'purple'
# set style line 4 pt 7 ps 0.5 lc rgb 'red'




# Plot
plot \
	'data1.csv' using 3:2 with points ls 1 title 'Data 1 1 Hz', \
    'data2.csv' using 3:2 with points ls 2 title 'Data 2 10 Hz'