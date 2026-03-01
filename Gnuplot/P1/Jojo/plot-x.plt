reset
set encoding utf8 

# set terminal epslatex color
# set out 'TV3.tex' #################

# ============================ Plot Settings ============================



set title "Jojo-Bewegung (t, x)"
set ylabel 'X-Auslenkung (m)'
set xlabel 'Zeit (s)'
# set grid
set xrange [0:10]
set yrange [-0.1:0.1]
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
    'data-60fps.csv' using 1:2 with points ls 4 notitle, \
    'data-60fps.csv' using 1:2 with lines ls 5 notitle




# set out