reset
set encoding utf8 

# set terminal epslatex color
# set out 'day34.tex'

# ============================ Plot Settings ============================



set title 'Test Signal'
set ylabel 'Signal (V)'
set xlabel 'Time (s)'
# set grid
# set xrange [-180:200]
# set yrange [-2:2]
set datafile separator ','
# set samples 10000

# ---------------- Measurement (instrument) uncertainties ----------------
  

# Linear Regression Fit
# f(x) = a*x+b

# set fit quiet
# fit f(x) 'data.csv' using 1:2 via a,b 


# Styling
# Use valid color syntax and distinct colors per dataset
set style line 1 pt 7 ps 0.3 lc rgb 'black'
set style line 2 pt 7 ps 0.3 lc rgb 'blue' 
set style line 3 pt 7 ps 0.3 lc rgb 'purple'
set style line 4 pt 7 ps 0.3 lc rgb 'red'




# Plot
plot \
    'signal.csv' using 2:3 with points ls 2 title 'Signal'



# set out