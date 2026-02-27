reset
set encoding utf8 

# set terminal epslatex color
# set out 'TV3.tex' #################

# ============================ Plot Settings ============================



set title "Jojo-Bewegung"
set ylabel 'Höhe (m)'
set xlabel 'Zeit (s)'
# set grid
set xrange [0:10]
set yrange [-5:5]
# set format x "%.0s%c"
set datafile separator ','
set samples 10000

h0 = 1
a = 2
T = 2*sqrt(2*h0/a)
v_max = a*T
k = 1.0 # Dämpfungsfaktor
h(x,n) = k**n * (h0 - 0.5*a*(x-n*T)**2)
v_down(x,n) = -sqrt(2*a*(h0 - h(x,n)))
v_up(x,n) = +sqrt(2*a*(h0 - h(x,n)))
v(x,n) = (x-n*T < T/2) ? v_down(x,n) : v_up(x,n)
# Styling

# Use valid color syntax and distinct colors per dataset
set style line 1 lw 1.5 pt 7 ps 0.5 lc rgb 'black' dt 4
set style line 2 lw 2 pt 7 ps 0.5 lc rgb 'blue' 
set style line 3 lw 2 pt 7 ps 0.5 lc rgb 'purple'
set style line 4 lw 2 pt 4 lc rgb 'red' 



# Plot
plot \
    v(x,0) with lines ls 4 notitle, \
    v(x,1) with lines ls 4 notitle, \
    v(x,2) with lines ls 4 notitle, \
    v(x,3) with lines ls 4 notitle, \
    v(x,4) with lines ls 4 notitle




# set out