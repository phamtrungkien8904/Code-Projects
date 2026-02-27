reset
set encoding utf8 

# set terminal epslatex color
# set out 'TV6.tex' #################

# ============================ Plot Settings ============================



set title "Intensitätsprofil"
set ylabel 'Intensität/Imax'
set xlabel 'Pixel'
# set grid
set xrange [0:2048]
set yrange [0:150]
# set format x "%.0s%c"
set datafile separator ','
set samples 10000


# Styling
# Use valid color syntax and distinct colors per dataset
set style line 1 lw 1.5 pt 7 ps 0.5 lc rgb 'black' dt 4
set style line 2 lw 2 pt 7 ps 0.5 lc rgb 'blue' 
set style line 3 lw 2 pt 7 ps 0.5 lc rgb 'purple'
set style line 4 pt 4 lc rgb 'red' 



# Plot
plot \
    'TV6.csv' using 1:2 with lines ls 4 title 'Data'


# set out