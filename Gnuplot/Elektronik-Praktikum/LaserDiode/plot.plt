reset
set encoding utf8 

set terminal epslatex color
set out 'day1.tex'

# ============================ Plot Settings ============================

set title 'Characteristic Curve of Photodiode'
set xlabel 'U (V)'
set ylabel 'I (mA)'
# set grid
set xrange [0:0.7]
set yrange [-4:10]
set datafile separator ','
set samples 10000

# ---------------- Measurement (instrument) uncertainties ----------------
  

# Linear Regression Fit
I1(x) = I01*(exp(a*x) - 1) + b
I2(x) = I02*(exp(c*x) - 1) + d


set fit quiet
fit I1(x) 'data101.csv' using 3:4 via I01,a,b
b= 0.00000011
fit I2(x) 'data102.csv' using 3:4 via I02,c,d
d = -2.5570558
c = a
I02 = I01


# Styling
# Use valid color syntax and distinct colors per dataset

set style line 4 pt 7 ps 0.5 lc rgb 'red'
set style line 3 lw 2 lc rgb 'orange'
set style line 1 lw 2 lc rgb 'blue'
set style line 2 lw 2 lc rgb 'black'





# Plot
plot \
    'data101.csv' using 3:4 with points ls 4 title 'Data (dark)', \
    'data102.csv' using 3:4 with points ls 3 title 'Data (light)', \
    I2(x) with lines ls 2 title 'Fit (light)', \
    I1(x) with lines ls 1 title 'Fit (dark)'

set out