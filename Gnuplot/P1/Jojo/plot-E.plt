reset
set encoding utf8 

# set terminal epslatex color
# set out 'TV3.tex' #################

# ============================ Plot Settings ============================



set title "Jojo-Bewegung (t, E)"
set ylabel 'Energie (J)'
set xlabel 'Zeit (s)'
# set grid
set xrange [0:10]
set yrange [0:10]
# set format x "%.0s%c"
set datafile separator ','
set samples 10000

# Energy from measured data: E = m*g*y (y is column 3 in data-60fps.csv)
m = 1.0
g = 9.81

# Styling
# Use valid color syntax and distinct colors per dataset
set style line 1 lw 1.5 pt 7 ps 0.5 lc rgb 'black' dt 4
set style line 2 lw 2 pt 7 ps 0.5 lc rgb 'blue' 
set style line 3 lw 2 pt 7 ps 0.5 lc rgb 'purple'
set style line 4 lw 1.5 pt 4 lc rgb 'red' 
set style line 5 lw 2 pt 4 lc rgb 'black' 



# Plot
plot \
    'data-60fps-peaks.csv' using 1:(m*g*$2) with points ls 4 title 'E = m g y (peaks)', \
    'data-60fps-peaks.csv' using 1:(m*g*$2) with lines ls 5 notitle




# set out