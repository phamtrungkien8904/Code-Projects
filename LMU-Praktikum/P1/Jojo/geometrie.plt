reset
set encoding utf8 

# set terminal epslatex color
# set out 'TV3.tex' #################

# ============================ Plot Settings ============================



set title "Trägheitsradius (r, RJ)"
set ylabel 'RJ (cm)'
set xlabel 'r (cm)'
# set grid
set xrange [0:2]
# set yrange [0:1]
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

H = 1.1
h = 0.4
R = 2.5

RJ(x) = sqrt(x**2/2 * (1 - 2*H/h * R**4/x**4)/(1 - 2*H/h * R**2/x**2))
# Plot
plot \
    RJ(x) with lines ls 2 title 'Theorie'





# set out