reset
set encoding utf8 

# set terminal epslatex color
# set out 'TV4.tex' #################

# ============================ Plot Settings ============================

set title 'Resonanzkurve für eine Oberschwingung'
set ylabel 'Mikrofonspannung (mV)'
set xlabel 'Frequenz (Hz)'
# set grid
set xrange [740:900]
set yrange [0:1000]
set datafile separator ','
set samples 10000







# Styling
# Use valid color syntax and distinct colors per dataset
set style line 1 lw 1.5 pt 7 ps 0.5 lc rgb 'black' dt 4
set style line 2 lw 2 pt 7 ps 0.5 lc rgb 'blue' 
set style line 3 lw 2 pt 7 ps 0.5 lc rgb 'purple'
set style line 4 pt 4 lw 1.5 lc rgb 'red' 


# Peak frequency (from max V in column 2)
stats 'data-4.csv' using 2 nooutput
Vmax = STATS_max
stats 'data-4.csv' using (column(2) == Vmax ? column(1) : 1/0) nooutput
f2 = STATS_min

set arrow 1 from f2, graph 0 to f2, graph 1 nohead dt 2 lw 1.5 lc rgb 'black'
set label 1 sprintf('f_2 = %.0f Hz', f2) at f2 + 2, Vmax + 20 tc rgb 'black'



# Plot
plot \
    'data-4.csv' using 1:2 smooth csplines with line ls 4 title 'Fitkurve', \
    'data-4.csv' using 1:2 with point ls 4 title 'Messdaten'

# set out