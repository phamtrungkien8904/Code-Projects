reset
set encoding utf8 

# set terminal epslatex color
# set out 'TV3.tex' #################

# ============================ Plot Settings ============================



set title "Jojo Bewegungsbahn"
set ylabel 'Höhe (m)'
set xlabel 'Zeit (s)'
# set grid
set xrange [0:10]
set yrange [0:2]
# set format x "%.0s%c"
set datafile separator ','
set samples 10000

h0 = 1
a = 0.5
T = 2*sqrt(2*h0/a)
h(x,n) = h0 - 0.5*a*(x-n*T)**2

# Styling
# Use valid color syntax and distinct colors per dataset
set style line 1 lw 1.5 pt 7 ps 0.5 lc rgb 'black' dt 4
set style line 2 lw 2 pt 7 ps 0.5 lc rgb 'blue' 
set style line 3 lw 2 pt 7 ps 0.5 lc rgb 'purple'
set style line 4 lw 2 pt 4 lc rgb 'red' 



# Plot
plot \
    h(x,0) with lines ls 4 notitle, \
    h(x,1) with lines ls 4 notitle, \



# set out