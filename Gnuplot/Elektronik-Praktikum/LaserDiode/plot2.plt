reset
set encoding utf8 

set terminal epslatex color
set out 'day42.tex'

# ============================ Plot Settings ============================

set title 'LDA Signal and Op-Amp Response over Time'
set ylabel '$V$(V)'
set xlabel 't (s)'

# set title 'OpAmp Output vs. Input Difference Voltage in time'
# set ylabel '$V_{out}$(V), $V_\text{in}-V_\text{ref}$(10$\cdot$mV)'
# set xlabel '$t$ (s)'
# set grid
set xrange [0:2]
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
    'data407.csv' using 1:3 with points ls 1 title 'Output of Op-Amp',\
    'data407.csv' using 1:4 with points ls 3 title 'LDA Signal',\
    'data407.csv' using 1:($2-180)/10 with points ls 2 title 'Input of Op-Amp'
set out