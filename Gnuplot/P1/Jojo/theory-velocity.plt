reset
set encoding utf8 

set terminal epslatex color
set out 'theory-velocity.tex' #################

# ============================ Plot Settings ============================



set title "Jojo-Bewegung (t, v_y)"
set ylabel 'Geschwindigkeit (m/s)'
set xlabel 'Zeit (s)'
# set grid
set xrange [0:10]
set yrange [-2:2]
# set format x "%.0s%c"
set datafile separator ','
set samples 10000

h0 = 1
a = 2
T = 2*sqrt(2*h0/a)
v_max = a*T# Dämpfungsfaktor
h(x,n) =(h0 - 0.5*a*(x-n*T)**2)
v(x,n) = -a*(x-n*T)
# Styling

# Use valid color syntax and distinct colors per dataset
set style line 1 lw 1.5 pt 7 ps 0.5 lc rgb 'black' dt 4
set style line 2 lw 2 pt 7 ps 0.5 lc rgb 'blue' 
set style line 3 lw 2 pt 7 ps 0.5 lc rgb 'purple'
set style line 4 lw 2 pt 4 lc rgb 'red' 



# Plot
plot \
    v(x,0) with lines ls 2 notitle, \
    v(x,1) with lines ls 2 notitle, \
    v(x,2) with lines ls 2 notitle, \
    v(x,3) with lines ls 2 notitle, \
    v(x,4) with lines ls 2 notitle




set out