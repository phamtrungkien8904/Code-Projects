reset
set encoding utf8 

# set terminal epslatex color
# set out 'TV4.tex' #################

# ============================ Plot Settings ============================



set title "Transmittierter Leistung gegen Strahldurchmesser"
set ylabel 'Transmittierte Leistung $P$ (mW)'
set xlabel 'Strahldurchmesser $d$ (mm)'
# set grid
set xrange [0:10]
set yrange [0:1100]
# set format x "%.0s%c"
set datafile separator ','
set samples 10000


# Styling
# Use valid color syntax and distinct colors per dataset
set style line 1 lw 1.5 pt 7 ps 0.5 lc rgb 'black' dt 4
set style line 2 lw 2 pt 7 ps 0.5 lc rgb 'blue' 

set style line 3 lw 2 pt 7 ps 0.5 lc rgb 'purple'
set style line 4 lw 1.5 pt 4 lc rgb 'red' 
set style line 5 lw 2 pt 4 lc rgb 'black' 



# Plot
plot \
    'data.csv' using 1:2 with points ls 4 title 'Messdaten'


# set out