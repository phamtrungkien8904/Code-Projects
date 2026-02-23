reset
set encoding utf8 



# ============================ Plot Settings ============================

set title 'Resonanzkurve für eine Oberschwingung'
set ylabel 'Mikrofonspannung (mV)'
set xlabel 'Frequenz (Hz)'
# set grid
set xrange [700:900]
set yrange [0:1000]
set datafile separator ','
set samples 10000



# Styling
# Use valid color syntax and distinct colors per dataset
set style line 1 pt 7 ps 0.3 lc rgb 'black'
set style line 2 pt 7 ps 0.3 lc rgb 'blue' 
set style line 3 pt 7 ps 0.3 lc rgb 'purple'
set style line 4 pt 7 ps 1.0 lc rgb 'red'




# Plot
plot \
    'data-4.csv' using 1:2 with points ls 4 notitle



# set out