reset
set encoding utf8 

# ============================ Plot Settings ============================

set title 'Characteristic Curve of Laser Diode'
set xlabel 'U (V)'
set ylabel 'I (mA)'
# set grid
set xrange [0:0.7]
set yrange [-5:10]
set datafile separator ','
set samples 10000

# ---------------- Measurement (instrument) uncertainties ----------------
  

# Linear Regression Fit
I(x) = I0*(exp(a*x) - 1) + b

set fit quiet
fit I(x) 'data102.csv' using 3:4 via I0,a,b


# Styling
# Use valid color syntax and distinct colors per dataset
set style line 1 pt 7 ps 0.5 lc rgb 'black'
set style line 2 pt 7 ps 0.5 lc rgb 'blue' 
set style line 3 pt 7 ps 0.5 lc rgb 'purple'
set style line 4 pt 7 ps 0.5 lc rgb 'red'




# Plot
plot \
    'data102.csv' using 3:4 with points ls 4 title 'Data', \
    I(x) with lines ls 1 title 'Fit'
