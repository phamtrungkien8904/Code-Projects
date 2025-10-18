reset
set encoding utf8 

set terminal epslatex color
set out 'day33.tex'

# ============================ Plot Settings ============================

set title 'OpAmp Output vs. Input Difference Voltage in time'
set ylabel '$V_{out}$(V), $V_\text{in}-V_\text{ref}$(10$\cdot$mV)'
set xlabel '$t$ (s)'
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
    'data5.csv' using 1:($3/10) with points ls 3 title 'Test Input Signal - Vref',\
    'data5.csv' using 1:2 with points ls 4 title 'Output Signal'
    # 'data4.csv' using 1:($3/10) with points ls 3 title 'Test Input Signal - Vref',\
    # 'data4.csv' using 1:2 with points ls 4 title 'Output Signal',\
    # 'data4.csv' using 1:($4/10) with points ls 2 title 'Reference Signal'
    # 'data1.csv' using 1:($3/10) every 10 with points ls 4 title 'Output',\
    # 'data1.csv' using 1:2 every 10 with points ls 2 title 'Input'
    # 'data2.csv' using 3:2 every 10 with points ls 2 title '10 Hz'



    # 'data3.csv' using 3:2 with points ls 3 title '10 Hz with R6',\
    # 'data5.csv' using 3:2 with points ls 1 title '1 Hz LPF',\
    # 'data6.csv' using 3:2 with points ls 2 title '3 Hz LPF',\
    # 'data8.csv' using 3:2 with points ls 3 title '7 Hz LPF',\
    # 'data9.csv' using 3:2 with points ls 4 title '10 Hz LPF',\
    # 'data10.csv' using 3:2 with points ls 1 title '15 Hz LPF',\
    # 'data11.csv' using 3:2 with points ls 2 title '20 Hz LPF'

set out