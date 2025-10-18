reset
set encoding utf8 

set terminal epslatex color
set out 'day2.tex'

# ============================ Plot Settings ============================

set title 'Performance of Laser Diode'
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
# Use valid color syntax and distinct colors per dataset
set style line 1 pt 7 ps 0.5 lc rgb 'black'
set style line 2 pt 7 ps 0.5 lc rgb 'blue' 
set style line 3 pt 7 ps 0.5 lc rgb 'purple'
set style line 4 pt 7 ps 0.5 lc rgb 'red'




# Plot
plot \
	'data1.csv' using 1:2 every 100 with points ls 1 title 'Data 1',\
    'data2.csv' using 1:2 every 100 with points ls 2 title 'Data 2',\
	'data3.csv' using 1:2 every 100 with points ls 3 title 'Data 3',\
	'data4.csv' using 1:2 every 100 with points ls 4 title 'Data 4'
	# f(x) with lines ls 5 title 'Linear Fit'

set out