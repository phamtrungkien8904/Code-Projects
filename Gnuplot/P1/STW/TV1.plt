reset
set encoding utf8 



# ============================ Plot Settings ============================

set title 'Stehende Wellen in einer Luftsäule'
set ylabel 'Mikrofonspannung (mV)'
set xlabel 'Auslenkung (mm)'
# set grid
set xrange [50:300]
set yrange [0:100]
set datafile separator ','
set samples 10000







# Styling
# Use valid color syntax and distinct colors per dataset
set style line 1 lw 1.5 pt 7 ps 0.5 lc rgb 'black' dt 4
set style line 2 lw 2 pt 7 ps 0.5 lc rgb 'blue' 
set style line 3 lw 2 pt 7 ps 0.5 lc rgb 'purple'
set style line 4 lw 1.5 pt 4 lc rgb 'red' 




# Plot
plot \
    'data-1.csv' using 1:2 with point ls 4 title 'Messdaten', \


# set out