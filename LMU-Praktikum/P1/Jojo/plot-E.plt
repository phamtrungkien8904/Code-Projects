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
set yrange [0:2]
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


E(y,vy,ay) = y + 0.5*vy**2/abs(ay)

# Plot
plot \
    'data-60fps.csv' using 1:(E($3,$4,$5)) with points ls 4 title 'Messdaten', \
    'data-60fps-peaks.csv' using 1:2 with points ls 4 notitle, \
    'data-60fps-peaks.csv' using 1:2 with lines ls 1 title 'Peaks'




# set out