reset
set encoding utf8 

# set terminal epslatex color
# set out 'TV3.tex' #################

# ============================ Plot Settings ============================



set title "Anregung-Bewegung (t, y_B)"
set ylabel 'Höhe (m)'
set xlabel 'Zeit (s)'
# set grid
set xrange [0:8]
set yrange [0.7:1.2]
# set format x "%.0s%c"
set datafile separator ','
set samples 10000

# Fit
h1(x) = a1*x**2 + b1*x + c1
a1 = -8.752e-1
b1 = 3.319e-2
c1 = 9.814e-1
h2(x) = a2*x**2 + b2*x + c2
h3(x) = a3*x**2 + b3*x + c3
h4(x) = a4*x**2 + b4*x + c4
h5(x) = a5*x**2 + b5*x + c5



set fit quiet
fit [1.166:2.866] h2(x) 'data-60fps.csv' using 1:3 via a2, b2, c2
fit [3.0:4.5] h3(x) 'data-60fps.csv' using 1:3 via a3, b3, c3
fit [4.5:5.8] h4(x) 'data-60fps.csv' using 1:3 via a4, b4, c4
fit [5.8:6.8] h5(x) 'data-60fps.csv' using 1:3 via a5, b5, c5

# Styling
# Use valid color syntax and distinct colors per dataset
set style line 1 lw 1.5 pt 7 ps 0.5 lc rgb 'black' dt 4
set style line 2 lw 1.5 pt 4 ps 0.5 lc rgb 'blue' 
set style line 3 lw 2 pt 7 ps 0.5 lc rgb 'purple'
set style line 4 lw 1.5 pt 4 lc rgb 'red' 
set style line 5 lw 1.5 pt 4 lc rgb 'black' 


# Plot
plot \
    'Jojo-2B.csv' using 1:3 with points ls 2 title 'Messdaten'





# set out